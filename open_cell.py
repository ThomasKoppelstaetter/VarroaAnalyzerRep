import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
pwm_gpio = 12
frequence = 50

GPIO.setup(pwm_gpio, GPIO.OUT)
pwm = GPIO.PWM(pwm_gpio, frequence)

pwm.start(2.5)
time.sleep(.2)

pwm.ChangeDutyCycle(10)
time.sleep(.5)

pwm.ChangeDutyCycle(2.5)
time.sleep(.5)

pwm.stop()
GPIO.cleanup(pwm_gpio)
