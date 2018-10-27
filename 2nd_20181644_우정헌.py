#########################################################################
# Date: 2018/10/02
# file name: 2nd_assignment_main.py
# Purpose: this code has been generated for the 4 wheel drive body
# moving object to perform the project with line detector
# this code is used for the student only
#########################################################################

from car import Car
import time


class myCar(object):

    def __init__(self, car_name):
        self.car = Car(car_name)

    def drive_parking(self):
        self.car.drive_parking()

    # =======================================================================
    # 2ND_ASSIGNMENT_CODE
    # Complete the code to perform Second Assignment
    # =======================================================================
    def car_startup(self):
        # implement the assignment code here
        # ㄴ OK!!

        # Step Turn
        VERY_LITTLE_STEP_TURN = 5
        LITTLE_STEP_TURN = 10
        LARGE_STEP_TURN = 30
        VERY_LARGE_STEP_TURN = 35
        CENTER_STEP_TURN = 0

        # 변수 초기화
        previous_step_turn = -2

        # 뒷바퀴 40의 속도로 직진
        self.car.accelerator.go_forward(40)
        while True:

            # 검은 라인의 위치를 측정하고 그에 따른 조향 각도를 step_turn 변수로 받습니다.
            if self.car.line_detector.is_equal_status([0, 0, 1, 0, 0]) or self.car.line_detector.is_equal_status(
                    [0, 1, 1, 1, 0]):
                step_turn = CENTER_STEP_TURN

            elif self.car.line_detector.is_equal_status([0, 1, 1, 0, 0]):
                step_turn = VERY_LITTLE_STEP_TURN * (-1)
            elif self.car.line_detector.is_equal_status([0, 0, 1, 1, 0]):
                step_turn = VERY_LITTLE_STEP_TURN

            elif self.car.line_detector.is_equal_status([0, 1, 0, 0, 0]):
                step_turn = LITTLE_STEP_TURN * (-1)
            elif self.car.line_detector.is_equal_status([0, 0, 0, 1, 0]):
                step_turn = LITTLE_STEP_TURN

            elif self.car.line_detector.is_equal_status([1, 1, 0, 0, 0]):
                step_turn = LARGE_STEP_TURN * (-1)
            elif self.car.line_detector.is_equal_status([0, 0, 0, 1, 1]):
                step_turn = LARGE_STEP_TURN

            elif self.car.line_detector.is_equal_status([1, 0, 0, 0, 0]):
                step_turn = VERY_LARGE_STEP_TURN * (-1)
            elif self.car.line_detector.is_equal_status([0, 0, 0, 0, 1]):
                step_turn = VERY_LARGE_STEP_TURN

            else:
                step_turn = -1

            self.car.steering.turn(90 + step_turn)

            # <테스트 코드>
            # 라인의 위치가 바뀐 경우 위치를 측정해 출력
            #  self.car.line_detector.read_digital()를 새로 불러오기 때문에 주행중 시간 오차로 인해 값이 달라질 가능성도 (very little) 있음.
            if step_turn != previous_step_turn:
                print("Position of line: ", self.car.line_detector.read_digital())
                previous_step_turn = step_turn

                # if문과 elif문에서 정의되지 않은 경우
                if step_turn == -1:
                    print("정의되지 않은 경우이므로 재측정 합니다. >>", self.car.line_detector.read_digital())


if __name__ == "__main__":
    try:
        myCar = myCar("CarName")
        myCar.car_startup()

    except KeyboardInterrupt:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        myCar.drive_parking()
        print("정상적으로 중지 하였습니다.")
