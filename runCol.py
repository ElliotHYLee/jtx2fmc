import pyzed.camera as zcam
import pyzed.defines as sl
import pyzed.types as tp
import pyzed.core as core
import cv2
from dronekit import connect, VehicleMode
from my_vehicle import MyVehicle

def initZed(fps):
    # Create a PyZEDCamera object
    zed = zcam.PyZEDCamera()
    # Create a PyInitParameters object and set configuration parameters
    init_params = zcam.PyInitParameters()
    init_params.camera_resolution = sl.PyRESOLUTION.PyRESOLUTION_HD1080  # Use HD1080 video mode
    init_params.camera_fps = fps  # Set fps at 30

    # Use a right-handed Y-up coordinate system
    init_params.coordinate_system = sl.PyCOORDINATE_SYSTEM.PyCOORDINATE_SYSTEM_RIGHT_HANDED_Y_UP
    init_params.coordinate_units = sl.PyUNIT.PyUNIT_METER  # Set units in meters

    # Open the camera
    err = zed.open(init_params)
    if err != tp.PyERROR_CODE.PySUCCESS:
        exit(1)

    # Enable positional tracking with default parameters
    py_transform = core.PyTransform()  # First create a PyTransform object for PyTrackingParameters object
    tracking_parameters = zcam.PyTrackingParameters(init_pos=py_transform)
    err = zed.enable_tracking(tracking_parameters)
    if err != tp.PyERROR_CODE.PySUCCESS:
        exit(1)

    image = core.PyMat()
    zed_pose = zcam.PyPose()
    return zed, image, zed_pose

def getFreq(time_prev, timestamp ):
    time_current = timestamp  # Get the timestamp at the time the image was captured
    freq = 1.0*10**9/(time_current - time_prev)
    time_prev = time_current
    return time_prev, freq

def getPos(zed_pose, py_translation):
    tx = round(zed_pose.get_translation(py_translation).get()[0], 3)
    ty = round(zed_pose.get_translation(py_translation).get()[1], 3)
    tz = round(zed_pose.get_translation(py_translation).get()[2], 3)
    return tx, ty, tz

def main():
    connection_string = '/dev/ttyACM0'
    print("Connecting to vehicle on: %s" % (connection_string))
    vehicle = connect(connection_string, wait_ready=True, vehicle_class=MyVehicle)

    zed, image, zed_pose = initZed(30)
    index, time_prev, time_current, time_bias = 0,0,0,0
    key = ' '
    file = open("Data/data.txt", "w")
    while key != 113:
        if zed.grab(zcam.PyRuntimeParameters()) == tp.PyERROR_CODE.PySUCCESS:
            if index%3==0:
                zed.get_position(zed_pose, sl.PyREFERENCE_FRAME.PyREFERENCE_FRAME_WORLD)
                tx, ty, tz = getPos(zed_pose, core.PyTranslation())

                zed.retrieve_image(image, sl.PyVIEW.PyVIEW_LEFT)
                img = image.get_data()[:,:,0:3]
                cv2.imshow('dd', img )
                key = cv2.waitKey(1)
                cv2.imwrite('Data/'+str(index)+'.jpg', img)

                time_prev, freq = getFreq(time_prev, zed.get_camera_timestamp())
                file.write("%f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f\n" %
                    (1/freq,
                    tx,ty,tz,
                    vehicle.location._lat, vehicle.location._lon, vehicle.location._relative_alt,
                    vehicle.attitude.roll, vehicle.attitude.pitch, vehicle.attitude.yaw,
                    vehicle._pitchspeed, vehicle._rollspeed, vehicle._yawspeed,
                    vehicle.raw_imu.xacc, vehicle.raw_imu.yacc, vehicle.raw_imu.zacc,
                    vehicle.raw_imu.xgyro, vehicle.raw_imu.ygyro, vehicle.raw_imu.zgyro,
                    vehicle.raw_imu.xmag, vehicle.raw_imu.ymag, vehicle.raw_imu.zmag))
            index +=1

    cv2.destroyAllWindows()
    file.close()
    zed.close()

if __name__ == "__main__":
    main()
