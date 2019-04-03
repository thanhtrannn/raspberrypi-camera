import picamera
import datetime
from time import sleep

camera = picamera.PiCamera()

#naming file with unique timestamp
timestamp = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

try:
    sleep(3)
finally:
    camera.start_preview()
    sleep(1)
    camera.capture("/home/pi/PycharmProjects/raspberrypi-camera/photoDatabase/" + timestamp + ".jpg")
    camera.stop_preview()
    camera.close()
