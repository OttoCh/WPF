#PythonGraph
#tidak bisa from vpython
##MAKE BALL ANIMATION
from visual import *
floor = box (pos=(0,0,0), length=4, height=0.5, width=4, color=color.blue)
ball = sphere (pos=(0,4,0), radius=1, color=color.red)
ball.velocity = vector(0,-1,0)
dt = 0.01
while 1:
    rate (100)
    ball.pos = ball.pos + ball.velocity*dt
    if ball.y < ball.radius:
        ball.velocity.y = abs(ball.velocity.y)
    else:
        ball.velocity.y = ball.velocity.y - 9.8*dt

#MAKE GRAPH 2D
#from visual import * # must import visual or vis first
#from visual.graph import *	# import graphing features 
#
#f1 = gcurve(color=color.red)	# a graphics curve
#for x in arange(0, 8.05, 0.1):	# x goes from 0 to 8
#    f1.plot(pos=(x,5*cos(2*x)*exp(-0.2*x)))	# plot