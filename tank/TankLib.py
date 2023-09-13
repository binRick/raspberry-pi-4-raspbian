import RPi.GPIO as GPIO, time, typing, os, sys, json
from threading import Thread

class TankLib:
    #Motor pin definition
    IN1 = 20
    IN2 = 21
    IN3 = 19
    IN4 = 26
    ENA = 16
    ENB = 13
    buzzer_pin = 8

    speed_control = 33
    spin_speed = 50
    #How much we should slow down our spin speed 0..1
    spin_dampen = 1
    """#Button pin definition
    button_Pin = 8

    #Ultrasonic pin definition
    echo_pin = 0
    trigger_pin = 1
    """
    #RGB LED pin definition
    led_r_pin = 22
    led_g_pin = 27
    led_b_pin = 24 
    
    #Servo pin definition
    SONAR_PIN = 23
    gimbal_y_pin = 9
    gimbal_x_pin = 11
    GIMBAL_X_POS = 45
    GIMBAL_Y_POS = 20
    GIMBAL_X_POS_MIN = 0
    GIMBAL_X_POS_MAX = 180
    GIMBAL_Y_POS_MIN = 0
    GIMBAL_Y_POS_MAX = 180

    # sonar pins
    SONAR_ECHO = 0
    SONAR_TRIG = 1

    # sonar left/right sweep len
    SONAR_SWEEP = 5
    SONAR_POS = 45
    SONAR_POS_MIN = 0
    SONAR_POS_MAX = 90


    """
    #Infrared obstacle avoidance pin definition
    avoid_left_pin = 12
    avoid_right_pin = 17

    #Buzzer pin definition
    buzzer_pin = 8

    outfire_pin = 2

    #TrackSensorLeftPin1 TrackSensorLeftPin2 TrackSensorRightPin1 TrackSensorRightPin2
    #      3                 5                  4                   18
    TrackSensorLeftPin1  =  3  
    TrackSensorLeftPin2  =  5   
    TrackSensorRightPin1 =  4   
    TrackSensorRightPin2 =  18  

    LdrSensorLeft = 7
    LdrSensorRight = 6"""
    #Motor pin initialized to output mode
    #Button pin initialized to input mode
    #Ultrasonic,RGB tri-color lamp, servo pin initialization
    #Infrared obstacle avoidance pin initialization
    def __init__(self):
        GPIO.setwarnings(False)

        #Start angle for gimbal x/y of camera
        #Servos have been calibrated where 90 is 'neutral'
        self.gimbal_x_angle = 90
        self.gimbal_y_angle = 90

        #Set GPIO mode
        GPIO.setmode(GPIO.BCM)

        #Init motor pins
        GPIO.setup(self.ENA,GPIO.OUT,initial=GPIO.HIGH)
        GPIO.setup(self.IN1,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.IN2,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.ENB,GPIO.OUT,initial=GPIO.HIGH)
        GPIO.setup(self.IN3,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.IN4,GPIO.OUT,initial=GPIO.LOW)
        #Honk honk
        GPIO.setup(self.buzzer_pin,GPIO.OUT,initial=GPIO.HIGH)

        #Camera gimbal servo pins
        GPIO.setup(self.gimbal_x_pin, GPIO.OUT)
        GPIO.setup(self.gimbal_y_pin, GPIO.OUT)
        """GPIO.setup(outfire_pin,GPIO.OUT)
        GPIO.setup(echo_pin,GPIO.IN)
        GPIO.setup(trigger_pin,GPIO.OUT)
        """
        self.led_on = False
        GPIO.setup(self.led_r_pin, GPIO.OUT)
        GPIO.setup(self.led_g_pin, GPIO.OUT)
        GPIO.setup(self.led_b_pin, GPIO.OUT)

        # setup sonar servo
        GPIO.setup(self.SONAR_PIN, GPIO.OUT)
        self.sonar_servo = GPIO.PWM(self.SONAR_PIN, 50)
        self.sonar_servo.start(0)

        # setup sonar
        GPIO.setup(self.SONAR_TRIG,GPIO.OUT)
        GPIO.setup(self.SONAR_ECHO,GPIO.IN)


        """
        GPIO.setup(avoid_left_pin,GPIO.IN)
        GPIO.setup(avoid_right_pin,GPIO.IN)
        GPIO.setup(LdrSensorLeft,GPIO.IN)
        GPIO.setup(LdrSensorRight,GPIO.IN)
        GPIO.setup(TrackSensorLeftPin1,GPIO.IN)
        GPIO.setup(TrackSensorLeftPin2,GPIO.IN)
        GPIO.setup(TrackSensorRightPin1,GPIO.IN)
        GPIO.setup(TrackSensorRightPin2,GPIO.IN)"""
        
        #Set the motor pwm pins to 2000hz and start
        self.pwm_ENA = GPIO.PWM(self.ENA, 2000)
        self.pwm_ENB = GPIO.PWM(self.ENB, 2000)
        self.pwm_ENA.start(0)
        self.pwm_ENB.start(0)
        #Set the servo frequency and starting duty cycle
        #self.pwm_FrontServo = GPIO.PWM(front_servo_pin, 50)
        self.pwm_gimbal_y = GPIO.PWM(self.gimbal_y_pin, 50)
        self.pwm_gimbal_x = GPIO.PWM(self.gimbal_x_pin, 50)
        #self.pwm_FrontServo.start(0)
        self.pwm_gimbal_y.start(0)
        self.pwm_gimbal_x.start(0)
        self.pwm_r_led = GPIO.PWM(self.led_r_pin, 1000)
        self.pwm_g_led = GPIO.PWM(self.led_g_pin, 1000)
        self.pwm_b_led = GPIO.PWM(self.led_b_pin, 1000)
        self.pwm_r_led.start(0)
        self.pwm_g_led.start(0)
        self.pwm_b_led.start(0)

        # center sonar
        #self.sonar_servo.ChangeDutyCycle(2.5+10 * self.SONAR_POS/100)
        self.set_sonar_servo(self.SONAR_POS)
        self.gimbal_y(self.GIMBAL_Y_POS)
        self.gimbal_x(self.GIMBAL_X_POS)

    def get_sonar_distance(self):
      GPIO.output(self.SONAR_TRIG, GPIO.LOW)
      time.sleep(0.000002)
      GPIO.output(self.SONAR_TRIG, GPIO.HIGH)
      time.sleep(0.000015)
      GPIO.output(self.SONAR_TRIG, GPIO.LOW)
      t3 = time.time()
      while not GPIO.input(self.SONAR_ECHO):
        t4 = time.time()
        if (t4 - t3) > 0.03 :
          return -1
      t1 = time.time()
      while GPIO.input(self.SONAR_ECHO):
        t5 = time.time()
        dur = t5 - t1
        if(t5 - t1) > 0.03 :
          return -2
      t2 = time.time()
      #time.sleep(0.01)
      return int(((t2 - t1)* 340 / 2) * 100)

    def set_sonar_servo(self, pos):
        print(f'sonar pos: {pos}')
        self.sonar_servo.ChangeDutyCycle(2.5+10 * pos/100)

    def sonar_servo_left(self):
        self.SONAR_POS = self.SONAR_POS + self.SONAR_SWEEP
        if self.SONAR_POS > self.SONAR_POS_MAX:
            self.SONAR_POS = self.SONAR_POS_MAX
        self.set_sonar_servo(self.SONAR_POS)

    def sonar_servo_right(self):
        self.SONAR_POS = self.SONAR_POS - self.SONAR_SWEEP
        if self.SONAR_POS < self.SONAR_POS_MIN:
            self.SONAR_POS = self.SONAR_POS_MIN
        self.set_sonar_servo(self.SONAR_POS)

    #Move forward
    def forward(self, active_time:float):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(self.speed_control)
        self.pwm_ENB.ChangeDutyCycle(self.speed_control)
        time.sleep(active_time)
        self.brake()

    #Move Backward
    def reverse(self, active_time:float):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(self.speed_control)
        self.pwm_ENB.ChangeDutyCycle(self.speed_control)
        time.sleep(active_time)
        self.brake()

            
    #Skid left (Doesn't work well)
    def left(self, active_time:float):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(self.speed_control)
        self.pwm_ENB.ChangeDutyCycle(self.speed_control)
        time.sleep(active_time)
        self.brake()

    #Skid right (Doesn't work well)
    def right(self, active_time:float):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(self.speed_control)
        self.pwm_ENB.ChangeDutyCycle(self.speed_control)
        time.sleep(active_time)
        self.brake()
            
    #Spin to the left
    def spin_left(self, active_time:float):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(self.spin_speed*self.spin_dampen)
        self.pwm_ENB.ChangeDutyCycle(self.spin_speed*self.spin_dampen)
        time.sleep(active_time)
        self.brake()

    #Spin to the right
    def spin_right(self, active_time:float):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(self.spin_speed*self.spin_dampen)
        self.pwm_ENB.ChangeDutyCycle(self.spin_speed*self.spin_dampen)
        time.sleep(active_time)
        self.brake()

    #Stop
    def brake(self):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    #The servo rotates left or right **BY THE SPECIFIED AMOUNT**
    #If you wish to actively stabilize the servo you can call
    #this function with 0 as the amount.
    def gimbal_x(self, amount): 
        self.gimbal_x_angle += amount
        print(f"Changing gimbal to {self.gimbal_x_angle}")
        #Contraints
        if(self.gimbal_x_angle < self.GIMBAL_X_POS_MIN):
            self.gimbal_x_angle = self.GIMBAL_X_POS_MIN
        if(self.gimbal_x_angle > self.GIMBAL_X_POS_MAX):
            self.gimbal_x_angle = self.GIMBAL_X_POS_MAX
        
        for i in range(1):
            self.pwm_gimbal_x.ChangeDutyCycle(2.5 + 10 * self.gimbal_x_angle/180)
            time.sleep(0.02)
        self.pwm_gimbal_x.ChangeDutyCycle(0)            

    #The servo rotates up or down **BY THE SPECIFIED AMOUNT**
    #If you wish to actively stabilize the servo you can call
    #this function with 0 as the amount.
    def set_gimbal_x(self,pos):
        print(f"Changing camera x to {pos}")
        self.pwm_gimbal_x.ChangeDutyCycle(2.5+10 * pos/100)

    def set_gimbal_y(self,pos):
        print(f"Changing camera y to {pos}")
        self.pwm_gimbal_y.ChangeDutyCycle(2.5+10 * pos/100)

    def gimbal_y(self, amount):  
        self.gimbal_y_angle += amount
        print(f"Changing gimbal to {self.gimbal_y_angle}")
        #Contraints
        if(self.gimbal_y_angle < self.GIMBAL_Y_POS_MIN):
            self.gimbal_y_angle = self.GIMBAL_Y_POS_MIN
        if(self.gimbal_y_angle > self.GIMBAL_Y_POS_MAX):
            self.gimbal_y_angle = self.GIMBAL_Y_POS_MAX
        for i in range(1):
            self.pwm_gimbal_y.ChangeDutyCycle(2.5 + 10 * self.gimbal_y_angle/180)
            time.sleep(0.02)
        self.pwm_gimbal_y.ChangeDutyCycle(0)            
        

    #HONK
    def beep(self, active_time:float):
        GPIO.output(self.buzzer_pin, GPIO.LOW)
        time.sleep(active_time)
        GPIO.output(self.buzzer_pin, GPIO.HIGH)

    def toggle_led(self):
        if(self.led_on):
            GPIO.output(self.led_r_pin, GPIO.LOW)
            GPIO.output(self.led_g_pin, GPIO.LOW)
            GPIO.output(self.led_b_pin, GPIO.LOW)
            self.pwm_r_led.ChangeDutyCycle(0)
            self.pwm_g_led.ChangeDutyCycle(0)
            self.pwm_b_led.ChangeDutyCycle(0)

            self.led_on = False
        else:
            GPIO.output(self.led_r_pin, GPIO.HIGH)
            GPIO.output(self.led_g_pin, GPIO.HIGH)
            GPIO.output(self.led_b_pin, GPIO.HIGH)
            self.pwm_r_led.ChangeDutyCycle(100)
            self.pwm_g_led.ChangeDutyCycle(100)
            self.pwm_b_led.ChangeDutyCycle(100)

            self.led_on = True

