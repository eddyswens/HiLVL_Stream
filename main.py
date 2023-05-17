import cv2
import numpy as np

from CamClass import Camera
import Config


cam1 = Camera(1080, 1920, Config.RTSP_URL_1, Config.CamSetsFile)

# if Config.CALIBRATION_ENABLE:
#     Calibration.start(Config.NUMBER_OF_SHOTS)

# cam1.Calibration()
cam1.get_new_Rvec_Tvec()

# if Config.GET_RVEC_TVEC_ENABLE:
#     getRvecTvec.start_scan()

while True:
    cv2.imshow('After undistort', cam1.get_undist_frame())

    if cv2.waitKey(1) & 0xFF == ord('x'):
        cv2.destroyAllWindows()
        break
