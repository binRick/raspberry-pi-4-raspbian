import RPi.GPIO as GPIO
import sys, termios, tty, os, time
import enum
from threading import Thread
from TankLib import TankLib

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
 
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def main():
    print(f'Initializing Tank')
    my_tank = TankLib()
    print(f'Initialized Tank')
    #my_tank.gimbal_x_angle = 40
    #my_tank.gimbal_y_angle = 0
    #my_tank.gimbal_y(0)
    #my_tank.gimbal_x(0)
    while True:
        char = getch()
        if(char == "a"):
            my_tank.spin_left(0.1)
        elif(char == "d"):
            my_tank.spin_right(0.1)
        elif(char == "s"):
            my_tank.reverse(0.1)
        elif(char == "z"):
            my_tank.brake()
        elif(char == "w"):
            my_tank.forward(0.1)
        elif(char == "b"):
            my_tank.beep(0.5)
        elif(char == "i"):
            #my_tank.gimbal_y(5)
            my_tank.gimbal_y_servo_right()
        elif(char == "k"):
            #my_tank.gimbal_y(-5)
            my_tank.gimbal_y_servo_left()
        elif(char == "j"):
            my_tank.gimbal_x_servo_right()
            #my_tank.gimbal_x(5)
        elif(char == "l"):
            my_tank.gimbal_x_servo_left()
            #my_tank.gimbal_x(-5)
        elif(char == "r"):
            my_tank.toggle_led()
        elif(char == "x"):
            my_tank.sonar_servo_left()
        elif(char == "c"):
            my_tank.sonar_servo_right()
        elif(char == "u"):
            dist = my_tank.get_sonar_distance()
            print(f'distance [{my_tank.SONAR_POS}]: {dist}')
        elif(char == "o"):
            print(f'stopping polling distance')
            my_tank.stop_poll_sonar_distance()
            print(f'stopped polling distance')
        elif(char == "O"):
            my_tank.stop_sonar_sweep()
        elif(char == "p"):
            print(f'polling distance')
            my_tank.poll_sonar_distance()
        elif(char == "P"):
            my_tank.start_sonar_sweep()
        elif(char == "q"):
            exit(0)
main()
if __name__ == "main":
    main()
