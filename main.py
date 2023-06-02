import cv2
from CamClass import Camera
import Config
import DroneClass


cam1 = Camera(720, 1280, Config.RTSP_URL_1, Config.CamSetsFile)

# cam1.Calibration()
cam1.get_new_rvec_tvec()

if Config.SIMULATION_ENABLE:
    drone = DroneClass.Drone()
    while True:
        x, y, z = drone.pos[0][0]
        frame = cam1.get_undist_frame()
        cam1.draw_circle(frame, x, y, z - 0.15)
        cv2.imshow('Test_fly', frame)

        if cv2.waitKey(1) & 0xFF == ord('x'):
            cv2.destroyAllWindows()
            break

else:
    while True:
        x, y, z = DroneClass.get_pos()
        frame = cam1.get_undist_frame()
        cam1.draw_circle(frame, x, y, z-0.15)
        cv2.imshow('Test_fly', frame)

        if cv2.waitKey(1) & 0xFF == ord('x'):
            cv2.destroyAllWindows()
            break