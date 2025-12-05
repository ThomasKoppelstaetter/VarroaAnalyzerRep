import time
import utils_stepper

try:
    utils_stepper.setup()
    while True:
        utils_stepper.runMM_x(True, 10)
        time.sleep(1)
        utils_stepper.runMM_x(False, 10)
        time.sleep(1)
        utils_stepper.runMM_y(True, 10)
        time.sleep(1)
        utils_stepper.runMM_y(False, 10)
        time.sleep(1)
        # utils_stepper.runMM_z(False, 10)
        # time.sleep(1)
        # utils_stepper.runMM_z(True,10)
        # time.sleep(1)
except KeyboardInterrupt:
    print(" Programm beendet")
    utils_stepper.shutdown()
    
