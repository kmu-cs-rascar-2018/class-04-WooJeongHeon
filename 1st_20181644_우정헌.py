#########################################################################
# Date: 2018/08/09
# file name: 1st_assignment_main.py
# Purpose: this code has been generated for the 4 wheels drive body
# moving object to perform the project with ultra sensor
# this code is used for the student only
#########################################################################


# =======================================================================
# import GPIO library and time module
# =======================================================================
import RPi.GPIO as GPIO
import time

# =======================================================================
# import ALL method in the SEN040134 Tracking Module
# =======================================================================
from SEN040134 import SEN040134_Tracking as Tracking_Sensor

# =======================================================================
# import ALL method in the TCS34725 RGB Module
# =======================================================================
from TCS34725 import TCS34725_RGB as RGB_Sensor

# =======================================================================
# import ALL method in the SR02 Ultrasonic Module
# =======================================================================
from SR02 import SR02_Ultrasonic as Ultrasonic_Sensor

# =======================================================================
# import ALL method in the rear/front Motor Module
# =======================================================================
import rear_wheels
import front_wheels

# =======================================================================
#  set GPIO warnings as false
# =======================================================================
GPIO.setwarnings(False)


class Car(object):

    def __init__(self):
        self.moduleInitialize()

    def drive_parking(self):
        # front wheels center allignment
        self.front_steering.turn_straight()

        # power down both wheels
        self.rear_wheels_drive.stop()
        self.rear_wheels_drive.power_down()

    # =======================================================================
    # 1ST_ASSIGNMENT_CODE
    # Complete the code to perform First Assignment
    # =======================================================================
    def assignment_selfDriving(self, distanceSet, speedSet):
        print("%d의 속도로 전진합니다." % speedSet)
        self.rear_wheels_drive.forward_with_speed(speedSet)
        while True:
            distance = self.distance_detector.get_distance()

            # 초음파 센서 오류시 거리 재측정
            if distance == -1:
                print("일시적인 초음파센서 오류로 인하여 거리를 다시 측정합니다.")
                continue

            elif distance <= distanceSet:
                self.rear_wheels_drive.stop()
                print("전방 %dcm이내 장애물 감지!!" % distanceSet)
                print("4초간 %d의 속도로 후진합니다." % speedSet)
                self.rear_wheels_drive.backward_with_speed(speedSet)
                time.sleep(4)
                self.rear_wheels_drive.stop()
                break

    def assignment_main(self):
        # Implement the assignment code here.
        # OK!!

        self.front_steering.turn_straight()

        # 30의 속도로 전진, 장애물 앞 15cm 에서 정지 후 4초간 30의 속도로 후진
        print("\n---<첫번째 미션 시작>---")
        self.assignment_selfDriving(15, 30)

        # 50의 속도로 전진, 장애물 앞 20cm 에서 정지 후 4초간 50의 속도로 후진
        print("\n---<두번째 미션 시작>---")
        self.assignment_selfDriving(20, 50)

        # 70의 속도로 전진, 장애물 앞 25cm 에서 정지 후 4초간 70의 속도로 후진
        print("\n---<세번째 미션 시작>---")
        self.assignment_selfDriving(25, 70)

        # 모든 과제 완료 후 자동차 주차 함수 호출
        self.drive_parking()
        print("\n1차 과제 완료!!")

    def moduleInitialize(self):
        try:
            self.distance_detector = Ultrasonic_Sensor.Ultrasonic_Avoidance(35)

            self.front_steering = front_wheels.Front_Wheels(db='config')
            self.front_steering.ready()
            self.front_steering.turn_straight()

            self.rear_wheels_drive = rear_wheels.Rear_Wheels(db='config')
            self.rear_wheels_drive.ready()

        except:
            print("moduleInitialize ERROR")
            self.drive_parking()


if __name__ == "__main__":
    try:
        car = Car()
        car.assignment_main()

    except KeyboardInterrupt:
        # when the Ctrl+C key has been pressed,
        # the moving object will be stopped
        car.drive_parking()
        print("성공적으로 종료 하였습니다!!")
