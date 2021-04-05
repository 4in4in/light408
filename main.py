# from app import fl_app

from app import control as ctrl
from app import jalyuzi

from flask import Flask, render_template, request
from time import sleep
from threading import Thread

app = Flask(__name__, template_folder='app/templates')

lamp_controller = ctrl.LampController()
jal_controller = jalyuzi.JalController()

modes_keys = lamp_controller.modes_list.keys()
modes = lamp_controller.modes_list
lamps = lamp_controller.lamps_dict
selected_mode = list(modes_keys)[0]

@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    return render_template('index.html', modes_keys=modes_keys, modes=modes, selected_mode=selected_mode)

@app.route('/set_mode', methods=["POST"])
def set_mode():
    selected_mode = request.form['mode']
    print(request.form)
    lamp_controller.set_lamp_mode_all(selected_mode)
    print(selected_mode)
    return render_template('index.html', selected_mode=selected_mode, modes_keys=modes_keys, modes=modes)

@app.route('/smooth_off', methods=["POST"])
def smooth_off():
    lamp_controller.smooth_off_all()
    return render_template('index.html', selected_mode=selected_mode, modes_keys=modes_keys, modes=modes)

@app.route('/smooth_on', methods=["POST"])
def smooth_on():
    lamp_controller.smooth_on_all('default')
    return render_template('index.html', selected_mode=selected_mode, modes_keys=modes_keys, modes=modes)

@app.route('/demo', methods=["POST"])
def demo():
    lamp_controller.demo()
    return render_template('index.html', selected_mode=selected_mode, modes_keys=modes_keys, modes=modes)


@app.route('/set_mode_bot', methods=['GET'])
def set_mode_bot():
    args = request.json
    target_mode = args['mode']

    # Лампы #

    if target_mode == 'smooth_off_all':
        th = Thread(target=lamp_controller.smooth_off_all)
        th.start()
        # lamp_controller.smooth_off_all()
    elif target_mode == 'gradient_projector':
        th = Thread(target=lamp_controller.gradient_projector)
        th.start()
        # lamp_controller.gradient_projector()
    elif target_mode == 'gradient_demo':
        th = Thread(target=lamp_controller.gradient_demo)
        th.start()
        # lamp_controller.gradient_demo()
    elif target_mode == 'demo':
        th = Thread(target=lamp_controller.demo)
        th.start()
        # lamp_controller.demo()
    elif target_mode == 'pairs_on':
        th = Thread(target=lamp_controller.pairs_on, args=['default'])
        th.start()
        # lamp_controller.pairs_on('default')
    elif target_mode == 'smooth_on_all':
        th = Thread(target=lamp_controller.smooth_on_all, args=['default'])
        th.start()
        # lamp_controller.smooth_on_all('default')

    # Жалюзи #
    elif target_mode=='jal1_up':
        jal_controller.move(1, 'up')
    elif target_mode=='jal1_down':
        jal_controller.move(1, 'down')
    elif target_mode=='jal1_stop':
        jal_controller.stop(1)
    elif target_mode=='jal1_open_up':
        jal_controller.turn_up(1, 'up')
    elif target_mode=='jal1_open_down':
        jal_controller.turn_up(1, 'down')
    elif target_mode=='jal2_up':
        jal_controller.move(2, 'up')
    elif target_mode=='jal2_down':
        jal_controller.move(2, 'down')
    elif target_mode=='jal2_stop':
        jal_controller.stop(2)
    elif target_mode=='jal2_open_up':
        jal_controller.turn_up(2, 'up')
    elif target_mode=='jal2_open_down':
        jal_controller.turn_up(2, 'down')
    else:
        lamp_controller.set_lamp_mode_all(args['mode'])
    print(args['mode'])
    return args['mode']

@app.route('/set_jelaousy', methods=["GET"])
def set_jalyuzi():
    args = request.json
    target_mode = args['mode']
    jal_id = int(args['jal_id'])

    if target_mode=='jal_up':
        jal_controller.move(jal_id, 'up')
    elif target_mode=='jal_down':
        jal_controller.move(jal_id, 'down')
    elif target_mode=='jal_stop':
        jal_controller.stop(jal_id)
    elif target_mode=='jal_open_up':
        jal_controller.turn_up(jal_id, 'up')
    elif target_mode=='jal_open_down':
        jal_controller.turn_up(jal_id, 'down')
    else:
        return 'error'
    return str(jal_id) + ' ' + target_mode

if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')
