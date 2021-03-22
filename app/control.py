# В этом файле осуществляется управление светильниками


# from app.classes import DUMMY_PCA9685 as Adafruit_PCA9685

import Adafruit_PCA9685

import json
from app.classes.lamp import Lamp # В классе Lamp содержатся основные атрибуты светильника

pwms = {
    0: Adafruit_PCA9685.PCA9685(0x40),
    1: Adafruit_PCA9685.PCA9685(0x41)
} # Список плат ШИМ (на одной висит 8 светильников, на второй - 4)

def load_lamps_config():
    with open('lamps.json', 'r') as f:
        lamps_config = json.load(f)
        return lamps_config # загрузка конфигурации пинов и номеров плат ШИМ светильников

def load_lamp_modes():
    with open('modes.json', 'r') as f:
        modes = json.load(f)
        return modes # загрузка режимов, в которых могут работать светильники

def set_lamp_mode(lamp_id, mode):
    lamps_dict[lamp_id].set_mode(mode, modes_list[mode]) # задать режим работы для светильника с номером lamp_id

def set_lamp_mode_all(mode):
    for lamp_id in lamps_dict.keys():
        set_lamp_mode(lamp_id, mode) # задать режим работы для всех светильников

def create_lamps_dict():
    lamps_dict = {}
    lamps_config = load_lamps_config()
    lamp_modes = load_lamp_modes()

    for lamp_id in lamps_config.keys():
        lamp = Lamp(
            pwms[lamps_config[lamp_id]['board_id']],
            lamp_id,
            lamps_config[lamp_id],
            'default',
            lamp_modes['default']) # см. конструктор класса Lamp
        lamps_dict[lamp_id] = lamp

    return lamps_dict # создание списка, состоящего из экземпляров класса Lamp

modes_list = load_lamp_modes() # загрузка списка режимов работы светильников
lamps_dict = create_lamps_dict() # создание списка, состоящего из экземпляров класса Lamp