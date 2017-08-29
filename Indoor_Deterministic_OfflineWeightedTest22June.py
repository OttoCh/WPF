#program ini dipakai untuk mencari posisi indoor tetapi hanya menghasilkan gambar, per iterasi terakhir ada error ynag mengakibatkan
#gambar jadi tidak keluar sama sekali.

import math
import matplotlib
matplotlib.use('Agg')

import os.path
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import itertools as itertools
import pylab as pylab
from numpy import *

originAP = [[3.0,0.0], [27.0,0.0], [0.0,6.0], [27.0,12.0]]
rCircle = [[-1.0,-1.0], [-1.0,-1.0], [-1.0,-1.0], [-1.0,-1.0]]
IntersectCoor = [[-1.0,-1.0], [-1.0,-1.0], [-1.0,-1.0]]

TestData_filename = "TestData.txt"
Result_filename = "result.txt"

totalAP = 5
TestData = [0 for x in range(0,totalAP)]

numb = [1]
totalRSSIatTestData = 4
TestDataPosition = [-1]


def findIfCircleIntersect(circ1, circ2, r1, r2):
	if(distBetweenPoint(originAP[circ1], originAP[circ2]) < (r1 + r2)):
		return True
	else:
		return False

def distBetweenPoint(point1, point2):
	return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2) 

def resetCircIntersectConditionToFalse():
	circ12Intersect = False
	circ13Intersect = False
	circ23Intersect = False

def findCircleIntersection(x1,x2,y1,y2,r1,r2):
	xIntersect2 = 0
	xIntersect1 = 0
	yIntersect2 = 0
	yIntersect1 = 0
	if(x2-x1 == 0):
		yIntersect1 = (-r1**2 + r2**2 + y1**2 - y2**2)/(2*(y1-y2))
		yIntersect2 = yIntersect1
		a = 1
		b = -1*2*x1
		c = x1**2 + yIntersect1**2 - 2*yIntersect1*y1 + y1**2 - r1**2
		#print(str(a) + " " + str(b) + " " + str(c))
		inside = b**2-4*a*c
		if(inside>=0):
			xIntersect2 = (-b+math.sqrt(b**2-4*a*c))/(2*a)
			xIntersect1 = (-b-math.sqrt(b**2-4*a*c))/(2*a)
	elif(y2-y1 == 0):
		xIntersect1 = (-r1**2 + r2**2 + x1**2 - x2**2)/(2*(x1-x2))
		xIntersect2 = xIntersect1
		a = 1
		b = -1*2*y1
		c = y1**2 + xIntersect1**2 - 2*xIntersect1*x1 + x1**2 - r1**2
		#print(str(a) + " " + str(b) + " " + str(c))
		inside = b**2-4*a*c
		if(inside>=0):
			yIntersect2 = (-b+math.sqrt(b**2-4*a*c))/(2*a)
			yIntersect1 = (-b-math.sqrt(b**2-4*a*c))/(2*a)
	else:
		k1 = x1**2 - x2**2 + y1**2 - y2**2 - r1**2 + r2**2
		k2 = -k1/(2*(x2-x1))
		k3 = (y2-y1)/(x2-x1)
		k4 = k2-x1
		#print(str(k1) + " " + str(k2) + " " + str(k3) + " " + str(k4))
		a = (k3**2+1)
		b = (-2*k3*k4 - 2*y1)
		c = k4**2 + y1**2 - r1**2
		#print(str(a) + " " + str(b) + " " + str(c))
		inside = b**2-4*a*c
		if(inside>0):
			yIntersect1 = (-b+math.sqrt(b**2-4*a*c))/(2*a)
			yIntersect2 = (-b-math.sqrt(b**2-4*a*c))/(2*a)
			xIntersect1 = k2-yIntersect1*((y2-y1)/(x2-x1))
			xIntersect2 = k2-yIntersect2*((y2-y1)/(x2-x1))
		elif(inside<0 and b==0):
			yIntersect1 = math.sqrt((r1**2-c)/a)
			yIntersect2 = -yIntersect1
			xIntersect1 = k2-yIntersect1*((y2-y1)/(x2-x1))
			xIntersect2 = k2-yIntersect2*((y2-y1)/(x2-x1))
	writeToResultFile(xIntersect1, yIntersect1)
	drawIntersectionCoordinateToPlot(xIntersect1, yIntersect1)
	writeToResultFile(xIntersect2, yIntersect2)
	drawIntersectionCoordinateToPlot(xIntersect2, yIntersect2)
	#print "intersect coor"
	#print xIntersect1
	#print xIntersect2
	#print yIntersect1
	#print yIntersect2

def writeToResultFile(x,y):
	textFile = open(Result_filename, "a")
	textFile.write('\n' + str(numb[0])  + '\t' + str(x) + '\t' + str(y))
	textFile.close()

def writeResultFileHead():
	textFile = open(Result_filename, "a")
	textFile.write('\n' + "RealPos: " + str(TestData[4]))
	textFile.close()

def addWeight(j):
	w = [0.60, 0.58, 0.45, 1.0]
	for i in range(0,2):
		if(j==0):
			rCircle[j][i] = rCircle[j][i]*w[j]
		elif(j==1):
			rCircle[j][i] = (27.0 - abs(27.0 - rCircle[j][i])*w[j])
		elif(j==2):
			rCircle[j][i] = (12.0 - abs(12.0 - rCircle[j][i])*w[j])
		elif(j==3):
			rCircle[j][i] = (29.54 - abs(29.54- rCircle[j][i])*w[j])
		print("r setelah weight: " + str(j) + " " + str(i) + ": " + str(rCircle[j][i]))
	return

def drawCircle(originPoint_X, originPoint_Y, r_inner, r_outer):
	n = 50
	drawRange = np.linspace(r_inner, r_outer, n, endpoint=True)
	for i in drawRange:
		ax.axis("equal")
		circ = plt.Circle((originPoint_X,originPoint_Y), radius=i, color='r', alpha=0.1, fill=False)
		ax.add_patch(circ)

def saveFigure(filename):
	#pylab.savefig(filename, bbox_inches='tight')
	pylab.savefig(filename)

def clearFigure():
	plt.clf()

def ReadTestData(res):
	i=0
	for x in res:
		if(i==totalRSSIatTestData):
			TestDataPosition[0] = int(x)
			break
		TestData[i] = float(x)
		i = i+1

#def ReadTestData():
#	readFile = open(TestData_filename, "r")
#	comment = False
#	for line in readFile:
#		i=0
##		#remove \n from string
#		a = line.rstrip()
#		#split by \t
#		res = a.split("\t")
#		for x in res:
#			#ganti posisi koordinat x setiap kali koordinat y sudah mencapai 6
#			if(x=='#'):
#				comment = True
#				break
#			else:
#				TestData[i] = float(x)
#				i = i+1

def drawIntersectionCoordinateToPlot(x,y):
	xWrite = x+0.5
	yWrite = y-0.5
	x = format(round(x,2))
	y = format(round(y,2))
	coorStr = str(numb[0])
	#plt.Text(x-1.0,y-1.0,coorStr, fontsize=15)
	bx = plt.gca()
	bx.annotate(coorStr, xy=(xWrite, yWrite), fontsize=7)
	circ = plt.Circle((x,y), radius=0.2, color='k', alpha=1, fill=True)
	ax.add_patch(circ)
	numb[0] += 1

def calculateRadii(circNumb, RSSI):
	z = 100
	d = [-1,-1,-1]
	if(circNumb==0):
		a = 2.985
		b = 9.747
	elif(circNumb==1):
		a = 2.092
		b = 5.796
	elif(circNumb==2):
		a = 2.446
		b = 11.85
	elif(circNumb==3):
		a = 2.494
		b = 13.76
	for x in range(0,3):
		if(x==0):
			RSSIr = RSSI - 3.0
			#RSSIr = RSSI - 1.5
		elif(x==1):
			RSSIr = RSSI
		elif(x==2):
			RSSIr = RSSI + 3.0
			#RSSIr = RSSI + 1.5
		c = (RSSIr+b+z)/(-10*a)
		d[x] = 100*(10**(c))
	return d

def calculatePosition():
	AP = [0,1,2,3]
	combinar = 4
	for item in itertools.combinations(AP,combinar):
		for j in item:
			d = calculateRadii(j, -TestData[j])
			rCircle[j][0] = d[0]	#rInner
			rCircle[j][1] = d[2]	#rOuter
			#print("r sebelum weight: " + str(j) + " 0: " + str(rCircle[j][0]))
			#print("r sebelum weight: " + str(j) + " 1: " + str(rCircle[j][1]))
			#addWeight(j)
			#drawCircle(originAP[j][0], originAP[j][1], d[0], d[2])
			drawCircle(originAP[j][0], originAP[j][1], rCircle[j][0], rCircle[j][1])
			print(str(originAP[j][0]) + " " + str(originAP[j][1]) + " " + str(rCircle[j][0]) + " " + str(rCircle[j][1]))
		#gambar dulu lingkarannya
		secondCombinar = 2
		for i in itertools.combinations(item, secondCombinar):
			#print "==============================================="
			for j in xrange(0,4):
				j1, j2 = 0, 0
				if(j==0):
					j1 = 0
					j2 = 0
				elif(j==1):
					j1=0
					j2=1
				elif(j==2):
					j1=1
					j2=0
				elif(j==3):
					j1=1
					j2=1
				if(findIfCircleIntersect(i[0], i[1], rCircle[i[0]][j1], rCircle[i[1]][j2])):
					#print(str(originAP[i[0]][0]) + " " + str(originAP[i[1]][0]) + " " + str(originAP[i[0]][1]) + " " + str(originAP[i[1]][1]) + " " + str(rCircle[i[0]][j1]) + " " + str(rCircle[i[1]][j2]))
					findCircleIntersection(originAP[i[0]][0], originAP[i[1]][0], originAP[i[0]][1], originAP[i[1]][1], rCircle[i[0]][j1], rCircle[i[1]][j2])

#buat visualisasi
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
#ReadTestData()
#writeToResultFile(TestData[totalRSSIatTestData], 10000000)
rect=plt.Rectangle((0,0), 27, 12, fill=False)
ax.add_patch(rect)

#calculatePosition()
#fileName = "ResultPosOut" + str(TestData[totalRSSIatTestData]) + ".png"
#pylab.xlim([-50,50])
#pylab.ylim([-50,50])
#saveFigure(fileName)

readFile = open(TestData_filename, "r")
for line in readFile:
	numb[0] = 1
	#remove \n from string
	a = line.rstrip()
	#split by \t
	res = a.split("\t")
	if(res[0] != '#'):
		ReadTestData(res)
		writeToResultFile(TestData[totalRSSIatTestData], 10000000)
		calculatePosition()
		fileName = "ResultPos" + str(TestDataPosition[0]) + ".png"
		print fileName
		saveFigure(fileName)
		clearFigure()



#drawCircle(10,10,2.0,1.0)

#AP1
#a = -2.985
#b = -15.33
#AP2
#a = -2.092
#b = -9.71
#AP3
#a = -2.446
#b = -11.85
#AP4
#a = -2.494
#b = -13.76

#habis semua perhitungan selesai baru gunakan perintah ini
#plt.show()
