#########################################################################
# Date: 2018/10/02
# file name: 3rd_assignment_main.py
# Purpose: this code has been generated for the 4 wheel drive body
# moving object to perform the project with line detector
# this code is used for the student only
#########################################################################

from car import Car
import time


class myCar(object):

    def __init__(self, car_name):
        self.car = Car(car_name)

        # Step Turn
        self.VERY_LITTLE_STEP_TURN = 5
        self.LITTLE_STEP_TURN = 10
        self.LARGE_STEP_TURN = 30
        self.VERY_LARGE_STEP_TURN = 35
        self.CENTER_STEP_TURN = 0

        # 변수 초기화
        self.previous_step_turn = -2

        self.count_echo = 0

    def drive_parking(self):
        self.car.drive_parking()

    def find_abstacle(self, distanceSet):

        distance = self.car.distance_detector.get_distance()
        print("초음파센서 거리: ", distance)

        # 초음파 센서 오류시 거리 재측정
        if distance == -1:
            print("일시적인 초음파센서 오류로 인하여 거리를 다시 측정합니다.")
            return False

        elif distance <= distanceSet:
            if distance <= distanceSet:
                if distance <= distanceSet:
                    if distance <= distanceSet:
                        return True
            return False
        else:
            return False

    # =======================================================================
    # 3RD_ASSIGNMENT_CODE
    # Complete the code to perform Third Assignment
    # =======================================================================

    def line_tracing(self):

        # while True:

        # 뒷바퀴 40의 속도로 직진
        self.car.accelerator.go_forward(35)

        # 검은 라인의 위치를 측정하고 그에 따른 조향 각도를 step_turn 변수로 받습니다.
        if self.car.line_detector.is_equal_status([0, 0, 1, 0, 0]) or self.car.line_detector.is_equal_status(
                [0, 1, 1, 1, 0]):
            step_turn = self.CENTER_STEP_TURN

        elif self.car.line_detector.is_equal_status([0, 1, 1, 0, 0]):
            step_turn = self.VERY_LITTLE_STEP_TURN * (-1)
        elif self.car.line_detector.is_equal_status([0, 0, 1, 1, 0]):
            step_turn = self.VERY_LITTLE_STEP_TURN

        elif self.car.line_detector.is_equal_status([0, 1, 0, 0, 0]):
            step_turn = self.LITTLE_STEP_TURN * (-1)
        elif self.car.line_detector.is_equal_status([0, 0, 0, 1, 0]):
            step_turn = self.LITTLE_STEP_TURN

        elif self.car.line_detector.is_equal_status([1, 1, 0, 0, 0]):
            step_turn = self.LARGE_STEP_TURN * (-1)
        elif self.car.line_detector.is_equal_status([0, 0, 0, 1, 1]):
            step_turn = self.LARGE_STEP_TURN

        elif self.car.line_detector.is_equal_status([1, 0, 0, 0, 0]):
            step_turn = self.VERY_LARGE_STEP_TURN * (-1)
        elif self.car.line_detector.is_equal_status([0, 0, 0, 0, 1]):
            step_turn = self.VERY_LARGE_STEP_TURN

        elif self.car.line_detector.is_equal_status([0, 0, 0, 0, 0]):
            print("00000 state")
            self.car.accelerator.go_backward(30)
            step_turn = self.previous_step_turn * (-1)
            # step_turn = -30
            self.car.steering.turn(90 + step_turn)

            time.sleep(0.5)
            print("back -35 0.5sec")

        elif self.car.line_detector.is_equal_status([1, 1, 1, 1, 1]):
            step_turn = 1 - 1
            print()
            print("1111111111111111111111111이 찍혔어요.")
            print()

        else:
            step_turn = -1

        self.car.steering.turn(90 + step_turn)

        self.previous_step_turn = step_turn

    def line_test(self):
        while True:
            self.line_tracing()

    def car_startup(self):
        while True:

            print("무한루프에 들어왔어용!!")
            if self.find_abstacle(30):
                print()
                print("앗 장애물이닷!!")

                self.count_echo += 1

                step_turn = self.LARGE_STEP_TURN * (-1)
                self.car.steering.turn(90 + step_turn)
                time.sleep(1.5)
                print("바퀴 왼쪽으로 꺾음")

                self.car.steering.turn(90)
                time.sleep(0.7)
                print("go straight")

                step_turn = self.LARGE_STEP_TURN
                self.car.steering.turn(90 + step_turn)
                time.sleep(2)
                print("바퀴 오른쪽으로 꺾음")

                while not self.car.line_detector.is_in_line():
                    time.sleep(0.2)
                    print("sleep 0.2sec")

            else:
                print("트랙에서 정상적으로 주행중")
                self.line_tracing()

                if self.count_echo == 4 and self.car.line_detector.is_equal_status([1, 1, 1, 1, 1]):
                    self.drive_parking()
                    print("success stop")
                    break


if __name__ == "__main__":

    try:
        myCar = myCar("CarName")
        # myCar.line_test()
        myCar.car_startup()


    except KeyboardInterrupt:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        myCar.drive_parking()
        print("정상적으로 강제 종료하였습니다.")
