import matplotlib.pyplot as plt
import numpy as np

import csv
 
ifile  = open('sammysecret.csv', "rb")
reader = csv.reader(ifile)

xdata = []
ydata = []
zdata = []
tdata = []
t=0.0

for row in reader:
   x, y, z = row
   xdata.append(float(x))
   ydata.append(float(y))
   zdata.append(float(z)-1.0)
   tdata.append(t/575.0)
   t += 1.0

plt.scatter(tdata, zdata, color='g')
plt.scatter(tdata, xdata, color='b')
plt.scatter(tdata, ydata, color='r')
plt.show()