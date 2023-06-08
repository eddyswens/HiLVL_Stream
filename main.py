import cv2
from CamClass import Camera
import Config
import DroneClass
import logging

main_logger = logging.getLogger(__name__)
main_logger.setLevel(logging.INFO)
# настройка обработчика и форматировщика для logger2
ml_handler = logging.FileHandler(f"{__name__}.log", mode='w')
ml_formater = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
# добавление форматировщика к обработчику
ml_handler.setFormatter(ml_formater)
# добавление обработчика к логгеру
main_logger.addHandler(ml_handler)
main_logger.info(f"Checking logger for module {__name__}...")

try:
    cam1 = Camera(720, 1280, Config.RTSP_URL_1, Config.CamSetsFile)
except:
    main_logger.error("Error while initing new cam")
    raise SystemExit
else:
    main_logger.info("Cam 1 init success")

# cam1.Calibration()
# cam1.get_new_rvec_tvec()


if __name__ == '__main__':
    if Config.SIMULATION_ENABLE:
        main_logger.info("Simulation is active now")
        drone = DroneClass.Drone()
        while True:
            x, y, z = drone.pos[0][0]
            frame = cam1.get_undist_frame()
            cam1.draw_circle(frame, x, y, z - 0.15)
            cv2.imshow('Test_fly', frame)

            if cv2.waitKey(1) & 0xFF == ord('x'):
                main_logger.info("Closed by user (Pressed 'x')")
                cv2.destroyAllWindows()
                break

    else:
        main_logger.info("Real drone is active now")
        while True:
            x, y, z = DroneClass.get_pos()
            frame = cam1.get_undist_frame()
            cam1.draw_circle(x, y, z - 0.15, frame)
            cv2.imshow('Test_fly', frame)

            if cv2.waitKey(1) & 0xFF == ord('x'):
                main_logger.info("Closed by user (Pressed 'x')")
                cv2.destroyAllWindows()
                break
