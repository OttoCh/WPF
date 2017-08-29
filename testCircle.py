import math
import matplotlib
matplotlib.use('Agg')

import os.path
import matplotlib.pyplot as plt
import numpy as np
import itertools as itertools
import pylab as pylab
from numpy import *

def findCircleIntersection(x1,x2,y1,y2,r1,r2):
	#persamaan dari online
	#k1 = (rCircle[circ1]**2 - rCircle[circ2]**2) - (originAP[circ1][0]**2 - originAP[circ2][0]**2) - (originAP[circ1][1]**2 - originAP[circ2][1]**2)
	#k2 = -1*2*(originAP[circ1][1]-originAP[circ2][1])
	#k3 = 2*(originAP[circ1][0]-originAP[circ2][0])
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
		print(str(a) + " " + str(b) + " " + str(c))
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
		print(str(a) + " " + str(b) + " " + str(c))
		inside = b**2-4*a*c
		if(inside>=0):
			yIntersect2 = (-b+math.sqrt(b**2-4*a*c))/(2*a)
			yIntersect1 = (-b-math.sqrt(b**2-4*a*c))/(2*a)
	else:
		k1 = x1**2 - x2**2 + y1**2 - y2**2 - r1**2 + r2**2
		k2 = -k1/(2*(x2-x1))
		k3 = (y2-y1)/(x2-x1)
		k4 = k2-x1
		print(str(k1) + " " + str(k2) + " " + str(k3) + " " + str(k4))
		a = (k3**2+1)
		b = (-2*k3*k4 - 2*y1)
		c = k4**2 + y1**2 - r1**2
		#k1 = ((r2**2-r1**2)+y1**2-y2**2+x1**2-x2**2)/(2*(x1-x2))
		#a = ((y1-y2)**2)/((x1-x2)**2)+1
		#b = ((-2*(y1-y2)/(x1-x2))*(x1-k1) - 2*y1)
		#c = (k1-x1)**2 + y1**2 - r1**2
		print(str(a) + " " + str(b) + " " + str(c))
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
	drawIntersectionCoordinateToPlot(xIntersect1, yIntersect1)
	drawIntersectionCoordinateToPlot(xIntersect2, yIntersect2)
	print xIntersect1
	print xIntersect2
	print yIntersect1
	print yIntersect2

def drawCircle(originPoint_X, originPoint_Y, r_inner, r_outer):
	n = 50
	drawRange = np.linspace(r_inner, r_outer, n, endpoint=True)
	for i in drawRange:
		ax.axis("equal")
		circ = plt.Circle((originPoint_X,originPoint_Y), radius=i, color='r', alpha=0.1, fill=False)
		ax.add_patch(circ)

def saveFigure(filename):
	pylab.savefig(filename, bbox_inches='tight')

def drawIntersectionCoordinateToPlot(x,y):
	xWrite = x+0.2
	yWrite = y-0.2
	x = format(round(x,2))
	y = format(round(y,2))
	coorStr = '(' + str(x) + ',' + str(y) + ')'
	#plt.Text(x-1.0,y-1.0,coorStr, fontsize=15)
	bx = plt.gca()
	bx.annotate(coorStr, xy=(xWrite, yWrite))
	circ = plt.Circle((x,y), radius=0.02, color='k', alpha=1, fill=True)
	ax.add_patch(circ)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
x1 = 0.0
y1 = 1.0
x2 = 1.0
y2 = -1.0
r1 = 2.0
r2 = 2.0
findCircleIntersection(x1, x2, y1, y2, r1, r2)
drawCircle(x1,y1,r1, r1+0.02)
drawCircle(x2,y2,r2, r2+0.02)
drawIntersectionCoordinateToPlot(1.983,0.7416)
drawIntersectionCoordinateToPlot(-0.9832,-0.7416)
#ax.set_xlim((0,27))
#ax.set_ylim((0,12))
ax.set_xlim((-5,5))
ax.set_ylim((-5,5))
fileName = "testCircle.png"
saveFigure(fileName)



