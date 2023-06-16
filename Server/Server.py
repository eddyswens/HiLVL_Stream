import json
from flask import Flask, request, jsonify
import requests
import Config
from main import cam1
import time
from Server_Info import json_pars
from Calculated_info import Points
import threading


# create the Flask app
app = Flask(__name__)
circle_points = Points()
player_id = 0


def get_new_points():
    # global player_id  # Временная вариация по разным pos
    # if player_id < 8:
    #     player_id += 1
    # else:
    #     player_id = 0

    player_id = 1
    try:
        r = requests.get(Config.GAME_SERVER_URL, Config.ARGS_FOR_GAME_SERVER)
        # r = requests.get(Config.URL_GET)
        players_pos = json_pars(r.json())
        return players_pos[str(player_id)]

    except requests.exceptions.RequestException as e:
        print('Error while getting data from the game server:', e)


def calculate_pos():
    while True:
        try:
            x, y, z, _ = get_new_points()
            print(x, y, z)
            # x, y, z = DroneClass.get_pos()
            circle_points.data = cam1.draw_circle(x, y, z)
        except TypeError:
            print('Error in calculating positions.')
        time.sleep(0.005)


th2 = threading.Thread(target=calculate_pos, daemon=True)


@app.post('/')
def post_handler():
    request_data = (json.loads(request.get_data()))
    print(request_data)
    list_of_points = request_data['points']
    need_to_calibrate = request_data['calibrate']
    print("parsed")
    if need_to_calibrate:
        if cam1.get_new_rvec_tvec(arr2d=list_of_points):
            print('New RVEC n TVEC calculated!')
        else:
            print('Error while calculating new RVEC n TVEC')
    response = jsonify("Success!")
    response.headers.add("Access-Control-Allow-Origin", '*')
    return response


@app.route('/', methods=["OPTIONS"])
def options_handler():
    response = jsonify()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET"
    return response


@app.get('/')
def get_handler():
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