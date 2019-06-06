from adafruit_servokit import ServoKit
import time

hat1 = ServoKit(channels=16,address=0x40)
#hat2 = ServoKit(channels=16,address=0x41)

hat1.servo[0].angle = 110
#hat2.servo[0].angle = 110

time.sleep(2)

hat1.servo[0].angle = 90
#hat2.servo[0].angle = 90

exit()
