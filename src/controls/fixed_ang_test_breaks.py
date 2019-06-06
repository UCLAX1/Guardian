from adafruit_servokit import ServoKit

import argparse
import time

kit = ServoKit(channels=16)
#kit._pca.frequency = 50

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ang1",dest="ang1",type=float,default=0)
    parser.add_argument("--ang2",dest="ang2",type=float,default=0)
    parser.add_argument("--ang3",dest="ang3",type=float,default=0)
    parser.add_argument("--num_breaks",dest="num_breaks",type=int,default=1)

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    ang1 = args.ang1
    ang2 = args.ang2
    ang3 = args.ang3
    num_breaks = args.num_breaks

    s_ang0 = 90
    s_ang1 = 90
    s_ang2 = 90

    kit.servo[0].angle = 90
    kit.servo[1].angle = 90
    kit.servo[2].angle = 90
    
    
    for i in range(1,num_break):
        time.sleep(1)
        kit.servo[0].angle = 90 + ang1
        kit.servo[1].angle = 90 + ang2
        kit.servo[2].angle = 90 + ang3 

    
    
    time.sleep(1)
    kit.servo[0].angle = 90
    kit.servo[1].angle = 90
    kit.servo[2].angle = 90

    print("Done")
    
