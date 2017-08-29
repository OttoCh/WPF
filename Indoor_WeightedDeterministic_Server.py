#Program untuk mengolah data yang baru didapat langsung dari RSSI_AP*.txt
#Data hasil pengolahan offline akan disimpan dalam sebuah file .txt, nanti progarm tinggal baca dari situ dulu
#program akan menerima bacaan dari alat dan kemudian memberikan balasan berupa persentase kemungkinan posisi yg ada
#Perbedaan program ini dengan yg Indoor_Deterministic_Server adalah disini sudah diterapkan rotasi dan
#bentuk file yang dibaca sudah berbeda dimana kita RSSI di 6 posisi akan ditulis di 4 arah berbeda (y[0])

import os.path
import paho.mqtt.client as mqtt
import numpy as np
import math
import itertools as itertools

AverageData_filename = "AverageData.txt"
Result_filename = "result.txt"

#Ref Data 6 posisi, 8 AP
totalPosition = 6
totalAP = 8
totalRotation = 4
RefData = [[[0 for x in range(totalPosition)] for z in range(totalRotation)] for y in range(totalAP)]

#Realtime data. 6 AP
RealtimeData = [0 for x in range(totalAP)]
#RealTimeRotation

#untuk menyimpan hasil perhitungan euclidian 
SquaredDeltaSignalResult = [[0 for x in range(totalPosition)]for y in range(totalAP)]

#untuk menyimpan hasil euclidian
ResultEuclidian = [0 for x in range(0,20)]

#untuk menyimpan hasil posisi
ResultPosition = [0 for x in range(0,20)]

#untuk menyimpan nilai kernel
kernel_value = [[0 for x in range(totalPosition)] for y in range(56)]

#arah kita
y = [0]
y[0] = 1

topic_AP = "otto/RSSI/#"
topic_AP1 = "otto/RSSI/AP1"
topic_AP2 = "otto/RSSI/AP2"
topic_AP3 = "otto/RSSI/AP3"
topic_AP4 = "otto/RSSI/AP4"
topic_AP5 = "otto/RSSI/AP5"
topic_AP6 = "otto/RSSI/AP6"
topic_AP7 = "otto/RSSI/AP7"
topic_AP8 = "otto/RSSI/AP8"
topicResult = "otto/result"
topic_Y = "otto/coor/y"

AP1_Data = [0]
AP2_Data = [0]
AP3_Data = [0]
AP4_Data = [0]
AP5_Data = [0]
AP6_Data = [0]
AP7_Data = [0]
AP8_Data = [0]

AP1_Data[0] = False
AP2_Data[0] = False
AP3_Data[0] = False
AP4_Data[0] = False
AP5_Data[0] = False
AP6_Data[0] = False
AP7_Data[0] = False
AP8_Data[0] = False

#weight from each AP (traditional way)
AP_Weight = [1,1,1,1,1,1,1,1]
AP_Sigma = [1,1,1,1,1,1,1,1]

def on_connect(client, userdata, flags, rc):
	print("Connected with result code" + str(rc))
	client.subscribe([(topic_AP1,0),(topic_AP2,0),(topic_AP3,0), \
		(topic_AP4,0),(topic_AP5,0),(topic_AP6,0),(topic_AP7,0),(topic_AP8,0),(topic_Y,0)])

def on_message(client, userdata, msg):
	print(msg.topic + " " + str(msg.payload))

def receive_Y_coor(client, userdata, message):
	y[0] = int(message.payload)-1

def ReadExistingData():
	readFile = open(AverageData_filename, "r")
	i=0
	k=0
	comment = False
	for line in readFile:
		j=0
		#remove \n from string
		a = line.rstrip()
		#split by \t
		res = a.split("\t")
		for x in res:
			if(x=='#' or x==""):
				comment = True	
				break
			else:
				RefData[i][k][j] = float(x)
				j = j+1
		if(comment==False):
			i = i+1
			if(i==7):
				i=1
				k+=1
		else:
			comment=False

def resetAP_Condition():
	AP1_Data[0] = False
	AP2_Data[0] = False
	AP3_Data[0] = False
	AP4_Data[0] = False
	AP5_Data[0] = False
	AP6_Data[0] = False
	AP7_Data[0] = False
	AP8_Data[0] = False

def euclidianDistance(num1, num2):
	return (num1-num2)**2

def calculateAverageData(Data, j):
	jumlahData= len(Data)
	total = 0
	for x in Data:
		if(float(x)==0):
			x=100.0
		total += float(x)
	avg = total/jumlahData
	RealtimeData[j] = avg
	return

def calculateAllPossibleCombination_WithWeight():
	AP = [0,1,2,3,4,5]
	combinar = 3
	k = 0	#untuk menghitung ini kombinasi ke berapa
	for item in itertools.combinations(AP,combinar):
		curTotal = 0
		print item
		print("kernel_value: ")
		for i in xrange(0,totalPosition):
			for j in item:
				#kalikan dengan weight 
				curTotal += SquaredDeltaSignalResult[i][j]*(AP_Weight[j])/(2*AP_Sigma[j])
			kernel_value[i][k] = math.exp(curTotal)
			print kernel_value[i][k]
			k+=1


			#current_diftotal = math.sqrt(current_diftotal)
			#if(current_diftotal<minimum_diftotal):
			#	minimum_diftotal = current_diftotal
			#	currentExpectedPosition = i+1
		#ResultEuclidian[k] = minimum_diftotal
		#ResultPosition[k] = currentExpectedPosition
		#k+=1

def determinedProbabilityOfPosition():
	print "Estimated Value"
	for k in range(56):
		curTotal = 0.0
		for i in xrange(0, totalPosition):
			curTotal += kernel_value[i][k]
		#ini adalah probabilitas posisiny
		estimatedValue = curTotal/20	#total sample = 20
		print("estimatedValue: " + str(estimatedValue))

def calculatePosition():
	#KONDISI INI DIGANTI BILA INGIN RUBAH DARI 6 JADI 8 AP!!
	if(AP1_Data[0] == True and AP2_Data[0] == True and AP3_Data[0] == True and AP4_Data[0] == True and AP5_Data[0] == True and AP6_Data[0] == True):
		textFile = open(Result_filename, "a")
		textFile.write("\nBegin new session \n")
		textFile.close()
		i=0
		for x in range(totalPosition):
			j=0
			total_dif=0
			for x in range(totalAP):
				dif = euclidianDistance(RefData[i][y[0]][j], RealtimeData[j])
				SquaredDeltaSignalResult[i][j] = dif
				j+=1
			i+=1
		#AKAR SquaredDeltaSignalResult membawa informasi yang dibutuhkan

		calculateAllPossibleCombination()
		determinedProbabilityOfPosition()
		resetAP_Condition()

def GetData(client, userdata, message):
	j=100
	if message.topic == topic_AP1:
		j=0
		AP1_Data[0] = True
	elif message.topic == topic_AP2:
		j=1
		AP2_Data[0] = True
	elif message.topic == topic_AP3:
		j=2
		AP3_Data[0] = True
	elif message.topic == topic_AP4:
		j=3
		AP4_Data[0] = True
	elif message.topic == topic_AP5:
		j=4
		AP5_Data[0] = True
	elif message.topic == topic_AP6:
		j=5
		AP6_Data[0] = True
	else:
		return 0
	A = message.payload.rstrip()
	Data = A.split("\t")
	if(j!=100):
		calculateAverageData(Data, j)
		calculatePosition()
	return 1

def writeTimestamp():
	import time
	import datetime
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	textFile = open(Result_filename, "a")
	textFile.write("\ntimestamp: " + st + '\n')
	textFile.close()

ReadExistingData()

writeTimestamp()

client = mqtt.Client()
client.message_callback_add(topic_AP, GetData)
client.message_callback_add(topic_Y, receive_Y_coor)

client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)
client.loop_forever()
