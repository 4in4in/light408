
import Adafruit_PCA9685
# from app.classes import DUMMY_PCA9685 as Adafruit_PCA9685

import time
import json
from app.classes.lamp import Lamp

class LampController:

    stop_thread = False

    pwms = {
        0: Adafruit_PCA9685.PCA9685(0x40),
        1: Adafruit_PCA9685.PCA9685(0x41)
    }

    def __init__(self) -> None:
        self.modes_list = self.load_config('modes.json')
        self.lamps_dict = self.create_lamps_dict()

    def create_lamps_dict(self):
        lamps_dict = {}
        lamps_config = self.load_config('lamps.json')
        lamp_modes = self.load_config('modes.json')

        for lamp_id in lamps_config.keys():
            lamp = Lamp(
                self.pwms[lamps_config[lamp_id]['board_id']],
                lamp_id,
                lamps_config[lamp_id],
                'default',
                lamp_modes['default']) # см. конструктор класса Lamp
            lamps_dict[int(lamp_id)] = lamp

        return lamps_dict # создание словаря, состоящего из экземпляров класса Lamp


    def load_config(self, path):
        with open(path, 'r') as f:
            return json.load(f)

    def get_lamps_ids(self):
        return list(self.lamps_dict.keys())

    def set_lamp_mode(self, lamp_id, mode):
        lamp = self.lamps_dict[lamp_id]
        lamp.set_mode(mode, self.modes_list[mode])

    def set_lamp_mode_all(self, mode):
        for lamp_id in self.lamps_dict.keys():
            self.set_lamp_mode(lamp_id, mode)

    def set_lamp_user_mode(self, lamp_id, cold, warm, pwm_freq):
        self.lamps_dict[lamp_id].set_user_mode(cold, warm, pwm_freq)

    def set_lamp_user_mode_selectively(self, lamp_ids: list, cold, warm, pwm_freq):
        for lamp_id in lamp_ids:
            self.set_lamp_user_mode(lamp_id, cold, warm, pwm_freq)

    def set_lamp_user_mode_all(self, cold, warm, pwm_freq):
        for lamp_id in self.lamps_dict.keys():
            self.set_lamp_user_mode(lamp_id, cold, warm, pwm_freq)

    def set_lamp_mode_all_smooth(self, mode, steps=40, lamps_ids=None):
        print('set_lamp_mode_all_smooth')
        time.sleep(0.3)
        self.stop_thread = False
        # steps = 40
        target_cold = self.modes_list[mode]['cold']
        target_warm = self.modes_list[mode]['warm']
        target_pwm = self.modes_list[mode]['pwm_freq']

        current_cold = self.lamps_dict[1].current_cold
        current_warm = self.lamps_dict[1].current_warm

        step_cold = (int(target_cold) - int(current_cold)) / steps
        step_warm = (int(target_warm) - int(current_warm)) / steps

        for i in range(steps):
            current_cold += step_cold
            current_warm += step_warm
            if not lamps_ids:
                lamps_ids = self.get_lamps_ids()

            self.set_lamp_user_mode_selectively(lamps_ids, current_cold, current_warm, target_pwm)
            print(current_cold, current_warm)
            time.sleep(0.1)
            if self.stop_thread:
                return

        self.set_lamp_mode_all(mode)

    def demo(self):
        print('demo')
        self.set_mode_all('off')
        lamps_order = [1, 3, 5, 7, 9, 11, 10, 8, 6, 4, 2]
        for i in range(len(lamps_order)):
            self.set_lamp_mode(lamps_order[i-2], 'off')
            time.sleep(0.125)
            self.set_lamp_mode(lamps_order[i-1], 'default')
            time.sleep(0.25)
            self.set_lamp_mode(lamps_order[i], 'default')
            time.sleep(0.25)
            if self.stop_thread:
                return

    def smooth_off_all(self):
        self.set_lamp_mode_all_smooth('off', steps=100)

    def smooth_on_all(self):
        self.set_lamp_mode_all_smooth('default', steps=100)

    def gradient_projector(self):
        lamps_ids = self.get_lamps_ids()
        current = 4095
        for i in range(0, len(self.lamps_dict), 2):
            self.lamps_dict[lamps_ids[i]].set_user_mode(current, current, 1000)
            self.lamps_dict[lamps_ids[i+1]].set_user_mode(current, current, 1000)
            current -= 3600/5

    def gradient_demo(self):
        lamps_ids = self.get_lamps_ids()
        current_cold = 0
        current_warm = 3500
        for i in range(0, len(self.lamps_dict), 2):
            self.lamps_dict[lamps_ids[i]].set_user_mode(current_cold, current_warm, 1000)
            self.lamps_dict[lamps_ids[i+1]].set_user_mode(current_cold, current_warm, 1000)
            current_cold += 3500/5
            current_warm -= 3500/5

    def pairs_on(self, mode):
        lamps_ids = self.get_lamps_ids()
        for i in range(0, len(self.lamps_dict), 2):
            self.set_lamp_mode_all_smooth(mode, 40, [lamps_ids[i], lamps_ids[i+1]])
            if self.stop_thread:
                return


            
if __name__ == '__main__':
    controller = LampController()


