#7 December 2016
#Otto Christianto
#Department of Physics, Institut Teknologi Bandung
#otto.christianto.oc@gmail.com
#Code written for position trilateration using leastsquare with regression based

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
d5 = [0]
d6 = [0]
d7 = [0]
d8 = [0] 
d1_calculate = [0]
d2_calculate = [0]
d3_calculate = [0]
d4_calculate = [0]
d5_calculate = [0]
d6_calculate = [0]
d7_calculate = [0]
d8_calculate = [0]
plsqx = [0]
plsqy = [0]

d1_calculate[0] = False
d2_calculate[0] = False
d3_calculate[0] = False
d4_calculate[0] = False
d5_calculate[0] = False
d6_calculate[0] = False
d7_calculate[0] = False
d8_calculate[0] = False

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
	w_filename = "Gauss-Position-Field.txt"
	textFile = open(w_filename, 'a')
	textFile.write("%f\t%f\n" %(x,y))
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
		a = 242.7570
		b = 12.1145
		c = 0.188
		d = 0.000901142
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
	elif(i==4):
		a = 143.172206590981
		b = 7.22893442739178
		c = 0.115613007935828
		d = 0.000566004263916771
		d5[0] = AP_distance(RSSI, a, b, c, d)
		d5_calculate[0] = True
	elif(i==5):
		a = -653.820806282379
		b = -26.2500350191127
		c = -0.344216064681108
		d = -0.00150239286939062
		d6[0] = AP_distance(RSSI, a, b, c, d)
		d6_calculate[0] = True
	elif(i==6):
		a = 1257.64850093558
		b = 46.7150759373339
		c = 0.568577585101825
		d = 0.00225863458572056
		d7[0] = AP_distance(RSSI, a, b, c, d)
		d7_calculate[0] = True
	elif(i==7):
		a = 381.817448686091
		b = 17.811143957717615
		c = 0.268338652835319
		d = 0.00129025788693145
		d8[0] = AP_distance(RSSI, a, b, c, d)
		d8_calculate[0] = True
	else:
		print "what it is?"
	Trilaterate(d1[0], d2[0], d3[0], d4[0], d5[0], d6[0], d7[0], d8[0])
	#d = 10^((int)msg.payload - P0 + b)/(10*a)#+- masih terbalik

def Trilaterate(d1, d2, d3, d4, d5, d6, d7, d8):
	if(d1_calculate[0] == True and d2_calculate[0] == True and d3_calculate[0] == True and d4_calculate[0] == True and d5_calculate[0] == True and d6_calculate[0] == True and d7_calculate[0] == True and d8_calculate[0] == True):
		#semua data sudah di update dan akan dilakukan perhitungan sekarang
		p0=[0,0]
		dAP = [(0,0,d1),(20,0,d2),(20,20,d3),(0,20,d4),(10,0,d5),(20,10,d6),(10,20,d7),(0,10,d8)]
		plsq = leastsq(residuals, p0, args=(dAP))
		#print d1
		#print d2
		#print d3
		#print d4
		#print "done"
		plsqx[0] = plsq[0]
		plsqy[0] = plsq[1]
		#print plsq[0]

def residuals(point, data):
	d = sqrt( square(data[0] - point[0]) + square(data[1] - point[1]) ) * data[2]
	#d = sqrt( square(data[0] - point[0]) + square(data[1] - point[1]) )-data[2]
	return d
	
def LeastDistance(x1, y1, x2, y2, r):
	return abs(sqrt((x2-x1)**2 + (y2-y1)**2)-r)

def beginLeastDistanceAnalytic(res):
	prAP = [[0,0,d1[0]], [0,20,d2[0]], [20,20,d3[0]], [20,0,d4[0]], [0,10,d5[0]], [10,20,d6[0]], [20,10,d7[0]], [10,0,d8[0]]]
	dist = [0,0,0,0,0,0,0,0]
	lastDist = 1000
	Pos = [0,0]
	xyrange = np.linspace(0.0, 20.0, 20/res)
	#for x in range(len(xyrange)-1):
	for x in xyrange:
		for y in xyrange:
			for i in xrange(0,8):
				dist[i] = LeastDistance(x,y,prAP[i][0], prAP[i][1], prAP[i][2])
			totalDist = dist[0] + dist[1] + dist[2] + dist[3] + dist[4] + dist[5] + dist[6] + dist[7]
			if(totalDist < lastDist):
				#print "DIST"
				#print dist[0]
				#print dist[1]
				#print dist[2]
				#print dist[3]
				#print totalDist
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
#buat visualisasi
fig = plt.figure()
ax = fig.add_subplot(1,1,1);
ax.set_xlim((0, 20))
ax.set_ylim((0, 20))
#buat kotak
rect=plt.Rectangle((0,0), 20, 20, fill=False)
ax.add_patch(rect)

#(2,2)
AP1 = [65,62,65,69,72,82]
AP2 = [88,81,82,82,91,93]
AP3 = [94,94,93,93,93,93]
AP4 = [91,91,91,91,91,91]
AP5 = [70,64,66,65,64,66]
AP6 = [91,83,84,94,84,88]
AP7 = [89,89,89,89,89,89]
AP8 = [89,86,87,85,85,78]
#(2,18)
AP1 = [81,78,88,82,77,92,80]
AP2 = [80,78,79,78,84,83,79]
AP3 = [86,86,91,90,90,92,90]
AP4 = [91,91,91,91,91,91,92]
AP5 = [70,74,72,84,65,73,81]
AP6 = [80,82,79,79,76,73,82]
AP7 = [89,89,89,89,90,90,90]
AP8 = [86,83,85,86,86,85,90]
#(18,18)
AP1 = [80,83,83,83,82,91]
AP2 = [93,89,88,89,89,91]
AP3 = [65,69,71,64,69,72]
AP4 = [89,92,93,93,89,89]
AP5 = [78,76,75,76,75,70]
AP6 = [77,77,83,74,73,79]
AP7 = [90,90,92,92,81,90]
AP8 = [79,75,77,81,79,81]
#(18,2)
AP1 = [79,84,86,83,80,78,77]
AP2 = [93,93,93,94,94,94,94]
AP3 = [86,88,88,93,88,86,86]
AP4 = [79,78,79,78,77,73,77]
AP5 = [76,78,87,84,83,82,71]
AP6 = [69,77,74,77,80,82,79]
AP7 = [87,84,93,93,86,91,90]
AP8 = [75,73,72,72,74,73,68]
#(10,10)
AP1 = [73,76,81,78,83,81,70]
AP2 = [93,96,91,91,91,90,90]
AP3 = [80,85,83,83,83,82,78]
AP4 = [94,93,89,92,92,92,92]
AP5 = [79,79,80,76,80,80,74]
AP6 = [71,68,71,66,76,69,71]
AP7 = [93,93,90,92,92,92,93]
AP8 = [80,77,73,81,77,76,85]

w_filename = "Gauss-Position-Field.txt"
textFile = open(w_filename, 'a')
textFile.write("(10,10)\n")
textFile.close()

for j in xrange(0, len(AP1)):
	for i in xrange(0,8):
	
	#0,0 -66, -99,-99,-95
	#7,3 -95, -70, -85, -90
	#7,7 -90, -87, -64, -87
	#1,1 -67, -94, -89, -95
	#9,1 -91, -68, -84, -90
	#9,9 -95, -92, -62, -82
	#1,9 
		if(i==0):
			Calculation(-AP1[j],i)
			#Calculation(87, i)
		elif(i==1):
			Calculation(-AP2[j],i)
			#Calculation(83, i)
		elif(i==2):
			Calculation(-AP3[j],i)
			#Calculation(82, i)
		elif(i==3):
			Calculation(-AP4[j],i)
			#Calculation(93, i)
		elif(i==4):
			Calculation(-AP5[j],i)
		elif(i==5):
			Calculation(-AP6[j],i)
		elif(i==6):
			Calculation(-AP7[j],i)
		elif(i==7):
			Calculation(-AP8[j],i)

	Pos = FindLeastDistanceMethod()
	#point = [(0,0,d1[0]), (0,20,d2[0]), (20,20,d3[0]), (20,0,d4[0])]
	#args = (point)
	#p0 = [10,10]
	#plsq = leastsq(residuals, p0, args=(point))
	#print plsq[0]
#plotting
#[(0,0,d1),(0,10,d2),(9,10,d3),(9,0,d4)]
	circ = plt.Circle((Pos), radius=0.2, color='r', alpha=0.5 + 1/len(AP1))
	ax.add_patch(circ)
	Write_File(Pos[0], Pos[1])


plt.show()

#client.message_callback_add(topic_RSSI_AP1, Calculation);
#client.message_callback_add(topic_RSSI_AP2, Calculation);
#client.message_callback_add(topic_RSSI_AP3, Calculation);
#client.message_callback_add(topic_RSSI_AP4, Calculation);

#client.on_connect = on_connect
#client.on_message = on_message

#client.connect("23.92.65.163", 1883, 60)
#client.loop_forever()
