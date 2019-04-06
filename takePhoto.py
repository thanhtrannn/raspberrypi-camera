import picamera
import datetime
from time import sleep

#Author: David
#Function Name: takePhoto
#Parameters: none
#Date:April 3rd 2019
#Returns: none
def takePhoto():
    camera = picamera.PiCamera()

    #variable to hold current timestamp
    #format: month/day/year/hour/minute/second
    timestamp = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

    try:
        sleep(3) #warm up camera
    finally:
        #camera.start_preview() #for testing purposes, view camera stream
        sleep(1)
        #take picture and append the timestamp
        camera.capture("/home/pi/PycharmProjects/raspberrypi-camera/photoDatabase/" + timestamp + ".jpg")
        #camera.stop_preview() #for testing purposes, close camera stream
        camera.close()