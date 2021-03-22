from app import fl_app
from app import control
from flask import render_template, request

@fl_app.route('/', methods=["GET", "POST"])
@fl_app.route('/index', methods=["GET", "POST"])
def index():
    modes_keys = control.load_lamp_modes().keys()
    modes = control.load_lamp_modes()

    if request.method == "POST":
        selected_mode = request.form['mode']
        control.set_lamp_mode_all(selected_mode)
        print(selected_mode)

    return render_template('index.html', modes_keys=modes_keys, modes=modes)