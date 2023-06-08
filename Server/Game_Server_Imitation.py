from flask import Flask, request

# create the Flask app
app = Flask(__name__)

@app.route('/', methods=['GET'])
def game_info():
    target = request.args.get('target')
    type_com = request.args.get('type_command')
    com = request.args.get('command')
    param = request.args.get('param')

    with open('Test_JSON.json', 'r') as file:
        json_data = file.read()
    return json_data


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=4000)
