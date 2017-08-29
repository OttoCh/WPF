#7 December 2016
#Otto Christianto
#Department of Physics, Institut Teknologi Bandung
#otto.christianto.oc@gmail.com
#Code written for position trilateration using 

import os.path
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt

from numpy import *
from scipy.optimize import leastsq

#Bila node ditambah maka ini juga harus ditambah
total_node = 4
topic_RSSI_AP1 = "otto/RSSI/AP1"
topic_RSSI_AP2 = "otto/RSSI/AP2"
topic_RSSI_AP3 = "otto/RSSI/AP3"
topic_RSSI_AP4 = "otto/RSSI/AP4"


client = mqtt.Client()

#menyimpan jarak radius tiap AP
d1 = [0]
d2 = [0]
d3 = [0]
d4 = [0] 
d1_calculate = [0]
d2_calculate = [0]
d3_calculate = [0]
d4_calculate = [0]

d1_calculate[0] = False
d2_calculate[0] = False
d3_calculate[0] = False
d4_calculate[0] = False

#data dasar, posisi x y dari AP, xmax=10, ymax=11
#dAP = [(1,1,0),(1,11,0),(10,11,0),(10,1,0)]

def on_connect(client, userdata, flags, rc):
	print("connected with result code" + str(rc))
	client.subscribe([topic])

#Tes, bisa tidak
def subscribe_to(topic):
	client.subscribe([topic,0]);

def on_message(client, userdata, msg):
	print(msg.topic + " " + str(msg.payload))

def send_position(msg_x, msg_y):
	topic_position_x = "otto/position/x"
	topic_position_y = "otto/position/y"

	#publish posisi
	client.publish(topic_position_x, msg_x)
	client.publish(topic_position_y, msg_y)
	#tulis posisi
	Write_File(msg_x, msg_y)

def Write_File(x, y):
	w_filename = "Position_list.txt"
	if os.path.isfile(w_filename)==False:
		textFile.open(w_filename, "w")
		textFile.write("#New Position\n")
	textFile = open(w_filename, 'a')
	textFile.write("x\ty\n")
	textFile.close()

def AP_distance(RSSI, P0, a, b):
	#data dari AP1!
	#d = 10^((int)msg.payload - P0 + b)/(10*a)#+- masih terbalik
	d = 10**(RSSI- P0 + b)/(10*a)
	return d

#def Calculation(client, userdata, msg):
def Calculation(RSSI, i):
	if(i==0):
#	if(msg.topic == topic_RSSI_AP1):
		P0 = 66	#daya referensi
		a = 1.14 #path loss
		b = 0	#practically 0, shadow fading
		d1[0] = AP_distance(RSSI, P0, a, b)
		#dAP[0][2] = AP_distance((int)msg.payload, P0, a, b)
		#d1[0] = AP_distance((int)msg.payload, P0, a, b)
		d1_calculate[0] = True
	elif(i==1):
#	else if(msg.topic == topic_RSSI_AP2):
		P0 = 62
		a = 1.239 
		b = 0
		d2[0] = AP_distance(RSSI, P0, a, b)
		#dAP[1][2] = AP_distance((int)msg.payload, P0, a, b)
		#d2[0] = AP_distance((int)msg.payload, P0, a, b)
		d2_calculate[0] = True
	elif(i==2):
#	else if(msg.topic == topic_RSSI_AP3):
		P0 = 65
		a = 0.9791
		b = 0
		d3[0] = AP_distance(RSSI, P0, a, b)
		#dAP[2][2] = AP_distance((int)msg.payload, P0, a, b)
		#d3[0] = AP_distance((int)msg.payload, P0, a, b)
		d3_calculate[0] = True
	elif(i==3):
#	else if(msg.topic == topic_RSSI_AP4):
		P0 = 66
		a = 1.135
		b = 0
		d4[0] = AP_distance(RSSI, P0, a, b)
		#dAP[3][2] = AP_distance((int)msg.payload, P0, a, b)
		#d4[0] = AP_distance((int)msg.payload, P0, a, b)
		d4_calculate[0] = True
	else:
		print "what it is?"
	Trilaterate(d1[0], d2[0], d3[0], d4[0])
	#d = 10^((int)msg.payload - P0 + b)/(10*a)#+- masih terbalik

def Trilaterate(d1, d2, d3, d4):
	if(d1_calculate[0] == True and d2_calculate[0] == True and d3_calculate[0] == True and d4_calculate[0] == True):
		#semua data sudah di update dan akan dilakukan perhitungan sekarang
		p0=[0,0]
		dAP = [(0,0,d1),(0,10,d2),(9,10,d3),(9,0,d4)]
		plsq = leastsq(residuals, p0, args=(dAP))
		print d1
		print d2
		print d3
		print d4
		print "done"
		print plsq[0]

def residuals(point, data):
	#based on paper 
	d = (sqrt( square(data[0] - point[0]) + square(data[1] - point[1]) ) * data[2])**2
	return d
	


#terima dulu semua data
#ubah satu persatu menjadi data d
#kumpulkan semua ke dalam satu fungsi
#lakukan non-linear least squareas
#tulis semua hasil x,y,RSSI,d,xo,yo, 

for i in xrange(0,4):
	print "A"
	if(i==0):
		Calculation(66,i)
	elif(i==1):
		Calculation(93,i)
	elif(i==2):
		Calculation(99,i)
	elif(i==3):
		Calculation(90,i)

#client.message_callback_add(topic_RSSI_AP1, Calculation);
#client.message_callback_add(topic_RSSI_AP2, Calculation);
#client.message_callback_add(topic_RSSI_AP3, Calculation);
#client.message_callback_add(topic_RSSI_AP4, Calculation);

#client.on_connect = on_connect
#client.on_message = on_message

#client.connect("23.92.65.163", 1883, 60)
#client.loop_forever()
