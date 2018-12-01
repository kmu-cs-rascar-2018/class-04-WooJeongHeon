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

    def Buzzer_module(self):    

        # Raspberry Pi의 buzzer_pin을 8번으로 사용합니다.
        buzzer_pin = 8

        # BCM GPIO 핀 번호를 사용하도록 설정합니다.
        GPIO.setmode(GPIO.BOARD)


        notes = {"A#2": 116.5, "G2": 97.9, "C3": 130.8, "C#3": 138.5, "D3": 146.8, "D#3": 155.5, "E3": 164.8, "F3": 174.6,
         "F3#": 184.9,
         "G3": 195.9,
         "G#3": 207.6, "A3": 220.0, "A#3": 233.0, "B3": 246.9, "C4": 261.6,
         "C#4": 277.1, "D4": 293.6, "D#4": 311.1, "E4": 329.6, "F4": 349.2,
         "F#4": 369.9, "G4": 391.9,
         "G#4": 415.3, "A4": 440.0, "A#4": 466.1, "B4": 493.8, "C5": 523.2, "C#5": 554.3, "D5": 587.3, "D#5": 622.2,
         "E5": 659.2, "F5": 698.4, "F#5": 739.9, "G5": 783.9, "G#5": 830.6, "A5": 880.0, "A#5": 932.3, "B5": 987.7,
         "G6": 1567.9}


        GPIO.setup(buzzer_pin, GPIO.OUT)

        BPM = 2




        # 엘리제를 위하여
        # 미 레# 미 레# 미 시 레 도 라
        elise1_notes = [notes["E4"], notes["D#4"], notes["E4"], notes["D#4"], notes["E4"], notes["B3"], notes["D4"],
                notes["C4"],
                notes["A3"]]
        elise1_beats = [1 / 8, 1 / 8, 1 / 8, 1 / 8, 1 / 8, 1 / 8, 1 / 8, 1 / 8, 1 / 4]

        # 카트라이더 우승
        # 결승: 라라시도 레레도시미 미미미도#라미도#라 미라라라라
        cart_rider_win_notes = [notes["A4"], notes["A4"], notes["B4"], notes["C5"], notes["D5"], notes["D5"], notes["C5"],
                        notes["B4"], notes["E5"], notes["E5"], notes["E5"], notes["E5"], notes["C#5"], notes["A4"],
                        notes["E5"], notes["C#5"], notes["A4"], notes["E5"], notes["A5"], notes["A5"], notes["A5"],
                        notes["A5"]]

        # 카트라이더 BGB1
        # 도도솔 솔파미파파 도
        cart_rider_bgm1_notes = [notes["C4"], notes["C4"], notes["G4"], notes["G4"], notes["F4"], notes["E4"], notes["F4"],
                         notes["F4"], notes["C5"]]

        # 카트라이더 카운트다운
        # B4(G2) B4(G2) B4(G2) G5(G6)
        # 시4(솔2) 시(솔) 시(솔) 솔5(솔6)
        cart_rider_countdown_notes_part1 = [notes["B4"], notes["B4"], notes["B4"], notes["G5"]]
        cart_rider_countdown_notes_part2 = [notes["G2"], notes["G2"], notes["G2"], notes["G6"]]

        # 전방 감지기
        # G#5
        # 솔#5
        obstacle_sound_notes = [notes["G#5"]]

        # 위험 소리
        # A#2
        # 라#2
        obstacle_sound_notes = [notes["A#2"]]

        try:
            p = GPIO.PWM(buzzer_pin, 100)
            p.start(4)  # start the PWM on 4% duty cycle

            print()
            print("엘리제를 위하여 시작!!")
            for i in range(len(elise1_notes)):
                p.ChangeFrequency(elise1_notes[i])
                time.sleep(BPM * elise1_beats[i])
                print(i, "번째 음 출력했음.")


            print()
            print("카트라이더 결승 시작!!!")
            for i in range(len(cart_rider_win_notes)):
                p.ChangeFrequency(cart_rider_win_notes[i]/2)
                time.sleep(0.3)
                print(i, "번째 음 출력했음.")

            print()
            print("카트라이더 bgm1 시작!!")
            for i in range(len(cart_rider_bgm1_notes)):
                p.ChangeFrequency(cart_rider_bgm1_notes[i]/2)
                time.sleep(0.3)
                print(i, "번째 음 출력했음.")

            print()
            print("카트라이더 카운트다운 시작!!")
            for i in range(len(cart_rider_countdown_notes_part1)):
                p.ChangeFrequency(cart_rider_countdown_notes_part1[i]/2)
                time.sleep(0.3)
                print(i, "번째 1파트 음 출력했음.")

                p.ChangeFrequency(cart_rider_countdown_notes_part2[i]/2)
                time.sleep(0.1)
                print(i, "번째 2파트 음 출력했음.")
            
            
            p.stop()  # stop the PWM output



        finally:
            GPIO.cleanup()
        
        
    
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
