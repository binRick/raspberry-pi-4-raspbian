import RPi.GPIO as GPIO, time, typing, os, sys, json, threading, term, queue
from TankMath import sampler as sonar_sampler
from TankPosition import TankPosition
from TankGPS import TankGPS

class ServoController(object):
    PIN = 9
    POS_MIN = 0
    POS_MAX = 180
    POS = 20
    THREAD = None
    LAST_UPDATE = None
    SET_STILL_AFTER = 0.50
    LOCK = threading.Lock()
    QUEUE = queue.Queue()
    SWEEP = 5
    servo = None
    SWEEP = 5

    def __init__(self, pin=0, name=None, min=None, max=None, pos=None, sweep=None):
        self.NAME = name
        self.PIN = pin
        if sweep:
            self.SWEEP = sweep
        if min:
            self.POS_MIN = min
        if max:
            self.POS_MAX = min
        if pos:
            self.POS = pos
        self.servo = GPIO.PWM(self.PIN, 50)
        self.set_servo()

    def get_servo(self):
        return self.POS

    def set_servo(self):
        self.QUEUE.put(self.SONAR_POS)
        self.LAST_UPDATE = time.time()
        if not self.THREAD:
            threading.Thread(target=self._set_still, daemon=True).start()
            self.THREAD = threading.Thread(target=self._set_servo, daemon=True)
            self.THREAD.start()

    def _set_still(self):
        while True:
            with self.LOCK:
                if self.LAST_UPDATE and (time.time() - self.LAST_UPDATE) > self.SET_STILL_AFTER:
                    self.servo.ChangeDutyCycle(0)            
            time.sleep(0.30)

    def _set_servo(self):
        while True:
            pos = int(self.QUEUE.get())
            print(f'\n{self.name} pos: {pos}')
            for i in range(1):
                with self.LOCK:
                    self.servo.ChangeDutyCycle(2.5+10 * pos/100)

    def left(self):
        self.POS = self.POS + self.SONAR_SWEEP
        if self.POS > self.POS_MAX:
            self.POS = self.POS_MAX
        self.set_servo()

    def right(self):
        self.POS = self.POS - self.SWEEP
        if self.POS < self.POS_MIN:
            self.POS = self.POS_MIN
        self.set_servo()

class TankLib(object):
    IN1 = 20
    IN2 = 21
    IN3 = 19
    IN4 = 26
    ENA = 16
    ENB = 13
    buzzer_pin = 8

    speed_control = 33
    spin_speed = 50
    spin_dampen = 1

    led_r_pin = 22
    led_g_pin = 27
    led_b_pin = 24 
 
    # GIMBAL X
    gimbal_x_pin = 11
    GIMBAL_X_POS = 40
    GIMBAL_X_POS_MIN = 0
    GIMBAL_X_POS_MAX = 180
    GIMBAL_X_THREAD = None
    GIMBAL_X_LAST_UPDATE = None
    GIMBAL_X_SET_STILL_AFTER = 0.50
    GIMBAL_X_LOCK = threading.Lock()
    GIMBAL_X_QUEUE = queue.Queue()
    GIMBAL_X_SWEEP = 5

    # GIMBAL Y
    gimbal_y_pin = 9
    GIMBAL_Y_POS_MIN = 0
    GIMBAL_Y_POS_MAX = 180
    GIMBAL_Y_POS = 20
    GIMBAL_Y_THREAD = None
    GIMBAL_Y_LAST_UPDATE = None
    GIMBAL_Y_SET_STILL_AFTER = 0.50
    GIMBAL_Y_LOCK = threading.Lock()
    GIMBAL_Y_QUEUE = queue.Queue()
    GIMBAL_Y_SWEEP = 5

    #  SONAR
    SONAR_PIN = 23
    SONAR_ECHO = 0
    SONAR_TRIG = 1
    SONAR_SWEEP = 5
    SONAR_START_POS = 45
    SONAR_SWEEP_ENABLED = False
    SONAR_SWEEP_INTERVAL = 0.2
    SONAR_POS = SONAR_START_POS
    SONAR_POS_MIN = 0
    SONAR_POS_MAX = 90
    SONAR_MAX_DISTANCE_CM = 300
    SONAR_POLL_INTERVAL = 0.1
    SONAR_POLL_THREAD = None
    SONAR_POLL_THREAD_ENABLED = None
    SONAR_POLL_SAMPLER = sonar_sampler(int(1/SONAR_POLL_INTERVAL*5), SONAR_MAX_DISTANCE_CM)
    SONAR_DISTANCES = {}
    SONAR_QUEUE = queue.Queue()
    SONAR_THREAD = None
    SONAR_LAST_UPDATE = None
    SONAR_SET_STILL_AFTER = 0.50
    SONAR_LOCK = threading.Lock()

    #  GPS
    GPS = None

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
    def __init__(self):
        GPIO.setwarnings(False)

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
        self.gimbal_y_servo = GPIO.PWM(self.gimbal_y_pin, 50)
        self.gimbal_x_servo = GPIO.PWM(self.gimbal_x_pin, 50)
        #self.pwm_FrontServo.start(0)
        self.gimbal_y_servo.start(0)
        self.gimbal_x_servo.start(0)
        self.pwm_r_led = GPIO.PWM(self.led_r_pin, 1000)
        self.pwm_g_led = GPIO.PWM(self.led_g_pin, 1000)
        self.pwm_b_led = GPIO.PWM(self.led_b_pin, 1000)
        self.pwm_r_led.start(0)
        self.pwm_g_led.start(0)
        self.pwm_b_led.start(0)

        # center sonar
        self.set_sonar_servo()

        # center gimbal
        self.set_gimbal_x_servo()
        self.set_gimbal_y_servo()

        # center gimbal
        #self.set_gimbal_y(self.GIMBAL_Y_POS)
        #self.set_gimbal_x(self.GIMBAL_X_POS)

        # global servo vars
        SERVO_MAX_SWEEP_TIME = 0.30

        # start positioning routine
        # self.tank_position = TankPosition()
        # self.position = self.tank_position.info()

        #  GPS
        #self.GPS = TankGPS()
        #print(self.GPS.info())
        
    def start_sonar_sweep(self):
      self.poll_sonar_distance()
      SONAR_SWEEP_ENABLED = True
      while self.SONAR_SWEEP_ENABLED:
          my_tank.sonar_servo_left()
          time.sleep(self.SONAR_SWEEP_INTERVAL)

    def stop_sonar_sweep(self):
      SONAR_SWEEP_ENABLED = False
      self.stop_poll_sonar_distance()

    def stop_poll_sonar_distance(self):
     if self.SONAR_POLL_THREAD is not None:
       self.SONAR_POLL_THREAD_ENABLED = False
     term.saveCursor()
     term.clearLine()
     term.restoreCursor()

    def poll_sonar_distance(self):
        self.SONAR_POLL_THREAD_ENABLED = True
        if self.SONAR_POLL_THREAD is None:
            self.SONAR_POLL_THREAD = threading.Thread(target=self.__poll_sonar_distance, daemon=True)
            self.SONAR_POLL_THREAD.start()

    def __poll_sonar_distance(self):
        while self.SONAR_POLL_THREAD_ENABLED:
            size = os.get_terminal_size()
            d = self.get_sonar_distance()
            msg = f"Sonar Distance: {d}cm @{self.get_sonar_servo()} | {len(self.SONAR_DISTANCES)} Distances"
            y = 0
            x = size.columns-len(msg)-10
            term.saveCursor()
            term.clearLine()
            term.clearLineToPos()
            term.pos(y, x)
            term.writeLine(msg, term.green, term.reverse)
            
            '''
            msg1 = f'{len(self.SONAR_DISTANCES)} Distances'
            term.down(value=1)
            term.clearLine()
            term.clearLineToPos()
            term.pos(1, x)
            term.writeLine(msg1, term.green, term.reverse)
            '''


            term.restoreCursor()

            time.sleep(self.SONAR_POLL_INTERVAL)
        self.SONAR_POLL_THREAD = None


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
      d = int(((t2 - t1)* 340 / 2) * 100)
      self.SONAR_DISTANCES[self.get_sonar_servo()] = d
      return d

    def get_sonar_servo(self):
        return self.SONAR_POS

    def set_sonar_servo(self):
        self.SONAR_QUEUE.put(self.SONAR_POS)
        self.SONAR_LAST_UPDATE = time.time()
        if not self.SONAR_THREAD:
            threading.Thread(target=self._set_sonar_still, daemon=True).start()
            self.SONAR_THREAD = threading.Thread(target=self._set_sonar_servo, daemon=True)
            self.SONAR_THREAD.start()

    def _set_sonar_still(self):
        while True:
            with self.SONAR_LOCK:
                if self.SONAR_LAST_UPDATE and (time.time() - self.SONAR_LAST_UPDATE) > self.SONAR_SET_STILL_AFTER:
                    self.sonar_servo.ChangeDutyCycle(0)            
            time.sleep(0.30)

    def _set_sonar_servo(self):
        while True:
            pos = int(self.SONAR_QUEUE.get())
            print(f'\nsonar pos: {pos}')
            for i in range(1):
                with self.SONAR_LOCK:
                    self.sonar_servo.ChangeDutyCycle(2.5+10 * pos/100)

    def sonar_servo_left(self):
        self.SONAR_POS = self.SONAR_POS + self.SONAR_SWEEP
        if self.SONAR_POS > self.SONAR_POS_MAX:
            self.SONAR_POS = self.SONAR_POS_MAX
        self.set_sonar_servo()

    def sonar_servo_right(self):
        self.SONAR_POS = self.SONAR_POS - self.SONAR_SWEEP
        if self.SONAR_POS < self.SONAR_POS_MIN:
            self.SONAR_POS = self.SONAR_POS_MIN
        self.set_sonar_servo()

    def gimbal_y_servo_left(self):
        self.GIMBAL_Y_POS = self.GIMBAL_Y_POS + self.GIMBAL_Y_SWEEP
        if self.GIMBAL_Y_POS > self.GIMBAL_Y_POS_MAX:
            self.GIMBAL_Y_POS = self.GIMBAL_Y_POS_MAX
        self.set_gimbal_y_servo()

    def gimbal_y_servo_right(self):
        self.GIMBAL_Y_POS = self.GIMBAL_Y_POS - self.GIMBAL_Y_SWEEP
        if self.GIMBAL_Y_POS < self.GIMBAL_Y_POS_MIN:
            self.GIMBAL_Y_POS = self.GIMBAL_Y_POS_MIN
        self.set_gimbal_y_servo()

    def _set_gimbal_y_still(self):
        while True:
            with self.GIMBAL_Y_LOCK:
                if self.GIMBAL_Y_LAST_UPDATE and (time.time() - self.GIMBAL_Y_LAST_UPDATE) > self.GIMBAL_Y_SET_STILL_AFTER:
                    self.gimbal_y_servo.ChangeDutyCycle(0)            
            time.sleep(0.30)

    def _set_gimbal_y_servo(self):
        while True:
            pos = int(self.GIMBAL_Y_QUEUE.get())
            print(f'\ngimbal y pos: {pos}')
            for i in range(1):
                with self.GIMBAL_Y_LOCK:
                    self.gimbal_y_servo.ChangeDutyCycle(2.5+10 * pos/100)

    def set_gimbal_y_servo(self):
        self.GIMBAL_Y_QUEUE.put(self.GIMBAL_Y_POS)
        self.GIMBAL_Y_LAST_UPDATE = time.time()
        if not self.GIMBAL_Y_THREAD:
            threading.Thread(target=self._set_gimbal_y_still, daemon=True).start()
            self.GIMBAL_Y_THREAD = threading.Thread(target=self._set_gimbal_y_servo, daemon=True)
            self.GIMBAL_Y_THREAD.start()

    def gimbal_x_servo_left(self):
        self.GIMBAL_X_POS = self.GIMBAL_X_POS + self.GIMBAL_X_SWEEP
        if self.GIMBAL_X_POS > self.GIMBAL_X_POS_MAX:
            self.GIMBAL_X_POS = self.GIMBAL_X_POS_MAX
        self.set_gimbal_x_servo()

    def gimbal_x_servo_right(self):
        self.GIMBAL_X_POS = self.GIMBAL_X_POS - self.GIMBAL_X_SWEEP
        if self.GIMBAL_X_POS < self.GIMBAL_X_POS_MIN:
            self.GIMBAL_X_POS = self.GIMBAL_X_POS_MIN
        self.set_gimbal_x_servo()

    def _set_gimbal_x_still(self):
        while True:
            with self.GIMBAL_X_LOCK:
                if self.GIMBAL_X_LAST_UPDATE and (time.time() - self.GIMBAL_X_LAST_UPDATE) > self.GIMBAL_X_SET_STILL_AFTER:
                    self.gimbal_x_servo.ChangeDutyCycle(0)            
            time.sleep(0.30)

    def _set_gimbal_x_servo(self):
        while True:
            pos = int(self.GIMBAL_X_QUEUE.get())
            print(f'\ngimbal x pos: {pos}')
            for i in range(1):
                with self.GIMBAL_X_LOCK:
                    self.gimbal_x_servo.ChangeDutyCycle(2.5+10 * pos/100)

    def set_gimbal_x_servo(self):
        self.GIMBAL_X_QUEUE.put(self.GIMBAL_X_POS)
        self.GIMBAL_X_LAST_UPDATE = time.time()
        if not self.GIMBAL_X_THREAD:
            threading.Thread(target=self._set_gimbal_x_still, daemon=True).start()
            self.GIMBAL_X_THREAD = threading.Thread(target=self._set_gimbal_x_servo, daemon=True)
            self.GIMBAL_X_THREAD.start()

    def forward(self, active_time:float):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(self.speed_control)
        self.pwm_ENB.ChangeDutyCycle(self.speed_control)
        time.sleep(active_time)
        self.brake()

    def reverse(self, active_time:float):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(self.speed_control)
        self.pwm_ENB.ChangeDutyCycle(self.speed_control)
        time.sleep(active_time)
        self.brake()

            
    def left(self, active_time:float):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(self.speed_control)
        self.pwm_ENB.ChangeDutyCycle(self.speed_control)
        time.sleep(active_time)
        self.brake()

    def right(self, active_time:float):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(self.speed_control)
        self.pwm_ENB.ChangeDutyCycle(self.speed_control)
        time.sleep(active_time)
        self.brake()
            
    def spin_left(self, active_time:float):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(self.spin_speed*self.spin_dampen)
        self.pwm_ENB.ChangeDutyCycle(self.spin_speed*self.spin_dampen)
        time.sleep(active_time)
        self.brake()

    def spin_right(self, active_time:float):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(self.spin_speed*self.spin_dampen)
        self.pwm_ENB.ChangeDutyCycle(self.spin_speed*self.spin_dampen)
        time.sleep(active_time)
        self.brake()

    def brake(self):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

        

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

