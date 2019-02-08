#!/usr/bin/env python
#import matplotlib.pyplot as plt
from mpu9250 import mpu9250
from time import sleep
from time import time

imu = mpu9250(mpu_addr=0x69)

##Write to CSV
import csv
 
#ifile  = open('test.csv', "rb")
#reader = csv.reader(ifile)
ofile  = open('test.csv', "wb")
write  = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)


##Loop to execute IMU data read
starttime =  time()*1000
while time()*1000 - starttime < 10000:
	try:
		a = imu.accel
                accelerometer_data = list(a)
                print accelerometer_data
		# print 'Accel: {:.3f} {:.3f} {:.3f} mg'.format(*a)
		# g = imu.gyro
		# print 'Gyro: {:.3f} {:.3f} {:.3f} dps'.format(*g)
		# m = imu.mag
		# print 'Magnet: {:.3f} {:.3f} {:.3f} mT'.format(*m)
		#m = imu.temp
                #print 'Temperature: {:.3f} C'.format(m * 9.0/5.0 + 32.)
		write.writerow(accelerometer_data)
	except KeyboardInterrupt:
		print 'bye ...'
print('Hurray I Finished')
#ifile.close()
ofile.close()

#testing matplotlib
#plt.plot([1,2,3],[4,6,8])
#plt.show()
