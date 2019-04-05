#!/usr/bin/env python
#import matplotlib.pyplot as plt
from mpu9250 import mpu9250
from time import time


def take_sample(sample_time, name):
    ##Write to CSV
    
    imu = mpu9250(mpu_addr=0x69)
    import csv
     
    #ifile  = open('test.csv', "rb")
    #reader = csv.reader(ifile)
    ofile  = open(name, "wb")
    write  = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)


    ##Loop to execute IMU data read
    starttime   =  time()*1000
    output_data = []
    while time()*1000 - starttime < sample_time * 1000:
            try:
                    a = imu.accel
                    accelerometer_data = list(a)
                    output_data.append(accelerometer_data)
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
    ofile.close()
    return output_data

