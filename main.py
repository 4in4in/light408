# from app import fl_app

from app import control as ctrl
from app import jalyuzi

from flask import Flask, request
from threading import Thread

app = Flask(__name__, template_folder='app/templates')

lamp_controller = ctrl.LampController()
jal_controller = jalyuzi.JalController()

target_modes = {
    'smooth_off_all': lamp_controller.smooth_off_all,
    'gradient_projector': lamp_controller.gradient_projector,
    'gradient_demo': lamp_controller.gradient_demo,
}

@app.route('/set_mode_bot', methods=['GET'])
def set_mode_bot():
    args = request.json
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
        th = Thread(target=lamp_controller.set_lamp_mode_all_smooth, args=['mode'])
        th.start()    

    print(args['mode'])
    return args['mode']

if __name__ == "__main__":
    try:
        app.run(port=5000, host='0.0.0.0')
    finally:
        # lamp_controller.set_lamp_mode_all('default')
        jal_controller.leave()
