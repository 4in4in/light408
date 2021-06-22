import RPi.GPIO as GPIO
import time, os


class JalController:
    jal_list = { 1: (22, 27, 17), 2: (6, 13, 19) }

    def __init__(self):
        self.setup()

    def setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        for jal_id in self.jal_list:
            for pin_id in self.jal_list[jal_id]:
                GPIO.setup(pin_id, GPIO.OUT)
                GPIO.output(pin_id, 1)

        os.system("clear")

    def move(self, jal_id, move_type):
        GPIO.output(self.jal_list[jal_id][0], 1)
        time.sleep(0.25)
        out_val = 1 if move_type == 'up' else 0
        GPIO.output(self.jal_list[jal_id][1], out_val)
        GPIO.output(self.jal_list[jal_id][2], out_val)
        time.sleep(0.25)
        GPIO.output(self.jal_list[jal_id][0], 0)

    def stop(self, jal_id):
        for pin_id in self.jal_list[jal_id]:
            GPIO.output(pin_id, 1)

    def turn_up(self,jal_id, open_type):
        self.move(jal_id, open_type)
        time.sleep(0.5)
        self.stop(jal_id)

    def leave(self):
        for jal_id in self.jal_list:
            self.stop(jal_id)
            os.system("clear")
            # GPIO.cleanup()

if __name__=="__main__":
    controller = JalController()

    while True:
        command = int(input("\tНомер жалюзи(1,2) + Команды:\n\t1 - Поднять, 2 - Опустить, 3 - Стоп, 4 - Открыть вверх, 5 - Открыть вниз, 0 - Выйти\n\tКоманда: "))
        jal_id = command // 10
        command %= 10

        if command == 1:
            controller.move(jal_id, 'up')
        elif command ==2:
            controller.move(jal_id, 'down')
        elif command == 3:
            controller.stop(jal_id)
        elif command == 4:
            controller.turn_up(jal_id, 'up')
        elif command == 5:
            controller.turn_up(jal_id, 'down')
        elif command == 0:
            controller.leave()
            break