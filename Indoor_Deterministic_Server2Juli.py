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
totalPosition = 67
totalAP = 4
#RefData = [[0 for x in range(totalPosition)] for y in range(totalAP)]
RefData = [[0 for x in range(totalAP)] for y in range(totalPosition)]
totalPossibleCombination = 1;

#Realtime data. 4 AP
RealtimeData = [-1.00 for x in range(totalAP)]

#untuk menyimpan hasil perhitungan euclidian 
SquaredDeltaSignalResult = [[0 for x in range(totalAP)] for y in range(totalPosition)]

#untuk menyimpan hasil euclidian
ResultEuclidian = [0 for x in range(0,totalPossibleCombination)]

#untuk menyimpan hasil posisi
ResultPosition = [0 for x in range(0,totalPossibleCombination)]

topic_Data = "otto/data"
topicResult = "otto/result"

doneReadRefData = [False]

def on_connect(client, userdata, flags, rc):
	print("Connected with result code" + str(rc))
	client.subscribe([(topic_Data,0)])

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
	doneReadRefData[0] = True
	print doneReadRefData[0]

def euclidianDistance(num1, num2):
	return (num1-num2)**2

def calculateAllPossibleCombination():
	AP = [0,1,2,3]
	combinar = 4
	for item in itertools.combinations(AP,combinar):
		currentExpectedPosition = 0
		current_diftotal = 0
		minimum_diftotal = 1000	
		for i in xrange(0,totalPosition):
			for j in item:
				#print(str(j) + " " + str(RealtimeData[j]) + " RD")
				if(RealtimeData[j] != 100):
					current_diftotal += SquaredDeltaSignalResult[i][j]
			current_diftotal = math.sqrt(current_diftotal)
			if(current_diftotal<minimum_diftotal):
				print(str(i) + " " + str(j) + " :" + str(current_diftotal) + " cd")
				minimum_diftotal = current_diftotal
				currentExpectedPosition = i+1
	print("expected Position: " + str(currentExpectedPosition))
	client.publish(topicResult, str(currentExpectedPosition))


def determinedProbabilityOfPosition():
	#untuk skrg ini ga dipanggil karena tidak berguna gara gara combinar=4
	textFile = open(Result_filename, "a")
	textFile.write('\n')
	for i in ResultPosition:
		textFile.write(str(i) + ",")
	textFile.close()
	for x in xrange(1,7):
		p = ResultPosition.count(x)
		result = p*100/20
		messageResult = str(result) + "/" + str(x)
		#ini yg di publish harusnya angka di koordinat brapa posisi user
		client.publish(topicResult, messageResult)
		textFile = open(Result_filename, "a")
		textFile.write('\n' + str(x) + ": " + '\t' + str(result) + "%")
		textFile.close()


def calculatePosition():
	textFile = open(Result_filename, "a")
	textFile.write("\nBegin new session \n")
	textFile.close()
	for i in range(totalPosition):
		for j in range(totalAP):
			total_dif=0
			dif = euclidianDistance(RefData[i][j], RealtimeData[j])
			#print(str(i) + " " + str(j) + " :" + str(dif))
			SquaredDeltaSignalResult[i][j] = dif
	calculateAllPossibleCombination()
	#determinedProbabilityOfPosition()

def GetData(client, userdata, message):
	print("call")
	print message.payload
	print doneReadRefData
	if(doneReadRefData[0] == True):
		j=0
		print("begin")
		A = message.payload.rstrip()
		Data = A.split("\t")
		print("split data")
		for x in Data:
			print x
			RealtimeData[j] = float(x)
			j += 1
		print(RealtimeData)
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
client.message_callback_add(topic_Data, GetData)

client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)
client.loop_forever()
