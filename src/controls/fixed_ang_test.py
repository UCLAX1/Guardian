from adafruit_servokit import ServoKit

import argparse
import time

kit1 = ServoKit(channels=16,address=0x40)
kit2 = ServoKit(channels=16,address=0x41)
#kit._pca.frequency = 50

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ang",dest="ang",type=float,default=0)

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    ang = args.ang

    for i in range(0,16):
        kit1.servo[i].angle = 90
    for i in range(0,16):
        kit2.servo[i].angle = 90

    time.sleep(1)

    for i in range(0,16):
        kit1.servo[i].angle = 90 + ang
    for i in range(0,16):
        kit2.servo[i].angle = 90 + ang

    time.sleep(1)

    for i in range(0,16):
        kit1.servo[i].angle = 90
    for i in range(0,16):
        kit2.servo[i].angle = 90        
    
   
    

    print("Done")
    
