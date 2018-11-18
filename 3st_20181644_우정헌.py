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
        self.previous_step_turn = 12
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

        # 거리 측정의 정확도를 높히기 위해 2번 측정합니다.
        # 2번 측정값이 모두 distanceSet보다 작거나 같은 경우 True를 반환합니다.
        elif distance <= distanceSet:
            distance = self.car.distance_detector.get_distance()
            if distance != -1 and distance <= distanceSet:
                return True
            return False
        else:
            return False

    # =======================================================================
    # 3RD_ASSIGNMENT_CODE
    # Complete the code to perform Third Assignment
    # =======================================================================

    def line_tracing(self):

        # 뒷바퀴 35의 속도로 직진
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

        # 00000이 감지 될경우 앞바퀴를 기존 각의 크기만큼 반대방향으로 틀고 후진을 합니다.
        elif self.car.line_detector.is_equal_status([0, 0, 0, 0, 0]):
            print("00000이 감지되었습니다!!")
            self.car.accelerator.go_backward(35)
            step_turn = self.previous_step_turn * (-1)
            self.car.steering.turn(90 + step_turn)
            print("0.5초간 후진합니다.")
            time.sleep(0.5)

        elif self.car.line_detector.is_equal_status([1, 1, 1, 1, 1]):
            step_turn = self.CENTER_STEP_TURN
            print()
            print("11111이 감지되었습니다!!!!!")
            print()

        else:
            step_turn = -1

        self.car.steering.turn(90 + step_turn)

        # --<테스트 코드>--
        # 라인의 위치가 바뀐 경우 위치를 측정해 출력
        #  self.car.line_detector.read_digital()를 새로 불러오기 때문에 주행중 시간 오차로 인해 값이 달라질 가능성도 (very little) 있음.
        if self.previous_step_turn != step_turn:
            print("Position of line: ", self.car.line_detector.read_digital())
            self.previous_step_turn = step_turn

            # if문과 elif문에서 정의되지 않은 경우
            if step_turn == -1:
                print("정의되지 않은 경우이므로 재측정 합니다. >>", self.car.line_detector.read_digital())

    # --<테스트 코드>--
    # 장애물 회피기능 없이 라인트레이싱만 테스트 가능
    def line_test(self):
        while True:
            self.line_tracing()

    def car_startup(self):
        while True:

            if self.find_abstacle(30):
                self.count_echo += 1
                print()
                print("앗 장애물이닷!!")
                print("장애물 만난 횟수:", self.count_echo)

                # 1.5초동안 왼쪽으로 30도만큼 좌회전
                step_turn = self.LARGE_STEP_TURN * (-1)
                self.car.steering.turn(90 + step_turn)
                time.sleep(1.5)
                print("왼쪽으로 장애물을 피해갑니다!")

                # 0.7초동안 직진합니다
                self.car.steering.turn(90)
                time.sleep(0.7)
                print("장애물 피해 직진!!")

                # 1.5초동안 왼쪽으로 30도만큼 좌회전
                step_turn = self.LARGE_STEP_TURN
                self.car.steering.turn(90 + step_turn)
                time.sleep(1.5)
                print("장애물을 피한 후 오른쪽으로 트랙으로 복귀중입니다!")

                # 트랙으로 정상 복귀 할때까지 휴식
                while not self.car.line_detector.is_in_line():
                    time.sleep(0.2)
                    print("sleep for 0.2 sec")
                    print("트랙으로 복귀중...")

            else:
                print("트랙에서 정상적으로 주행중입니다.")
                self.line_tracing()

                if self.count_echo == 4 and self.car.line_detector.is_equal_status([1, 1, 1, 1, 1]):
                    print()
                    print("2바퀴 완주 성공!!")
                    self.drive_parking()
                    print("주차 완료!!")
                    break


if __name__ == "__main__":

    try:
        myCar = myCar("CarName")
        # line_test()함수는 테스트용 코드.
        # myCar.line_test()
        myCar.car_startup()


    except KeyboardInterrupt:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        myCar.drive_parking()
        print("정상적으로 강제 종료하였습니다.")
