import Adafruit_PCA9685

class Lamp:

    def __init__(self, new_pwm, lamp_id, pins_config, mode_name, mode_params):
        self.pwm = new_pwm
        self.lamp_id = lamp_id
        self.pins = { "cold": pins_config['cold_pin'], "warm": pins_config['warm_pin'] }
        self.set_mode(mode_name, mode_params)

    def apply_params(self):
        self.pwm.set_pwm_freq(self.current_pwm_freq) # задание частоты ШИМ
        self.pwm.set_pwm(self.pins['cold'], 0, self.current_cold) # задание скважности для холодного света
        self.pwm.set_pwm(self.pins['warm'], 0, self.current_warm) # задание скважности для теплого света

    def set_user_mode(self, cold, warm, pwm_freq):  # задел на будущее - возможность вручную регулировать параметры света
        self.params = { 'cold': cold, 'warm': warm, 'pwm_freq': pwm_freq }
        self.set_mode('user', params)  

    def set_mode(self, mode, params):  # запись значений параметров светильника в переменные класса
        self.current_mode = mode
        self.current_cold = int(params['cold'])
        self.current_warm = int(params['warm'])
        self.current_pwm_freq = int(params['pwm_freq'])
        self.apply_params()

