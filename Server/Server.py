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
    global player_id  # Временная вариация по разным pos
    if player_id < 8:
        player_id += 1
    else:
        player_id = 0
    try:
        r = requests.get(Config.GAME_SERVER_URL, Config.ARGS_FOR_GAME_SERVER)
        players_pos = json_pars(r.json())
        return players_pos[str(player_id)]

    except requests.exceptions.RequestException as e:
        print('Error while getting data from the game server:', e)


def calculate_pos():
    count = 0
    while True:
        print (count)
        count += 1
        try:
            x, y, z, _ = get_new_points()
            circle_points.data = cam1.draw_circle(x, y, z)
        except TypeError:
            print('Error in calculating positions.')
        # time.sleep(0.005)

# th2 = threading.Thread(target=calculate_pos)
# th2.start()


@app.post('/')
def post_handler():
    request_data = request.get_json()
    list_of_points = request_data['points']
    need_to_calibrate = request_data['calibrate']
    if need_to_calibrate:
        cam1.calibration(imgpoints=list_of_points)
    if list_of_points:
        return jsonify("Succes!")


@app.get('/')
def get_handler():
    points = request.args.get('points')
    if points == "1":
        return jsonify(circle_points.get_data())
    return jsonify("No points for u")


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)


# TODO: Разобраться с потоками, почему то запускается calculate_pos два раза pizdec