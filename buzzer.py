import time
import RPi.GPIO as GPIO

class Buzzer:
    def __init__(self):
        self.notes = {"E2": 82.4, "F2": 87.3, "F#2": 92.4, "G2": 97.9, "G#2": 103.82, "A2": 110.0, "A#2": 116.5, "B2": 123.4,
                 "C3": 130.8, "C#3": 138.5, "D3": 146.8, "D#3": 155.5, "E3": 164.8, "F3": 174.6,
                 "F3#": 184.9, "G3": 195.9, "G#3": 207.6, "A3": 220.0, "A#3": 233.0, "B3": 246.9, "C4": 261.6,
                 "C#4": 277.1,
                 "D4": 293.6, "D#4": 311.1, "E4": 329.6, "F4": 349.2, "F#4": 369.9, "G4": 391.9, "G#4": 415.3,
                 "A4": 440.0,
                 "A#4": 466.1, "B4": 493.8, "C5": 523.2, "C#5": 554.3, "D5": 587.3, "D#5": 622.2, "E5": 659.2,
                 "F5": 698.4,
                 "F#5": 739.9, "G5": 783.9, "G#5": 830.6, "A5": 880.0, "A#5": 932.3, "B5": 987.7, "G6": 1567.9,
                 "rest": 0.1}

        GPIO.setmode(GPIO.BOARD)
        self.buzzer_pin = 8
        GPIO.setup(self.buzzer_pin, GPIO.OUT)

        self.BPM = 4
        self.p = GPIO.PWM(self.buzzer_pin, 100)

    def elise(self):
        self.p.start(4)
        elise1_notes = [self.notes["E4"], self.notes["D#4"], self.notes["E4"], self.notes["D#4"], self.notes["E4"], self.notes["B3"], self.notes["D4"],
                        self.notes["C4"], self.notes["A3"], self.notes["rest"], self.notes["C3"], self.notes["E3"], self.notes["A3"], self.notes["B3"],
                        self.notes["rest"]]
        elise1_beats = [1 / 16, 1 / 16, 1 / 16, 1 / 16, 1 / 16, 1 / 16, 1 / 16, 1 / 16, 1 / 8, 1 / 16, 1 / 16, 1 / 16,
                        1 / 16,
                        1 / 8, 1 / 16]

        elise2_notes = [self.notes["E3"], self.notes["G#3"], self.notes["B3"], self.notes["C4"], self.notes["rest"]]
        elise2_beats = [1 / 16, 1 / 16, 1 / 16, 1 / 8, 1 / 16]

        elise3_notes = elise1_notes
        elise3_beats = elise1_beats

        elise4_notes = [self.notes["E3"], self.notes["C4"], self.notes["B3"], self.notes["A3"], self.notes["rest"]]
        elise4_beats = [1 / 16, 1 / 16, 1 / 16, 1 / 8, 1 / 8]

        print("엘리제를 위하여 시작!!")
        print("elise1")
        for i in range(len(elise1_notes)):
            self.p.ChangeFrequency(elise1_notes[i])
            time.sleep(self.BPM * elise1_beats[i])
            print(i, "번째 음 출력했음.")

        print("elise2")
        for i in range(len(elise2_notes)):
            self.p.ChangeFrequency(elise2_notes[i])
            time.sleep(self.BPM * elise2_beats[i])
            print(i, "번째 음 출력했음.")

        print("elise3")
        for i in range(len(elise3_notes)):
            self.p.ChangeFrequency(elise3_notes[i])
            time.sleep(self.BPM * elise3_beats[i])
            print(i, "번째 음 출력했음.")

        print("elise4")
        for i in range(len(elise4_notes)):
            self.p.ChangeFrequency(elise4_notes[i])
            time.sleep(self.BPM * elise4_beats[i])
            print(i, "번째 음 출력했음.")

        self.p.stop()

    def cart_rider_win(self):
        self.p.start(4)
        cart_rider_win_notes = [self.notes["A4"], self.notes["A4"], self.notes["B4"], self.notes["C5"], self.notes["D5"], self.notes["D5"],
                                self.notes["C5"],
                                self.notes["B4"], self.notes["E5"], self.notes["rest"],
                                self.notes["E5"], self.notes["E5"], self.notes["rest"],
                                self.notes["E5"], self.notes["C#5"], self.notes["A4"], self.notes["rest"],
                                self.notes["E5"], self.notes["C#5"], self.notes["A4"], self.notes["rest"],
                                self.notes["E5"], self.notes["rest"],
                                self.notes["A5"], self.notes["A5"], self.notes["A5"], self.notes["A5"]]

        cart_rider_win_beats = [0.4, 0.4, 0.15, 0.2, 0.4, 0.4, 0.15, 0.2, 0.75, 0.01,
                                0.5, 0.5, 0.01,
                                0.33, 0.22, 0.2, 0.01,
                                0.33, 0.22, 0.2, 0.01,
                                0.5, 0.1,
                                0.21, 0.13, 0.21, 0.13
                                ]

        print("카트라이더 결승 시작!!!")
        for i in range(len(cart_rider_win_notes)):
            self.p.ChangeFrequency(cart_rider_win_notes[i] / 2)
            time.sleep(cart_rider_win_beats[i])
            print(i, "번째 음 출력했음.")

        self.p.stop()

    def cart_rider_bgm(self):
        self.p.start(4)
        cart_rider_bgm1_notes = [self.notes["C4"], self.notes["C4"], self.notes["G4"], self.notes["G4"], self.notes["F4"], self.notes["E4"],
                                 self.notes["F4"],
                                 self.notes["F4"], self.notes["C5"]]
        cart_rider_bgm1_beats = [0.26, 0.15, 0.6, 0.15, 0.15, 0.15, 0.28, 0.15, 0.6]

        print("카트라이더 bgm1 시작!!")
        for i in range(len(cart_rider_bgm1_notes)):
            self.p.ChangeFrequency(cart_rider_bgm1_notes[i])
            time.sleep(cart_rider_bgm1_beats[i])
            print(i, "번째 음 출력했음.")

        self.p.stop()

    def cart_rider_countdown(self):
        self.p.start(4)
        cart_rider_countdown_notes_part1 = [self.notes["B4"], self.notes["B4"], self.notes["B4"], self.notes["G5"]]
        cart_rider_countdown_notes_part2 = [self.notes["G2"], self.notes["G2"], self.notes["G2"], self.notes["G6"]]

        cart_rider_countdown_beats = [0.67, 0.67, 0.67, 0.3]

        print("카트라이더 카운트다운 시작!!")
        for i in range(len(cart_rider_countdown_notes_part1)):
            self.p.ChangeFrequency(cart_rider_countdown_notes_part1[i])
            time.sleep(cart_rider_countdown_beats[i])
            print(i, "번째 1파트 음 출력했음.")

        for i in range(len(cart_rider_countdown_notes_part2)):
            self.p.ChangeFrequency(cart_rider_countdown_notes_part2[i])
            time.sleep(cart_rider_countdown_beats[i])
            print(i, "번째 2파트 음 출력했음.")

        self.p.stop()

    def obstacle_sound(self, distance):
        self.p.start(4)
        obstacle_sound_notes = [self.notes["G#5"], self.notes["rest"]]

        distance = 10  # 이 값은 초음파 센서에서 거리 측정값 받아오셈
        DISTANCE_SOUND_BPM = 0.01  # 상수값 적절하게 조정하셈
        while distance > 5 and distance < 30:
            print("주의!! 전방 장애물과의 거리:", distance, "cm")

            # 5cm ~ 10cm 사이에서는 경보음 연속으로 계속 울림 (rest 없음)
            while distance < 10:
                self.p.ChangeFrequency(obstacle_sound_notes[0])
                time.sleep(0.3)
                distance = 10  # 이 값은 초음파 센서에서 거리 측정값 받아오셈

            # 거리에 비례해서 rest길이 조정
            else:
                self.p.ChangeFrequency(obstacle_sound_notes[0])
                time.sleep(0.3)
                self.p.ChangeFrequency(obstacle_sound_notes[1])
                time.sleep(distance * DISTANCE_SOUND_BPM)

        self.p.stop()

    def danger_sound(self):
        self.p.start(4)
        danger_sound_notes = [self.notes["A#2"]]

        print("위험 알림 시작!!")
        self.p.ChangeFrequency(danger_sound_notes[0])
        time.sleep(1)

        self.p.stop()
