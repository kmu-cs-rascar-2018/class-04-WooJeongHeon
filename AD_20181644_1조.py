from car import Car
import threading
import time
import sys
import keyboard
import buzzer
import RPi.GPIO as GPIO


class myCar(object):

    def __init__(self, car_name):
        self.car = Car(car_name)

        self.Detect_line_thread = threading.Thread(target=self.Detect_line)
        self.Detect_obstacle_thread = threading.Thread(target=self.Detect_obstacle)
        self.Measure_time_thread = threading.Thread(target=self.Measure_time)
        self.LED_module_thread = threading.Thread(target=self.LED_moudle)

        self.key_input_thread = threading.Thread(target=self.key_input)
        self.key_input2_thread = threading.Thread(target=self.key_input2)
        self.key_input3_thread = threading.Thread(target=self.key_input3)
        self.key_input4_thread = threading.Thread(target=self.key_input4)
        self.key_input5_thread = threading.Thread(target=self.key_input5)

        self.key_w = ""
        self.key_s = ""
        self.key_a = ""
        self.key_d = ""
        self.key_shift = ""

        self.button_pin = 33
        self.led_pin = 37

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.button_pin, GPIO.IN)
        GPIO.setup(self.led_pin, GPIO.OUT)

        self.line = []
        self.distance = 0
        self.button_pressed_time = 0
        self.drive_start = False
        self.buzzer = buzzer.Buzzer()
        self.car_buzzer_start_count = 0

    def key_input(self):
        while True:
            if keyboard.is_pressed('w'):
                self.key_w = 'w'
            else:
                self.key_w = ''
            time.sleep(0.1)

    def key_input2(self):
        while True:
            if keyboard.is_pressed('s'):
                self.key_s = 's'
            else:
                self.key_s = ''
            time.sleep(0.1)

    def key_input3(self):
        while True:
            if keyboard.is_pressed('a'):
                self.key_a = 'a'
            else:
                self.key_a = ''
            time.sleep(0.1)

    def key_input4(self):
        while True:
            if keyboard.is_pressed('d'):
                self.key_d = 'd'
            else:
                self.key_d = ''
            time.sleep(0.1)

    def key_input5(self):
        while True:
            if keyboard.is_pressed('shift'):
                self.key_shift = 'shift'
            else:
                self.key_shift = ''
            time.sleep(0.1)

    def Detect_line(self):
        while True:
            self.line = self.car.line_detector.read_digital()

    def Detect_obstacle(self):
        while True:
            self.distance = self.car.distance_detector.get_distance()
            time.sleep(0.1)

    # def Detect_RGB(self):

    def LED_PWM(self):
        for sec in range(0, 101, 1):
            milisec = sec * 0.0001
            GPIO.output(self.led_pin, True)
            time.sleep(milisec)
            GPIO.output(self.led_pin, False)
            time.sleep(0.01 - milisec)
            if not self.drive_start:
                return 0

        for sec in range(100, -1, -1):
            milisec = sec * 0.0001
            GPIO.output(self.led_pin, True)
            time.sleep(milisec)
            GPIO.output(self.led_pin, False)
            time.sleep(0.01 - milisec)
            if not self.drive_start:
                return 0

    def LED_moudle(self):
        while True:

            self.distance = self.car.distance_detector.get_distance()
            print(self.distance)

            if 5 < self.distance < 30:
                # self.buzzer.obstacle_sound()
                count = 0
                while count <= 2:
                    print("LED: Detect Obstacle")
                    GPIO.output(self.led_pin, True)
                    time.sleep(0.5)
                    GPIO.output(self.led_pin, False)
                    time.sleep(0.5)
                    count += 1

            elif not self.drive_start:
                print("LED: Car Stop")
                GPIO.output(self.led_pin, True)
            """elif self.drive_start:
                print("LED: Car Start")
                self.LED_PWM()"""

            time.sleep(0.1)

    def Drive(self):
        count = 0
        countt = 0
        counttt = 0
        while True:
            rawData = self.car.color_getter.get_raw_data()
            if 300 < rawData[0] < 350 and 50 < rawData[1] < 100 and 50 < rawData[2] < 100:
                print("Red")
                self.buzzer.danger_sound()
                self.car.accelerator.stop()
                time.sleep(1)
                while True:
                    rawData = self.car.color_getter.get_raw_data()
                    if 350 < rawData[1] < 500 and 50 < rawData[0] < 200 and 150 < rawData[2] < 300:
                        print("Green")
                        self.car.accelerator.go_forward(50)
                        break

            self.line = self.car.line_detector.read_digital()
            self.car.accelerator.go_forward(40)

            if 0 < self.distance <= 30:
                count += 1
            if count >= 10:
                countt += 1
                print("distance detected")
                self.car.accelerator.stop()
                self.car.steering.turn(60)
                self.car.accelerator.go_forward(50)
                time.sleep(0.4)
                while True:
                    self.line = self.car.line_detector.read_digital()
                    if self.line == [1, 0, 0, 0, 0] or self.line == [1, 1, 0, 0, 0]:
                        self.car.accelerator.stop()
                        time.sleep(0.1)
                        self.car.accelerator.go_backward(50)
                        time.sleep(0.4)
                        self.car.steering.turn(120)
                        self.car.accelerator.go_forward(50)
                        time.sleep(1)
                        break
                    else:
                        pass

                while True:
                    self.line = self.car.line_detector.read_digital()
                    if self.line == [0, 0, 1, 0, 0] or self.line == [1, 1, 1, 0, 0] or self.line == [0, 1, 1, 0, 0]:
                        self.car.steering.turn(90)
                        self.car.accelerator.stop()
                        self.car.accelerator.go_backward(30)
                        time.sleep(0.05)
                        count = 0
                        break
                    else:
                        pass

            if (self.line == [0, 0, 1, 0, 0]):
                continue
            elif (self.line == [0, 1, 1, 0, 0]):
                self.car.steering.turn(80)
            elif (self.line == [0, 1, 0, 0, 0]):
                self.car.steering.turn(75)
            elif (self.line == [1, 1, 0, 0, 0]):
                self.car.steering.turn(50)
            elif (self.line == [1, 0, 0, 0, 0]):
                self.car.steering.turn(45)
            elif (self.line == [0, 0, 1, 1, 0]):
                self.car.steering.turn(95)
            elif (self.line == [0, 0, 0, 1, 0]):
                self.car.steering.turn(100)
            elif (self.line == [0, 0, 0, 1, 1]):
                self.car.steering.turn(120)
            elif (self.line == [0, 0, 0, 0, 1]):
                self.car.steering.turn(125)
            elif (self.line == [0, 0, 0, 0, 0]):
                self.car.accelerator.stop()
                self.car.steering.turn(120)
                self.car.accelerator.go_backward(25)
                while True:
                    # print(self.line)
                    self.line = self.car.line_detector.read_digital()
                    if (self.line == [0, 0, 0, 1, 1] or self.line == [0, 0, 0, 0, 1] or self.line == [0, 0, 1, 1,
                                                                                                      0]):
                        break
                    else:
                        continue
                self.car.accelerator.stop()
                self.car.steering.turn(70)
                self.car.accelerator.go_forward(25)
                while True:
                    # print(self.line)
                    self.line = self.car.line_detector.read_digital()
                    if (self.line == [1, 1, 0, 0, 0] or self.line == [1, 0, 0, 0, 0] or self.line == [0, 1, 1, 0,
                                                                                                      0] or self.line == [
                        0, 0, 1, 0, 0] or self.line == [0, 0, 1, 1, 0]):
                        break
                    else:
                        continue
                self.car.accelerator.go_forward(85)
                time.sleep(0.1)
            elif (self.line == [1, 1, 1, 1, 1]):
                if countt >= 1:
                    self.car.accelerator.stop()
                    time.sleep(1)
                    self.car.accelerator.go_backward(20)
                    time.sleep(0.3)
                    self.car.accelerator.stop()
                    print(countt)
                    self.buzzer.cart_rider_win()
                    break
            elif (self.line == [1, 1, 1, 0, 0]):
                print("T")
                if counttt == 0:
                    self.car.accelerator.stop()
                    time.sleep(1)
                    self.car.steering.turn(80)
                    self.car.accelerator.go_forward(40)
                    time.sleep(0.3)
                    self.car.steering.turn(120)
                    self.car.accelerator.go_forward(40)
                    time.sleep(1)
                    self.car.steering.turn(65)
                    self.car.accelerator.go_backward(40)
                    time.sleep(1.7)
                    self.car.steering.turn(90)
                    self.car.accelerator.go_backward(50)
                    time.sleep(0.4)
                    self.car.steering.turn(90)
                    self.car.accelerator.go_forward(50)
                    time.sleep(0.5)
                    self.car.steering.turn(65)
                    self.car.accelerator.go_forward(40)
                    time.sleep(1)
                    self.car.steering.turn(120)
                    self.car.accelerator.go_backward(40)
                    time.sleep(1.4)
                    self.car.accelerator.stop()
                    time.sleep(1)
                    counttt += 1
                elif counttt >= 1:
                    continue

    def Measure_time(self):
        before_input = 1
        button_on_time = 0
        while True:
            button_input = GPIO.input(self.button_pin)

            if (button_input != before_input):
                print(button_input)
                if button_input == 0:
                    button_on_time = time.time()
                elif button_input == 1:
                    button_off_time = time.time() - button_on_time
                    self.button_pressed_time = button_off_time
                    print("time:", self.button_pressed_time)

            before_input = button_input

            time.sleep(0.1)

    def car_startup(self):
        self.LED_module_thread.start()
        self.Measure_time_thread.start()
        # self.Detect_obstacle_thread.start()
        # self.Detect_line_thread.start()

        while True:
            if 0 < self.button_pressed_time < 2:
                if self.drive_start:
                    print("Button: stop")
                    self.drive_start = False
                    self.button_pressed_time = 0

                    self.car.drive_parking()
                if not self.drive_start:
                    self.buzzer.cart_rider_countdown()
                    self.Drive()
                    print("Button: start")
                    self.drive_start = True
                    self.button_pressed_time = 0
            elif self.button_pressed_time >= 2:
                print("키보드 입력 모듈")
                self.buzzer.elise()
                self.key_input_thread.start()
                self.key_input2_thread.start()
                self.key_input3_thread.start()
                self.key_input4_thread.start()
                self.key_input5_thread.start()

                while True:
                    # print(self.key_a, self.key_s, self.key_d, self.key_w, self.key_shift)
                    speed = 60
                    if self.key_shift == 'shift':
                        speed = 100
                    if self.key_w == 'w':
                        self.car.accelerator.go_forward(speed)
                        if self.key_w == 'w' and (self.key_a == '' and self.key_d == ''):
                            self.car.steering.turn(90)
                    if self.key_s == 's':
                        self.car.accelerator.go_backward(speed)
                        if self.key_s == 's' and (self.key_a == '' and self.key_d == ''):
                            self.car.steering.turn(90)
                    if self.key_a == 'a':
                        self.car.steering.turn(60)
                    if self.key_d == 'd':
                        self.car.steering.turn(120)
                    if self.key_w == '' and self.key_a == '' and self.key_d == '' and self.key_s == '' and self.key_shift == '':
                        self.car.accelerator.stop()
                        self.car.steering.turn(90)
                    time.sleep(0.1)

                self.button_pressed_time = 0

            time.sleep(0.1)

    def drive_parking(self):
        self.car.drive_parking()


if __name__ == "__main__":
    try:
        myCar = myCar("CarName")
        myCar.car_startup()

    except KeyboardInterrupt:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        myCar.drive_parking()
