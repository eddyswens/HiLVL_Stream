import cv2
import numpy as np
from CamClass import Camera
import Config
from DroneClass import Drone


cam1 = Camera(1080, 1920, Config.RTSP_URL_1, Config.CamSetsFile)

# cam1.Calibration()
cam1.get_new_Rvec_Tvec()

drone = Drone()
while True:
    x, y, z = drone.pos[0][0]
    frame = cam1.get_undist_frame()
    cam1.draw_circle(frame, x, y, z)
    cv2.imshow('Test_fly', frame)

    if cv2.waitKey(1) & 0xFF == ord('x'):
        cv2.destroyAllWindows()
        break
