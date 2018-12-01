from car import Car
import threading
import time
import sys
import RPi.GPIO as GPIO


class myCar(object):

    def __init__(self, car_name):
        self.car = Car(car_name)

        self.Detect_line_thread = threading.Thread(target=self.Detect_line)
        self.Detect_obstacle_thread = threading.Thread(target=self.Detect_obstacle)
        self.Measure_time_thread = threading.Thread(target=self.Measure_time)
        self.LED_module_thread = threading.Thread(target=self.LED_moudle)

        self.button_pin = 33
        self.led_pin = 37

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.button_pin, GPIO.IN)
        GPIO.setup(self.led_pin, GPIO.OUT)

        self.line = []
        self.distance = 0
        self.button_pressed_time = 0
        self.drive_start = False

    def Detect_line(self):
        while True:
            self.line = self.car.line_detector.read_digital()
            time.sleep(0.15)

    def Detect_obstacle(self):
        while True:
            self.distance = self.car.distance_detector.get_distance()
            time.sleep(0.15)

    # def Detect_RGB(self):

    def LED_PWM(self):
        print("a")
        for sec in range(0, 101, 1):
            milisec = sec * 0.0001
            GPIO.output(self.led_pin, True)
            time.sleep(milisec)
            GPIO.output(self.led_pin, False)
            time.sleep(0.01 - milisec)
        for sec in range(100, -1, -1):
            milisec = sec * 0.0001
            GPIO.output(self.led_pin, True)
            time.sleep(milisec)
            GPIO.output(self.led_pin, False)
            time.sleep(0.01 - milisec)

    def LED_moudle(self):
        while True:
            if 5 < self.distance < 30:
                print("LED: Detect Obstacle")
                GPIO.output(self.led_pin, True)
                time.sleep(0.5)
                GPIO.output(self.led_pin, False)
                time.sleep(0.5)
            elif self.drive_start:
                print("LED: Car Start")
                self.LED_PWM()
            elif not self.drive_start:
                print("LED: Car Stop")
                GPIO.output(self.led_pin, True)

    # def Buzzer_module(self):
    #
    # def Drive(self):

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

    def car_startup(self):
        self.Detect_obstacle_thread.start()
        self.Detect_line_thread.start()
        self.Measure_time_thread.start()
        self.LED_module_thread.start()

        while True:
            if 0 < self.button_pressed_time < 2:
                if self.drive_start:
                    # self.car.drive_parking()
                    print("Button: stop")
                    self.drive_start = False
                    self.button_pressed_time = 0
                elif not self.drive_start:
                    # self.Drive()
                    print("Button: start")
                    self.drive_start = True
                    self.button_pressed_time = 0
            elif self.button_pressed_time >= 2:
                print("키보드 입력 모듈")
                self.button_pressed_time = 0


if __name__ == "__main__":
    try:
        myCar = myCar("CarName")
        myCar.car_startup()

    except KeyboardInterrupt:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        myCar.drive_parking()
