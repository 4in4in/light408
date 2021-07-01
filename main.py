# from app import fl_app

from app import control1 as ctrl
from app import jalyuzi

from flask import Flask, request, render_template
from threading import Thread

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

lamp_controller = ctrl.LampController()
jal_controller = jalyuzi.JalController()

thread_methods = {
    'smooth_off_all': (lamp_controller.smooth_off_all, []),
    'gradient_projector': (lamp_controller.gradient_projector, []),
    'gradient_demo': (lamp_controller.gradient_demo, []),
    'pairs_on': (lamp_controller.pairs_on, ['default']),
    'smooth_on_all': (lamp_controller.smooth_on_all, ['default']),
    'smooth_off_all': (lamp_controller.smooth_off_all, ['default'])
}

ordinary_methods = {
    'jal1_up': (jal_controller.move, [1, 'up']),
    'jal1_down': (jal_controller.move, [1, 'down']),
    'jal1_stop': (jal_controller.stop, [1]),
    'jal1_open_up': (jal_controller.turn_up, [1, 'up']),
    'jal1_open_down': (jal_controller.turn_up, [1, 'down']),
    'jal2_up': (jal_controller.move, [2, 'up']),
    'jal2_down': (jal_controller.move, [2, 'down']),
    'jal2_stop': (jal_controller.stop, [2]),
    'jal2_open_up': (jal_controller.turn_up, [2, 'up']),
    'jal2_open_down': (jal_controller.turn_up, [2, 'down'])
}

@app.route('/get_modes')
def get_modes():
    return lamp_controller.modes_list

@app.route('/')
def main():
    return render_template('test.html')

@app.route('/check_mode', methods=['GET', 'POST'])
def check_mode():
    args = request.json
    lamp_controller.set_lamp_user_mode_all(args['cold'], args['warm'], args['pwm'])
    print(args)
    return args

@app.route('/create_mode', methods=['GET', 'POST'])
def add_mode():
    args = request.json
    lamp_controller.add_mode(args['name_ru'], args['cold'], args['warm'], args['pwm'])
    return args

@app.route('/set_mode_bot', methods=['GET', 'POST'])
def set_mode_bot():
    args = request.json
    target_mode = args['mode']

    if target_mode in thread_methods.keys():
        method = ordinary_methods[target_mode][0]
        method_args = ordinary_methods[target_mode][1]
        lamp_controller.stop_thread = True
        th = Thread(target=method, args=method_args)
        th.start()
    elif target_mode in ordinary_methods.keys():
        method = ordinary_methods[target_mode][0]
        method_args = ordinary_methods[target_mode][1]
        method(*method_args)
    else:
        lamp_controller.stop_thread = True
        th = Thread(target=lamp_controller.set_lamp_mode_all_smooth, args=[target_mode])
        th.start()

    print(args['mode'])
    return args['mode']

if __name__ == "__main__":
    try:
        app.run(port=5000, host='0.0.0.0')
    finally:
        # lamp_controller.set_lamp_mode_all('default')
        jal_controller.leave()
        # pass
