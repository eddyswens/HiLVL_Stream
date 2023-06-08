
CALIBRATION_ENABLE = 0
NUMBER_OF_SHOTS = 5
BOARD_SIZE = (6, 9)

GET_RVEC_TVEC_ENABLE = 1
POINTS = 6

# Парметры кольца:
RAD = 0.2 # Радиус кольца
NUM_POINTS = 36 # Количество точек на кольце

SIMULATION_ENABLE = 1

CAM1 = "rtsp://drom:DRom2022@10.10.33.19:554"
CAM2 = 'rtsp://drom:DRom2022@10.10.33.22:554'
CAM3 = 'rtsp://drom:DRom2022@10.10.33.13:554'

RTSP_URL_1 = 'rtsp://admin:12345678eE@169.254.41.224:554/h264Preview_01_main'
CamSetsFile = '/home/eddyswens/PycharmProjects/HiLVL_Stream/Camera_Settings.data'


#Servers

URL_GET = 'http://127.0.0.1:4000/?target=get&type_command=player&command=visualization&param=0'

GAME_SERVER_URL = 'http://127.0.0.1:4000/'
ARGS_FOR_GAME_SERVER = {'target': 'get',
                  'type_command': 'player',
                  'command': 'visualization',
                  'param': '0'}