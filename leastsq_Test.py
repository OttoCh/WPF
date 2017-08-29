import matplotlib.pyplot as plt

from numpy import *
from scipy.optimize import leastsq

#Ini adalah data yang kita miliki, atau posisi dari AP dan radius dari AP! artinya ini didapatkan dari persamaan milik kita.
points = [ (-1.91373, -0.799904, 2.04001), (-0.935453, -0.493735, 0.959304), (0.630964, -0.653075, 0.728477), (0.310857, -0.018258, 0.301885), (0.0431084, 1.25321, 1.19012) ]

#ini adalah bagian untuk menjadi residual, radius tebakan - radius eksperimen
def residuals(point, data):
	#d = sqrt( square(data[0] - point[0]) + square(data[1] - point[1]) ) * data[2]
	d = sqrt(square(data[0]-point[0])+square(data[1]-point[1]))-data[2]
	return d
#nilai awal dari x0 dan y0
p0 = [0, 0]
#one function to rule them all
args = (points)
print args
plsq = leastsq(residuals, p0, args=(points))
#posisi akhir dari x0 dan y0 (posisi alat kita)
print plsq[0]

#hanya plotting saja
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_xlim((-3,3))
ax.set_ylim((-3,3))

# Plot section
for p in points:
	circ = plt.Circle((p[0], p[1]), radius=p[2], color='b', alpha=0.5)
	circ2 = plt.Circle((p[0], p[1]), radius=0.01, color='r', alpha=1)
	ax.add_patch(circ)
	ax.add_patch(circ2)

circ = plt.Circle(plsq[0], radius=0.1, color='g', alpha=0.8)
ax.add_patch(circ)
plt.show()
