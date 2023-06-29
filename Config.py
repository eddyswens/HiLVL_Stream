import numpy as np


# Параметры исправления искажения:
CALIBRATION_ENABLE = 0
NUMBER_OF_SHOTS = 5
BOARD_SIZE = (6, 9)

# Параметры переноса 3д точек на 2д изображение:
GET_RVEC_TVEC_ENABLE = 0
POINTS = 6
POINTS_3D = np.array([[[-0.151, -0.237, 0],
                           [-0.161, 2.300, 0],
                           [-3.773, -0.337, 0],
                           [3.133, -0.198, 0],
                           [5.091, 0.354, 1],
                           [-3.395, -2.458, 1]
                           ]], dtype=float)

# Парметры кольца:
RAD = 0.2 # Радиус кольца
NUM_POINTS = 36 # Количество точек на кольце

#DEBUG
SIMULATION_ENABLE = 1
CAM_ENABLE = 0

# Ссылки на камеры:
CAM1 = "rtsp://drom:DRom2022@10.10.33.19:554"
CAM2 = 'rtsp://drom:DRom2022@10.10.33.22:554'
CAM3 = 'rtsp://drom:DRom2022@10.10.33.13:554'

RTSP_URL_1 = 'rtsp://admin:12345678eE@169.254.41.224:554/h264Preview_01_main'

# Ссылка на документ с сохраненными параметрами:
CamSetsFile = '/home/eddyswens/PycharmProjects/HiLVL_Stream/Camera_Settings.data'


# Ссылка запроса на игровой сервер:
URL_GET = 'http://127.0.0.1:4000/?target=get&type_command=player&command=visualization&param=0'  # simulation

GAME_SERVER_URL = 'https://arena.geoscan.aero/game/'  # real game server
ARGS_FOR_GAME_SERVER = {'target': 'get',
                  'type_command': 'player',
                  'command': 'visualization',
                  'param': '0'}