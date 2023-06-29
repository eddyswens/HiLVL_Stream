import json
from flask import Flask, request, jsonify
import requests
import Config
from main import cam1
import time
from Server_Info_Class import json_pars
from Calculated_info_Class import Points
import threading
import logging


server_logger = logging.getLogger(__name__)
server_logger.setLevel(logging.INFO)
# настройка обработчика и форматировщика для server_logger
sl_handler = logging.FileHandler(f"Server{__name__}.log", mode='w')
sl_formater = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
# добавление форматировщика к обработчику
sl_handler.setFormatter(sl_formater)
# добавление обработчика к логгеру
server_logger.addHandler(sl_handler)
server_logger.info(f"Checking logger for module {__name__}...")

# Создание приложения Flask
app = Flask(__name__)

# Создание объекта для хранения координат для передачи
circle_points = Points()
player_id = 0


def get_new_pos():
    global player_id  # Временная вариация по разным pos
    if player_id < 8:
        player_id += 1
    else:
        player_id = 0

    try:
        # r = requests.get(Config.GAME_SERVER_URL, Config.ARGS_FOR_GAME_SERVER)  # Получать позицию с игрового сервера
        r = requests.get(Config.URL_GET)  # Получать позицию с симуляции игрового сервера
        players_pos = json_pars(r.json())
        return players_pos[str(player_id)]

    except requests.exceptions.RequestException as e:
        server_logger.error('Error while getting pos from game server:', e)


def calculate_circle():
    while True:
        try:
            x, y, z, _ = get_new_pos()  # Последний параметр - рыскание
            # x, y, z = DroneClass.get_pos()
            circle_points.data = cam1.draw_circle(x, y, z)
        except TypeError:
            server_logger.error('Error in calculating circle')


th2 = threading.Thread(target=calculate_circle, daemon=True)


@app.post('/')
def post_handler():
    server_logger.info('New POST request')

    request_data = (json.loads(request.get_data()))
    list_of_points = request_data['points']
    need_to_calibrate = request_data['calibrate']

    if need_to_calibrate:
        if cam1.get_new_rvec_tvec(arr2d=list_of_points):
            server_logger.info('New RVEC n TVEC calculated!')
        else:
            server_logger.error('Error while calculating new RVEC n TVEC')

    response = jsonify("Success!")
    response.headers.add("Access-Control-Allow-Origin", '*')
    return response


@app.route('/', methods=["OPTIONS"])  # Заголовки для CORS
def options_handler():
    response = jsonify()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET"
    return response


@app.get('/')
def get_handler():
    server_logger.info('New GET request')
    points = request.args.get('points')
    response = jsonify()
    if points == "1":
        response = jsonify(circle_points.get_data())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


th2.start()

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=False, port=5000)

# Выяснено, что при активном дебагере фласка поток запускается дважды и ему похеру на все