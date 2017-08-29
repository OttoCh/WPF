import os.path
import paho.mqtt.client as mqtt

base_filename = "RSSI_AP"
AP1_filename = base_filename + "1.txt"
AP2_filename = base_filename + "2.txt"
AP3_filename = base_filename + "3.txt"
AP4_filename = base_filename + "4.txt"
AP5_filename = base_filename + "5.txt"
AP6_filename = base_filename + "6.txt"
AP7_filename = base_filename + "7.txt"
AP8_filename = base_filename + "8.txt"

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
topic_X = "otto/coor/x"
topic_Y = "otto/coor/y"
topic_reset = "otto/reset"
topic_ACK = "otto/ACK"

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
		(topic_AP4,0),(topic_AP5,0),(topic_AP6,0),(topic_AP7,0),(topic_AP8,0),(topic_Y_change,0),(topic_X_change,0),(topic_reset,0)])

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
		if(y[0]==10):
			y[0]=0
		print y[0], " (+)"
	elif message.payload == "0":
		y[0]-=1
		if(y[0]==-1):
			y[0]=9
		print y[0], " (-)"
	ystr[0] = str(y[0])
	write_new_coordinate(AP1_filename)
	write_new_coordinate(AP2_filename)
	write_new_coordinate(AP3_filename)
	write_new_coordinate(AP4_filename)
	write_new_coordinate(AP5_filename)
	write_new_coordinate(AP6_filename)
	write_new_coordinate(AP7_filename)
	write_new_coordinate(AP8_filename)
	client.publish(topic_Y, y[0])
	client.publish(topic_ACK, "1")
	
def change_X_coor(client, userdata, message):
	print "Change X coordinate to"
	if message.payload == "1":
		x[0]+=1
		if(x[0]==10):
			x[0]=0;
		print x[0], " (+)"
	elif message.payload == "0":
		x[0]-=1
		if(x[0]==-1):
			x[0]=9
		print x[0], " (-)"
	xstr[0] = str(x[0])
	write_new_coordinate(AP1_filename)
	write_new_coordinate(AP2_filename)
	write_new_coordinate(AP3_filename)
	write_new_coordinate(AP4_filename)
	write_new_coordinate(AP5_filename)
	write_new_coordinate(AP6_filename)
	write_new_coordinate(AP7_filename)
	write_new_coordinate(AP8_filename)
	client.publish(topic_X, x[0])
	client.publish(topic_ACK, "1")

def reset(client, userdata, message):
	print "Reset"
	if message.payload == "1":	
		#write data in a new file
		#Belum Berfungsi, harus cari cara yang bagus dulu untuk meruabh variabel
		base_filename = "RSSI_AP"
		base_filename += "~"
		AP1_filename = base_filename + "1.txt"
		AP2_filename = base_filename + "2.txt"
		AP3_filename = base_filename + "3.txt"
		AP4_filename = base_filename + "4.txt"

def Create_File(w_filename):
	if os.path.isfile(w_filename)==False:
		writeTimestamp(w_filename)
		textFile = open(w_filename, "w")
		textFile.write("#DATA RSSI " + w_filename)
	else:
		w_filename += "|"
		writeTimestamp(w_filename)
		textFile = open(w_filename, "w")
		textFile.write("#DATA RSSI " + w_filename)

def Write_File(w_filename, message):
	#write RSSI to file
	textFile = open(w_filename, "a")
	textFile.write('\t' + str(message.payload))
	textFile.close()

def write_AP_RSSI(client, userdata, message):
	print "receive AP Data"
	if message.topic == topic_AP1:
		#write RSSI to file
		w_filename = AP1_filename
	elif message.topic == topic_AP2:
		#Write to another file
		w_filename = AP2_filename
	elif message.topic == topic_AP3:
		#Write to another file
		w_filename = AP3_filename
	elif message.topic == topic_AP4:
		#Write to another file 
		w_filename = AP4_filename
	elif message.topic == topic_AP5:
		#Write to another file 
		w_filename = AP5_filename
	elif message.topic == topic_AP6:
		#Write to another file 
		w_filename = AP6_filename
	elif message.topic == topic_AP7:
		#Write to another file 
		w_filename = AP7_filename
	elif message.topic == topic_AP8:
		#Write to another file 
		w_filename = AP8_filename
	Write_File(w_filename, message)
	#client.publish(topic_ACK, "1")

def writeTimestamp(filename):
	import time
	import datetime
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	textFile = open(filename, "a")
	textFile.write("\ntimestamp: " + st + '\n')
	textFile.close()

#buat dulu filenya
Create_File(AP1_filename)
Create_File(AP2_filename)
Create_File(AP3_filename)
Create_File(AP4_filename)
Create_File(AP5_filename)
Create_File(AP6_filename)
Create_File(AP7_filename)
Create_File(AP8_filename)
client.message_callback_add(topic_Y_change, change_Y_coor)
client.message_callback_add(topic_X_change, change_X_coor)
client.message_callback_add(topic_reset, reset)
client.message_callback_add(topic_AP, write_AP_RSSI)

client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)
client.loop_forever()
