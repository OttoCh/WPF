#7 December 2016
#Otto Christianto
#Department of Physics, Institut Teknologi Bandung
#otto.christianto.oc@gmail.com
#Code written for position trilateration using Gaussian Elimination!

import os.path
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import numpy as np

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
plsqx = [0]
plsqy = [0]

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

def AP_distance(RSSI, a, b, c, d):
	#data dari AP1!
	#d = 10^((int)msg.payload - P0 + b)/(10*a)#+- masih terbalik
	#d = 10**(RSSI- P0 + b)/(10*a)
	d = a + b*RSSI + c*(RSSI**2) + d*(RSSI**3)
	return d

#def Calculation(client, userdata, msg):
def Calculation(RSSI, i):
	if(i==0):
#	if(msg.topic == topic_RSSI_AP1):
		a = 331.7984
		b = 12.2693
		c = 0.148
		d = 0.0005753657
		d1[0] = AP_distance(RSSI, a, b, c, d)
		#dAP[0][2] = AP_dist66ance((int)msg.payload, P0, a, b)
		#d1[0] = AP_distance((int)msg.payload, P0, a, b)
		d1_calculate[0] = True
	elif(i==1):
#	else if(msg.topic == topic_RSSI_AP2):
		a = 332.552755516578
		b = 12.336837715514
		c = 0.149975919933423
		d = 0.000588687227001324
		d2[0] = AP_distance(RSSI, a, b, c, d)
		#dAP[1][2] = AP_distance((int)msg.payload, P0, a, b)
		#d2[0] = AP_distance((int)msg.payload, P0, a, b)
		d2_calculate[0] = True
	elif(i==2):
#	else if(msg.topic == topic_RSSI_AP3):
		a = -18.7261701221980
		b = -0.588228463035758
		c = -0.00563360852373006
		d = -0.0000267992952860554
		d3[0] = AP_distance(RSSI, a, b, c, d)
		#dAP[2][2] = AP_distance((int)msg.payload, P0, a, b)
		#d3[0] = AP_distan93ce((int)msg.payload, P0, a, b)
		d3_calculate[0] = True
	elif(i==3):
#	else if(msg.topic == topic_RSSI_AP4):
		a = 31.0176857270489
		b = 1.44125883129203
		c = 0.0195941795335556
		d = 0.0000724853747877311
		d4[0] = AP_distance(RSSI, a, b, c, d)
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
		dAP = [(0,0,d1),(10,0,d2),(10,10,d3),(0,10,d4)]
		plsq = leastsq(residuals, p0, args=(dAP))
		print d1
		print d2
		print d3
		print d4
		print "done"
		plsqx[0] = plsq[0]
		plsqy[0] = plsq[1]
		print plsq[0]

def residuals(point, data):
	d = sqrt( square(data[0] - point[0]) + square(data[1] - point[1]) ) * data[2]
	return d
	
def LeastDistance(x1, y1, x2, y2, r):
	return abs(sqrt((x2-x1)**2 + (y2-y1)**2)-r)

def beginLeastDistanceAnalytic(res):
	prAP = [[0,0,d1[0]], [10,0,d2[0]], [10,10,d3[0]], [0,10,d4[0]]]
	dist = [0,0,0,0]
	lastDist = 100
	Pos = [0,0]
	xyrange = np.linspace(0.0, 10.0, 10/res)
	#for x in range(len(xyrange)-1):
	for x in xyrange:
		for y in xyrange:
			for i in xrange(0,4):
				dist[i] = LeastDistance(x,y,prAP[i][0], prAP[i][1], prAP[i][2])
			totalDist = dist[0] + dist[1] + dist[2] + dist[3]
			if(totalDist < lastDist):
				print "DIST"
				print dist[0]
				print dist[1]
				print dist[2]
				print dist[3]
				print totalDist
				lastDist = totalDist
				Pos[0] = x
				Pos[1] = y

	#output: titik dengan jarak terdekat di 4 sisi
	return Pos

def FindLeastDistanceMethod():
	Pos = beginLeastDistanceAnalytic(0.1)
	print "from least distance analytic"
	print Pos
	return Pos
			
			


#terima dulu semua data
#ubah satu persatu menjadi data d
#kumpulkan semua ke dalam satu fungsi
#lakukan non-linear least squareas
#tulis semua hasil x,y,RSSI,d,xo,yo, 

for i in xrange(0,4):
	print "A"
	#0,0 -66, -99,-99,-95
	#7,3 -95, -70, -85, -90
	#7,7 -90, -87, -64, -87
	#1,1 -67, -94, -89, -95
	#9,1 -91, -68, -84, -90
	#9,9 -95, -92, -62, -82
	#1,9 
	if(i==0):
		Calculation(-94,i)
		#Calculation(87, i)
	elif(i==1):
		Calculation(-87,i)
		#Calculation(83, i)
	elif(i==2):
		Calculation(-64,i)
		#Calculation(82, i)
	elif(i==3):
		Calculation(-87,i)
		#Calculation(93, i)

Pos = FindLeastDistanceMethod()

#buat visualisasi
fig = plt.figure()
ax = fig.add_subplot(1,1,1);
ax.set_xlim((-15, 15))
ax.set_ylim((-15, 15))
#plotting
#[(0,0,d1),(0,10,d2),(9,10,d3),(9,0,d4)]
circ = plt.Circle((0,0), radius=d1[0], color='b', alpha=0.5)
circ2 = plt.Circle((0,0), radius=0.01, color='r', alpha=1)
ax.add_patch(circ)
ax.add_patch(circ2)

circ = plt.Circle((10,0), radius=d2[0], color='b', alpha=0.5)
circ2 = plt.Circle((0,10), radius=0.01, color='r', alpha=1)
ax.add_patch(circ)
ax.add_patch(circ2)

circ = plt.Circle((10,10), radius=d3[0], color='b', alpha=0.5)
circ2 = plt.Circle((9,10), radius=0.01, color='r', alpha=1)
ax.add_patch(circ)
ax.add_patch(circ2)

circ = plt.Circle((0,10), radius=d4[0], color='b', alpha=0.5)
circ2 = plt.Circle((9,0), radius=0.01, color='r', alpha=1)
ax.add_patch(circ)
ax.add_patch(circ2)

circ = plt.Circle((Pos[0],Pos[1]), radius=0.2, color='r', alpha=1)
ax.add_patch(circ)

#buat kotak
rect=plt.Rectangle((0,0), 10, 10, fill=False)
ax.add_patch(rect)

plt.show()

#client.message_callback_add(topic_RSSI_AP1, Calculation);
#client.message_callback_add(topic_RSSI_AP2, Calculation);
#client.message_callback_add(topic_RSSI_AP3, Calculation);
#client.message_callback_add(topic_RSSI_AP4, Calculation);

#client.on_connect = on_connect
#client.on_message = on_message

#client.connect("23.92.65.163", 1883, 60)
#client.loop_forever()
