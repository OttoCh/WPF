#Program untuk membaca RSSI dari file dan langsung mengurutkannya agar didapat nilai tengahnya
#nilai yg didapat kemudian dituliskan di file lain sesuai ketentuan di Indoor_Deterministic_Server.py
#Sekalian akan digunakan untuk menentukan besaran weight untuk nanti digunakan!
#http://ieeexplore.ieee.org.sci-hub.cc/document/5684309/

import os.path
import paho.mqtt.client as mqtt

base_filename = "BurstNoise_AP"
AP1_filename = base_filename + "1.txt"
AP2_filename = base_filename + "2.txt"
AP3_filename = base_filename + "3.txt"
AP4_filename = base_filename + "4.txt"
AP5_filename = base_filename + "5.txt"
AP6_filename = base_filename + "6.txt"
AP7_filename = base_filename + "7.txt"
AP8_filename = base_filename + "8.txt"

base_resultFileName = "resultBurstNoise_AP"
burstNoiseAP1_filename = base_resultFileName + "1.txt"
burstNoiseAP2_filename = base_resultFileName + "2.txt"
burstNoiseAP3_filename = base_resultFileName + "3.txt"
burstNoiseAP4_filename = base_resultFileName + "4.txt"
burstNoiseAP5_filename = base_resultFileName + "5.txt"
burstNoiseAP6_filename = base_resultFileName + "6.txt"
burstNoiseAP7_filename = base_resultFileName + "7.txt"
burstNoiseAP8_filename = base_resultFileName + "8.txt"

topic_AP = "otto/RSSI/#"
topic_AP1 = "otto/RSSI/AP1"
topic_AP2 = "otto/RSSI/AP2"
topic_AP3 = "otto/RSSI/AP3"
topic_AP4 = "otto/RSSI/AP4"
topic_AP5 = "otto/RSSI/AP5"
topic_AP6 = "otto/RSSI/AP6"
topic_AP7 = "otto/RSSI/AP7"
topic_AP8 = "otto/RSSI/AP8"

topic_Y_change = "otto/coor/y_change"
topic_X_change = "otto/coor/x_change"

doneAP = [False, False, False, False, False, False, False, False]
allTopic_APX = [topic_AP1, topic_AP2, topic_AP3, topic_AP4, topic_AP5, topic_AP6, topic_AP7, topic_AP8]

count = [0]
newLine = [0]
x = [0]
y = [0]
xstr = [0]
ystr = [0]
oxstr = [0]
oystr = [0]
ystr[0] = str(y[0])
xstr[0] = str(x[0])
oxstr[0] = xstr[0]
oystr[0] = ystr[0]

count[0] = 0.0
newLine[0] = 0


client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
	print("Connected with result code" + str(rc))
	client.subscribe([(topic_AP1,0),(topic_AP2,0),(topic_AP3,0), \
		(topic_AP4,0),(topic_AP5,0),(topic_AP6,0),(topic_AP7,0),(topic_AP8,0),(topic_Y_change,0),(topic_X_change,0)])

def on_message(client, userdata, msg):
	print(msg.topic + " " + str(msg.payload))

def write_new_coordinate(w_filename):	
	textFile = open(w_filename, "a")
	textFile.write('\n' + xstr[0] + '\t' + ystr[0])
	textFile.close()

def change_Y_coor(client, userdata, message):
	print "Change Y coordinate to: "
	if message.payload == "1":
		y[0]+=1
		if(y[0]==5):
			y[0]=1
		print y[0], " (+)"
	elif message.payload == "0":
		y[0]-=0
		if(y[0]==0):
			y[0]=4
		print y[0], " (-)"
	ystr[0] = str(y[0])
	for i in xrange(0, len(allFileName)):
		write_new_coordinate(allFileName[i])

def change_X_coor(client, userdata, message):
	print "Change X coordinate to"
	if message.payload == "1":
		x[0]+=1
		print x[0], " (+)"
	elif message.payload == "0":
		x[0]-=1
		print x[0], " (-)"
	xstr[0] = str(x[0])
	for i in xrange(0, len(allFileName)):
		write_new_coordinate(allFileName[i])

def Create_File(w_filename):
	textFile = open(w_filename, "w")
	textFile.write("\n#\tDATA RSSI " + w_filename + "\n")

def Write_File(w_filename, message):
	#write RSSI to file
	textFile = open(w_filename, "a")
	if message.payload == "0":
		textFile.write("\t100")
	else:
		textFile.write("\t" + str(message.payload))
	textFile.close()

def write_AP_RSSI(client, userdata, message):
	print "receive AP Data"
	for i in xrange(0, len(allTopic_APX)):
		if message.topic == allTopic_APX[i]:
			w_filename = allFileName[i]
			doneAP[i] = True
			break
	Write_File(w_filename, message)
	#sehabis tulis langsung mulai sequence olah data
	burstNoiseFilter()

def resetDoneAPCond():
	for i in range(8):
		doneAP[i] = False

def writeTimestamp(filename):
	import time
	import datetime
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	textFile = open(filename, "a")
	textFile.write("\ntimestamp: " + st + '\n')
	textFile.close()

####################################################################################
#Bagian Burst Noise	

#raw data, disiapkan dahulu tempat kosong 40
totalSample = 40
RawData = [0 for i in range(totalSample)]

#all rawdata filename
allFileName = [AP1_filename, AP2_filename, AP3_filename, AP4_filename, AP5_filename, AP6_filename, AP7_filename, AP8_filename]
#all result filename
allResultFileName = [burstNoiseAP1_filename, burstNoiseAP2_filename, burstNoiseAP3_filename, burstNoiseAP4_filename, burstNoiseAP5_filename, burstNoiseAP6_filename, burstNoiseAP7_filename, burstNoiseAP8_filename]

#simpan panjang data
dataLength = [0]

#jumlah data yang mau di hilangkan
skipData = 8

#untuk menyimpan panjang data yang mau dirata ratakan
averagedDataRange = [0]

def burstNoiseFilter():
	if(doneAP[0]==True and doneAP[1]==True and doneAP[2]==True and doneAP[3]==True and doneAP[4]==True and doneAP[5]==True):
		#do everything that must be done
		#readRawData, store in array
		for file in allFileName:
			readRawData(file)
			#sortData
			sortData()
			#find median and find average
			avg = findAverageMiddleData()
			#write on a separate file
			writeDataToNewFile(file, avg)
		#reset file
		for i in xrange(0, len(allFileName)):
			Create_File(allFileName[i])
		#reset cond
		resetDoneAPCond()

def readRawData(filename):
	readFile = open(filename)
	for line in readFile:
		j=0
		#remove \n from string
		a = line.rstrip()
		#split by \t			
		res = a.split("\t")
		dataLength[0] = len(res)
		print res
		for l in res:
			if(l == '#' or l == ""):
				break
			else:
				RawData[j] = int(float(l))
				j = j+1

def sortData():
	#bubble sort(descending)
	#kedua for dimulai dari 2 karena 2 angka pertama akan digunakan untuk menentukan posisi, arah
	for j in xrange(2, dataLength[0]-1):
		a = RawData[j]
		b = RawData[j+1]
		if(a<b):
			c = RawData[j]
			RawData[j] = RawData[j+1]

def findAverageMiddleData():
	#Fungsi untuk mencari rata rata dari sebuah line data yang didapat
	#mulai dari 2 karena 2 data pertama (posisi dan arah) diabaikan
	z=2
	#skipData = dataLength[0]-2-usedMiddleData
	for j in range(skipData/2):
		z = z+1
	averagedDataRange[0] = dataLength[0]-2-(skipData/2)
	totalMiddleRawData = 0
	for dat in xrange(z,averagedDataRange[0]):
		totalMiddleRawData += RawData[dat]
	averageData = totalMiddleRawData/averagedDataRange[0]
	return averageData

def writeDataToNewFile(filename, average):
	#tentukan kita mesti tulis ke file mana berdasarkan sumber nama file
	w_filename = "dump.txt"
	for i in xrange(0, len(allFileName)):
		if allFileName[i]==filename:
			w_filename=allResultFileName[i]
	#Tulis data hasil 
	writeFile = open(w_filename, "a")
	writeFile.write('\n' + str(RawData[0]) + '\t' + str(RawData[1]) + '\t' + str(average))
	for i in xrange(2+skipData/2, averagedDataRange[0]):
		writeFile.write('\t' + str(RawData[i]))
	writeFile.close()

def createBurstNoiseFile(w_filename):
	if os.path.isfile(w_filename)==False:
		writeTimestamp(w_filename)
		textFile = open(w_filename, "a")
		textFile.write("\n#\tBurstNoiseFilter " + w_filename + "\tSkipdata: " + str(skipData) + "\tUsedRawData\n")
		textFile.write("\n#\tPoint\tOrientation\tAverage\n")
		textFile.close()

#################################################################################
#Initial routine
#buat file untuk simpan hasil
for i in xrange(0, len(allResultFileName)):
	createBurstNoiseFile(allResultFileName[i])

#buat dulu filenya buat simpan data awal
for i in xrange(0, len(allFileName)):
	Create_File(allFileName[i])

client.message_callback_add(topic_Y_change, change_Y_coor)
client.message_callback_add(topic_X_change, change_X_coor)
client.message_callback_add(topic_AP, write_AP_RSSI)

client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)
client.loop_forever()
