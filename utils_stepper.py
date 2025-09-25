import RPi.GPIO as GPIO
import time

# Pins für X-, Y- und Z-Achse
enx, dirx, stepx = 16, 20, 21
eny, diry, stepy = 8, 7, 1
enz, dirz, stepz = 10, 9, 11

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Pins für die X-Achse
    GPIO.setup(enx, GPIO.OUT)
    GPIO.setup(dirx, GPIO.OUT)
    GPIO.setup(stepx, GPIO.OUT)

    # Pins für die Y-Achse
    GPIO.setup(eny, GPIO.OUT)
    GPIO.setup(diry, GPIO.OUT)
    GPIO.setup(stepy, GPIO.OUT)

    # Pins für die Z-Achse
    GPIO.setup(enz, GPIO.OUT)
    GPIO.setup(dirz, GPIO.OUT)
    GPIO.setup(stepz, GPIO.OUT)

    # Motoren "aktivieren"
    GPIO.output(enx, GPIO.HIGH)
    GPIO.output(eny, GPIO.HIGH)
    GPIO.output(enz, GPIO.HIGH)
def shutdown():
    try:
        cleanup_gpios = [dirx, stepx, diry, stepy, dirz, stepz]
        GPIO.cleanup(cleanup_gpios)
    except Exception as e:
        print(e)
    GPIO.output(enz, GPIO.HIGH)
    GPIO.output(eny, GPIO.HIGH)
    GPIO.output(enx, GPIO.HIGH)

# runMM_xyz("TRUE" oder "FALSE", "Distance in mm")
def runMM_x(direction, distance):
    steps = distance * 50
    GPIO.output(enx, GPIO.LOW)
    if (direction == True):
        print("x-direction: " + str(direction) + ", distance: " + str(distance) + " mm")
        GPIO.output(dirx, GPIO.HIGH)
        for step_counter in range(steps):
            GPIO.output(stepx, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(stepx, GPIO.LOW)
            time.sleep(0.001)
    elif (direction == False):
        print("x-direction: " + str(direction) + ", distance: " + str(distance) + " mm")
        GPIO.output(dirx, GPIO.LOW)
        for step_counter in range(steps):
            GPIO.output(stepx, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(stepx, GPIO.LOW)
            time.sleep(0.001)
    else:
        print("Direction Error")
    GPIO.output(enx, GPIO.HIGH)
def runMM_y(direction, distance):
    GPIO.output(eny, GPIO.LOW)
    steps = distance * 50
    if (direction == True):
        print("y-direction: " + str(direction) + ", distance: " + str(distance) + " mm")
        GPIO.output(diry, GPIO.HIGH)
        for step_counter in range(steps):
            GPIO.output(stepy, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(stepy, GPIO.LOW)
            time.sleep(0.001)
    elif (direction == False):
        print("y-direction: " + str(direction) + ", distance: " + str(distance) + " mm")
        GPIO.output(diry, GPIO.LOW)
        for step_counter in range(steps):
            GPIO.output(stepy, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(stepy, GPIO.LOW)
            time.sleep(0.001)
    else:
        print("Direction Error")
    GPIO.output(eny, GPIO.HIGH) 
def runMM_z(direction, distance):
    GPIO.output(enz, GPIO.LOW)
    steps = distance * 50
    if (direction == True):
        print("z-direction: " + str(direction) + ", distance: " + str(distance) + " mm")
        GPIO.output(dirz, GPIO.HIGH)
        for step_counter in range(steps):
            GPIO.output(stepz, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(stepz, GPIO.LOW)
            time.sleep(0.001)
    elif (direction == False):
        print("z-direction: " + str(direction) + ", distance: " + str(distance) + " mm")
        GPIO.output(dirz, GPIO.LOW)
        for step_counter in range(steps):
            GPIO.output(stepz, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(stepz, GPIO.LOW)
            time.sleep(0.001)
    else:
        print("Direction Error")
    GPIO.output(enz, GPIO.HIGH)

# runCell_xy("TRUE" oder "FALSE", "Number of Honeycomb Cells")
def runCell_x(direction, distance):
    steps = distance * 270
    GPIO.output(enx, GPIO.LOW)
    if (direction == True):
        print("x-direction: " + str(direction) + ", distance: " + str(distance) + " Cell")
        GPIO.output(dirx, GPIO.HIGH)
        for step_counter in range(steps):
            GPIO.output(stepx, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(stepx, GPIO.LOW)
            time.sleep(0.001)
    elif (direction == False):
        print("x-direction: " + str(direction) + ", distance: " + str(distance) + " Cell")
        GPIO.output(dirx, GPIO.LOW)
        for step_counter in range(steps):
            GPIO.output(stepx, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(stepx, GPIO.LOW)
            time.sleep(0.001)
    else:
        print("Direction Error")
    GPIO.output(enx, GPIO.HIGH)
def runCell_y(direction, distance):
    GPIO.output(eny, GPIO.LOW)
    steps = distance * 250
    if (direction == True):
        print("y-direction: " + str(direction) + ", distance: " + str(distance) + " Cell")
        GPIO.output(diry, GPIO.HIGH)
        for step_counter in range(steps):
            GPIO.output(stepy, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(stepy, GPIO.LOW)
            time.sleep(0.001)
    elif (direction == False):
        print("y-direction: " + str(direction) + ", distance: " + str(distance) + " Cell")
        GPIO.output(diry, GPIO.LOW)
        for step_counter in range(steps):
            GPIO.output(stepy, GPIO.HIGH)
            time.sleep(0.001)
            GPIO.output(stepy, GPIO.LOW)
            time.sleep(0.001)
    else:
        print("Direction Error")
    GPIO.output(eny, GPIO.HIGH) 
