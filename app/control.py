# В этом файле осуществляется управление светильниками


# from app.classes import DUMMY_PCA9685 as Adafruit_PCA9685

from threading import Lock

import Adafruit_PCA9685
import time

import json
from app.classes.lamp import Lamp # В классе Lamp содержатся основные атрибуты светильника

class LampController:

    stop_thread = False
    lock = Lock()

    def set_thread_state(self, state):
        self.lock.acquire()
        self.stop_thread = state
        self.lock.release()

    pwms = {
        0: Adafruit_PCA9685.PCA9685(0x40),
        1: Adafruit_PCA9685.PCA9685(0x41)
    } # Список плат ШИМ (на одной висит 8 светильников, на второй - 4)

    def __init__(self):
        self.modes_list = self.load_lamp_modes() # загрузка списка режимов работы светильников
        self.lamps_dict = self.create_lamps_dict() # создание словаря, состоящего из экземпляров класса Lamp

    def load_lamps_config(self):
        with open('lamps.json', 'r') as f:
            lamps_config = json.load(f)
            return lamps_config # загрузка конфигурации пинов и номеров плат ШИМ светильников

    def load_lamp_modes(self):
        with open('modes.json', 'r') as f:
            modes = json.load(f)
            return modes # загрузка режимов, в которых могут работать светильники

    def add_mode(self, name_ru, cold, warm, pwm):
        from datetime import datetime
        import os
        internal_name = str(datetime.now().timestamp())
        self.modes_list[internal_name] = {'name_ru':name_ru, 'cold': cold, 'warm': warm, 'pwm_freq': pwm}
        with open('modes.json', 'w') as f:
            json.dump(self.modes_list, f, indent=4, ensure_ascii=False)

    def set_lamp_mode(self, lamp_id, mode):
        self.lamps_dict[lamp_id].set_mode(mode, self.modes_list[mode]) # задать режим работы для светильника с номером lamp_id

    def set_lamp_mode_all(self, mode):
        self.set_thread_state(True)
        time.sleep(0.3)
        for lamp_id in self.lamps_dict.keys():
            self.set_lamp_mode(lamp_id, mode) # задать режим работы для всех светильников
    
    def set_lamp_user_mode(self, lamp_id, cold, warm, pwm_freq):
        self.lamps_dict[lamp_id].set_user_mode(cold, warm, pwm_freq)

    def set_lamp_user_mode_all(self, cold, warm, pwm_freq):
        for lamp_id in self.lamps_dict.keys():
            self.set_lamp_user_mode(lamp_id, cold, warm, pwm_freq) 

    def set_lamp_mode_all_smooth(self, mode):
        self.set_thread_state(True)
        time.sleep(0.3)

        current_cold = self.lamps_dict[1].current_cold
        current_warm = self.lamps_dict[1].current_warm
        new_cold = self.modes_list[mode]['cold']
        new_warm = self.modes_list[mode]['warm']
        new_pwm = self.modes_list[mode]['pwm_freq']
        steps = 40
        step_cold = (int(new_cold) - int(current_cold))/steps
        step_warm = (int(new_warm) - int(current_warm))/steps

        for i in range(steps):
            self.lock.acquire()
            if self.stop_thread is True:
                self.lock.release()
                break
            self.lock.release()
            current_cold += step_cold
            current_warm += step_warm
            self.set_lamp_user_mode_all(current_cold, current_warm, new_pwm)
            time.sleep(0.1)
            print(current_cold, current_warm)

        self.set_lamp_mode_all(mode)
                


    def smooth_off_one(self, lamp_id): # плавное выключение
        curr_lamp_id = lamp_id

        MAX = 3000
        STEP = 200

        curr_cold = self.lamps_dict[curr_lamp_id].current_cold
        curr_warm = self.lamps_dict[curr_lamp_id].current_warm

        while curr_cold < MAX or curr_warm < MAX:
            if curr_cold<MAX:
                curr_cold += int(STEP)
            else:
                curr_cold = 4095
            if curr_warm<MAX:
                curr_warm += int(STEP)
            else:
                curr_warm = 4095

            self.lamps_dict[curr_lamp_id].set_user_mode(curr_cold, curr_warm, 300)
            time.sleep(0.2)
        
        self.set_lamp_mode(1, 'off')


    def smooth_on_one(self, lamp_id, target_mode):
        self.set_lamp_mode(lamp_id, 'off')
        time.sleep(0.5)
        target_cold = int(self.modes_list[target_mode]['cold'])
        target_warm = int(self.modes_list[target_mode]['warm'])
        target_pwm_freq = int(self.modes_list[target_mode]['pwm_freq'])

        curr_cold = 4000
        curr_warm = 4000

        STEP = 30

        while curr_cold > target_cold or curr_warm > target_warm:
            curr_cold -= STEP if curr_cold > target_cold else curr_cold
            curr_warm -= STEP if curr_warm > target_warm else curr_warm
            # if curr_cold > target_cold:
            #     curr_cold -= STEP
            # if curr_warm > target_warm:
            #     curr_warm -= STEP
            self.lamps_dict[lamp_id].set_user_mode(curr_cold, curr_warm, 300)
            # print('lamp_id', lamp_id,  'curr_cold ', curr_cold, 'curr_warm: ', curr_warm)
            time.sleep(0.1)
        self.set_lamp_mode(lamp_id, target_mode)

    #####

    def smooth_off_all(self):
        self.set_thread_state(True)
        time.sleep(0.5)
        self.set_thread_state(False)
        MAX = 4000
        STEP = 225 # было 50

        for lamp_id1, lamp_id2 in zip(range(1, 12, 2), range(2, 12, 2)):
            curr_cold = self.lamps_dict[lamp_id1].current_cold
            curr_warm = self.lamps_dict[lamp_id1].current_warm
            curr_pwm_freq = self.lamps_dict[1].current_pwm_freq

            while (curr_cold < MAX or curr_warm < MAX): # and not self.__stop_mode:
                self.lock.acquire()
                if self.stop_thread is True:
                    self.lock.release()
                    break
                self.lock.release()
                if curr_cold<MAX:
                    curr_cold += int(STEP)
                else:
                    curr_cold = 4095
                if curr_warm<MAX:
                    curr_warm += int(STEP)
                else:
                    curr_warm = 4095
                self.lamps_dict[lamp_id1].set_user_mode(curr_cold, curr_warm, curr_pwm_freq)
                self.lamps_dict[lamp_id2].set_user_mode(curr_cold, curr_warm, curr_pwm_freq)

        self.set_lamp_mode_all('off')
        

    def smooth_on_all_fast(self, target_mode):
        self.set_thread_state(True)
        self.set_lamp_mode_all('off')
        time.sleep(0.5)
        self.set_thread_state(False)
        STEP = 225 # было 50

        target_cold = int(self.modes_list[target_mode]['cold'])
        target_warm = int(self.modes_list[target_mode]['warm'])
        target_pwm_freq = int(self.modes_list[target_mode]['pwm_freq'])

        for lamp_id1, lamp_id2 in zip(range(1, 12, 2), range(2, 12, 2)):
            curr_cold = self.lamps_dict[lamp_id1].current_cold
            curr_warm = self.lamps_dict[lamp_id1].current_warm
            curr_pwm_freq = self.lamps_dict[1].current_pwm_freq

            while (curr_cold > target_cold or curr_warm > target_warm): 
                
                self.lock.acquire()
                if self.stop_thread is True:
                    self.lock.release()
                    break

                if curr_cold>target_cold:
                    curr_cold -= int(STEP)
                else:
                    curr_cold = target_cold
                if curr_warm<target_warm:
                    curr_warm += int(STEP)
                else:
                    curr_warm = target_warm
                self.lamps_dict[lamp_id1].set_user_mode(curr_cold, curr_warm, curr_pwm_freq)
                self.lamps_dict[lamp_id2].set_user_mode(curr_cold, curr_warm, curr_pwm_freq)

        self.set_lamp_mode_all(target_mode)

    def smooth_on_all(self, target_mode):
        self.set_thread_state(True)
        self.set_lamp_mode_all('off')
        time.sleep(0.5)
        self.set_thread_state(False)

        target_cold = int(self.modes_list[target_mode]['cold'])
        target_warm = int(self.modes_list[target_mode]['warm'])
        target_pwm_freq = int(self.modes_list[target_mode]['pwm_freq'])

        curr_cold = 3600
        curr_warm = 3600

        STEP = 10 # было 100

        while (curr_cold > target_cold or curr_warm > target_warm): # and not self.__stop_mode:
            self.lock.acquire()
            if self.stop_thread is True:
                self.lock.release()
                break
            self.lock.release()
            
            if curr_cold > target_cold:
                curr_cold -= STEP
            if curr_warm > target_warm:
                curr_warm -= STEP
            for lamp_id in self.lamps_dict.keys():
                self.lamps_dict[lamp_id].set_user_mode(curr_cold, curr_warm, target_pwm_freq)
                # print('lamp_id', lamp_id,  'curr_cold ', curr_cold, 'curr_warm: ', curr_warm)
            time.sleep(0.1)
        self.set_lamp_mode_all(target_mode)

    def demo(self): # бегающая лампа
        self.set_thread_state(True)
        self.set_lamp_mode_all('off')
        time.sleep(0.5)
        self.set_thread_state(False)
        lamps_order = [1, 3, 5, 7, 9, 11, 12, 10, 8, 6, 4, 2]
        while True: #not self.__stop_mode:
            print('snake!')
            self.lock.acquire()
            if self.stop_thread is True:
                self.lock.release()
                break
            self.lock.release()            
            for i in range(len(lamps_order)):
                if self.stop_thread is True:
                    self.lock.release()
                    break
                self.lock.release()
                self.set_lamp_mode(lamps_order[i-2], 'off')
                time.sleep(0.125)
                self.set_lamp_mode(lamps_order[i-1], 'default')
                time.sleep(0.25)
                self.set_lamp_mode(lamps_order[i], 'default')
                time.sleep(0.25)

    def gradient_demo(self):
        self.set_thread_state(True)
        time.sleep(0.5)
        self.set_thread_state(False)
        curr_cold = 0
        curr_warm = 3500
        for i in range(0, len(self.lamps_dict), 2):
            self.lock.acquire()
            if self.stop_thread is True:
                self.lock.release()
                break
            self.lock.release()
            lamp_id1 = list(self.lamps_dict.keys())[i]
            lamp_id2 = list(self.lamps_dict.keys())[i+1]
            self.lamps_dict[lamp_id1].set_user_mode(curr_cold, curr_warm, 1000)
            self.lamps_dict[lamp_id2].set_user_mode(curr_cold, curr_warm, 1000)
            curr_cold += 3500/5
            curr_warm -= 3500/5

    def gradient_projector(self):
        self.set_thread_state(True)
        time.sleep(0.5)
        self.set_thread_state(False)
        curr_cold = 4095
        curr_warm = 4095
        total_lamps = len(self.lamps_dict.keys())
        for i in range(0, len(self.lamps_dict.keys()), 2):
            self.lock.acquire()
            if self.stop_thread is True:
                self.lock.release()
                break
            self.lock.release()
            
            lamp_id1 = list(self.lamps_dict.keys())[i]
            lamp_id2 = list(self.lamps_dict.keys())[i+1]
            self.lamps_dict[lamp_id1].set_user_mode(curr_cold, curr_warm, 1000)
            self.lamps_dict[lamp_id2].set_user_mode(curr_cold, curr_warm, 1000)
            curr_cold -= 3600/5
            curr_warm -= 3600/5

    def pairs_on(self, target_mode):
        self.set_thread_state(True)
        self.set_lamp_mode_all('off')
        time.sleep(0.5)
        self.set_thread_state(False)
        STEP = 10
        for i in range(0, len(self.lamps_dict.keys()), 2):
            curr_cold = 4095
            curr_warm = 4095
            target_cold = int(self.modes_list[target_mode]['cold'])
            target_warm = int(self.modes_list[target_mode]['warm'])
            target_pwm_freq = int(self.modes_list[target_mode]['pwm_freq'])
            while curr_warm > target_warm or curr_cold > target_cold:
                self.lock.acquire()
                if self.stop_thread is True:
                    self.lock.release()
                    break
                self.lock.release()
                
                if curr_warm > target_warm:
                    curr_warm -= STEP
                if curr_cold > target_cold:
                    curr_cold -= STEP
                self.lamps_dict[list(self.lamps_dict.keys())[i]].set_user_mode(curr_cold, curr_warm, target_pwm_freq)
                self.lamps_dict[list(self.lamps_dict.keys())[i+1]].set_user_mode(curr_cold, curr_warm, target_pwm_freq)
            time.sleep(0.5)

    #####

    def create_lamps_dict(self):
        lamps_dict = {}
        lamps_config = self.load_lamps_config()
        lamp_modes = self.load_lamp_modes()

        for lamp_id in lamps_config.keys():
            lamp = Lamp(
                self.pwms[lamps_config[lamp_id]['board_id']],
                lamp_id,
                lamps_config[lamp_id],
                'default',
                lamp_modes['default']) # см. конструктор класса Lamp
            lamps_dict[int(lamp_id)] = lamp

        return lamps_dict # создание словаря, состоящего из экземпляров класса Lamp


if __name__ == '__main__':
    lamp_controller = LampController()