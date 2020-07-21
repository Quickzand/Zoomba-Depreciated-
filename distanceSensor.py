import RPi.GPIO as GPIO
import time

distanceGlob = 0

def run():
    global distanceGlob
    try:
        GPIO.setmode(GPIO.BCM)

        TRIG = 23
        ECHO = 24

        print ("Distance Measurement In Progress")

        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)

        GPIO.output(TRIG, False)

        startTime = time.time()
        while(time.time() - startTime < 0.1):
            pass

        GPIO.output(TRIG, True)

        startTimeTwo = time.time()
        while(time.time() - startTimeTwo < 0.00001):
            pass

        GPIO.output(TRIG, False)

        while GPIO.input(ECHO)==0:
            pulse_start = time.time()

        while GPIO.input(ECHO)==1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150

        distanceGlob = distance
        return distanceGlob

    except:
        print("[-] Error")
        GPIO.cleanup()

if __name__ == "__main__":
    run()
