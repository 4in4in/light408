# from app import fl_app

from app import control as ctrl
from app import jalyuzi

from flask import Flask, request, render_template
from threading import Thread

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

lamp_controller = ctrl.LampController()
jal_controller = jalyuzi.JalController()

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
    print(args)
    target_mode = args['mode']

    # Лампы #

    if target_mode == 'smooth_off_all':
        th = Thread(target=lamp_controller.smooth_off_all)
        th.start()
    elif target_mode == 'gradient_projector':
        th = Thread(target=lamp_controller.gradient_projector)
        th.start()
    elif target_mode == 'gradient_demo':
        th = Thread(target=lamp_controller.gradient_demo)
        th.start()
    elif target_mode == 'demo':
        th = Thread(target=lamp_controller.demo)
        th.start()
    elif target_mode == 'pairs_on':
        th = Thread(target=lamp_controller.pairs_on, args=['default'])
        th.start()
    elif target_mode == 'smooth_on_all':
        th = Thread(target=lamp_controller.smooth_on_all, args=['default'])
        th.start()      

    # Жалюзи #
    elif target_mode == 'jal1_up':
        jal_controller.move(1, 'up')
    elif target_mode == 'jal1_down':
        jal_controller.move(1, 'down')
    elif target_mode == 'jal1_stop':
        jal_controller.stop(1)
    elif target_mode == 'jal1_open_up':
        jal_controller.turn_up(1, 'up')
    elif target_mode == 'jal1_open_down':
        jal_controller.turn_up(1, 'down')
    elif target_mode == 'jal2_up':
        jal_controller.move(2, 'up')
    elif target_mode == 'jal2_down':
        jal_controller.move(2, 'down')
    elif target_mode == 'jal2_stop':
        jal_controller.stop(2)
    elif target_mode == 'jal2_open_up':
        jal_controller.turn_up(2, 'up')
    elif target_mode == 'jal2_open_down':
        jal_controller.turn_up(2, 'down')
    else:
        # lamp_controller.set_lamp_mode_all(args['mode'])
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
