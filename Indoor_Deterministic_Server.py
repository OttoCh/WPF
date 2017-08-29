#Program untuk mengolah data yang baru didapat langsung dari RSSI_AP*.txt
#Data hasil pengolahan offline akan disimpan dalam sebuah file .txt, nanti progarm tinggal baca dari situ dulu
#program akan menerima bacaan dari alat dan kemudian memberikan balasan berupa persentase kemungkinan posisi yg ada
import os.path
import paho.mqtt.client as mqtt
import numpy as np
import math
import itertools as itertools

AverageData_filename = "AverageData.txt"
Result_filename = "result.txt"

#Ref Data 6 posisi, 6 AP
totalPosition = 6
totalAP = 6
RefData = [[0 for x in range(totalPosition)] for y in range(totalAP)]

#Realtime data. 6 AP
RealtimeData = [0 for x in range(totalAP)]

#untuk menyimpan hasil perhitungan euclidian 
SquaredDeltaSignalResult = [[0 for x in range(totalPosition)] for y in range(totalAP)]

#untuk menyimpan hasil euclidian
ResultEuclidian = [0 for x in range(0,20)]

#untuk menyimpan hasil posisi
ResultPosition = [0 for x in range(0,20)]

topic_AP = "otto/RSSI/#"
topic_AP1 = "otto/RSSI/AP1"
topic_AP2 = "otto/RSSI/AP2"
topic_AP3 = "otto/RSSI/AP3"
topic_AP4 = "otto/RSSI/AP4"
topic_AP5 = "otto/RSSI/AP5"
topic_AP6 = "otto/RSSI/AP6"
topicResult = "otto/result"

AP1_Data = [0]
AP2_Data = [0]
AP3_Data = [0]
AP4_Data = [0]
AP5_Data = [0]
AP6_Data = [0]

AP1_Data[0] = False
AP2_Data[0] = False
AP3_Data[0] = False
AP4_Data[0] = False
AP5_Data[0] = False
AP6_Data[0] = False

def on_connect(client, userdata, flags, rc):
	print("Connected with result code" + str(rc))
	client.subscribe([(topic_AP1,0),(topic_AP2,0),(topic_AP3,0), \
		(topic_AP4,0),(topic_AP5,0),(topic_AP6,0)])

def on_message(client, userdata, msg):
	print(msg.topic + " " + str(msg.payload))

def ReadExistingData():
	readFile = open(AverageData_filename, "r")
	i=0
	comment = False
	for line in readFile:
		j=0
		#remove \n from string
		a = line.rstrip()
		#split by \t
		res = a.split("\t")
		for x in res:
			if(x=='#'):
				comment = True	
				break
			else:
				RefData[i][j] = float(x)
				j = j+1
		if(comment==False):
			i = i+1
		else:
			comment=False

def resetAP_Condition():
	AP1_Data[0] = False
	AP2_Data[0] = False
	AP3_Data[0] = False
	AP4_Data[0] = False
	AP5_Data[0] = False
	AP6_Data[0] = False

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

def calculateAllPossibleCombination():
	AP = [0,1,2,3,4,5]
	combinar = 3
	k=0
	for item in itertools.combinations(AP,combinar):
		currentExpectedPosition = 0
		current_diftotal = 0
		minimum_diftotal = 1000	
		for i in xrange(0,6):
			for j in item:
				current_diftotal += SquaredDeltaSignalResult[i][j]
			current_diftotal = math.sqrt(current_diftotal)
			if(current_diftotal<minimum_diftotal):
				minimum_diftotal = current_diftotal
				currentExpectedPosition = i+1
		ResultEuclidian[k] = minimum_diftotal
		ResultPosition[k] = currentExpectedPosition
		k+=1

def determinedProbabilityOfPosition():
	textFile = open(Result_filename, "a")
	textFile.write('\n')
	for i in ResultPosition:
		textFile.write(str(i) + ",")
	textFile.close()
	for x in xrange(1,7):
		p = ResultPosition.count(x)
		result = p*100/20
		messageResult = str(result) + "/" + str(x)
		client.publish(topicResult, messageResult)
		textFile = open(Result_filename, "a")
		textFile.write('\n' + str(x) + ": " + '\t' + str(result) + "%")
		textFile.close()

def calculatePosition():
	if(AP1_Data[0] == True and AP2_Data[0] == True and AP3_Data[0] == True and AP4_Data[0] == True and AP5_Data[0] == True and AP6_Data[0] == True):
		textFile = open(Result_filename, "a")
		textFile.write("\nBegin new session \n")
		textFile.close()
		i=0
		for x in range(totalPosition):
			j=0
			total_dif=0
			for x in range(totalAP):
				dif = euclidianDistance(RefData[i][j], RealtimeData[j])
				SquaredDeltaSignalResult[i][j] = dif
				j+=1
			i+=1
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

client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)
client.loop_forever()
