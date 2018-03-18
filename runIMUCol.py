from dronekit import connect, VehicleMode
from my_vehicle import MyVehicle
from time import sleep
import cv2
import numpy as np
def getFreq(time_prev, timestamp ):
    time_current = timestamp  # Get the timestamp at the time the image was captured
    freq = 1.0*10**9/(time_current - time_prev)
    time_prev = time_current
    return time_prev, freq

def main():
    connection_string = '/dev/ttyACM0'
    print("Connecting to vehicle on: %s" % (connection_string))
    vehicle = connect(connection_string, wait_ready=True, vehicle_class=MyVehicle)

    time_prev, time_current, time_bias = 0,0,0
    key = ' '
    file = open("Data/0_accbias.txt", "w")

    index = 0.0
    imu_time, prev_imu_time = 0, 0
    accum_acc = np.array([0,0,0])
    acc_bias = np.zeros_like(accum_acc)
    DIFF_us = 10**6/10
    cv2.namedWindow('dd')
    print ("calculating g_acc")
    for i in range(0,5000):
        acc_bias = acc_bias + np.array([vehicle.raw_imu.xacc, vehicle.raw_imu.yacc, vehicle.raw_imu.zacc])

    acc_bias /= 5000
    file.write("%.4f %.4f %.4f \n" %(acc_bias[0], acc_bias[1], acc_bias[2]))
    file.close()
    print ("acc_bias: ")
    print (acc_bias)

    gpsFlag = 1
    cnt = 0
    file = open("Data/0_data.txt", "w")
    while key != 113:
        key = cv2.waitKey(1)
        imu_time = vehicle.raw_imu.time_boot_us
        diff_us = abs(imu_time - prev_imu_time)

        if diff_us - DIFF_us >= 0:
            #time_prev, freq = getFreq(time_prev, vehicle.raw_imu.time_boot_us)
            prev_gps = np.array([0.0,0.0,0.0])
            current_gps = np.array([vehicle.location._lat, vehicle.location._lon])
            if current_gps == prev_gps:
                flag = 1
            else:
                flag = 0
            if (index > 0):
                file.write("%s %s %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f\n" %
                            # (1/freq,
                            (flag, diff_us,
                            vehicle.location._lat, vehicle.location._lon, vehicle.location._relative_alt,
                            vehicle.attitude.roll, vehicle.attitude.pitch, vehicle.attitude.yaw,
                            vehicle._pitchspeed, vehicle._rollspeed, vehicle._yawspeed,
                            accum_acc[0]/index, accum_acc[1]/index, accum_acc[2]/index,
                            vehicle.raw_imu.xgyro, vehicle.raw_imu.ygyro, vehicle.raw_imu.zgyro,
                            vehicle.raw_imu.xmag, vehicle.raw_imu.ymag, vehicle.raw_imu.zmag))
            prev_gps = current_gps
            index = 0
            accum_acc = np.array([0,0,0])
            prev_imu_time = imu_time
        else:
            accum_acc = accum_acc + np.array([vehicle.raw_imu.xacc, vehicle.raw_imu.yacc, vehicle.raw_imu.zacc])
            #print (accum_acc)
            index +=1

        #print (index)


    cv2.destroyAllWindows()
    file.close()

if __name__ == "__main__":
    main()
