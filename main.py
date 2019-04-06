# USAGE
# python pi_face_recognition.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
from gpiozero import MotionSensor, LED
from signal import pause
import time
import subprocess
from twilio.rest import Client
import smtplib, ssl
from account import password, account_sid, auth_token

#Author: from pyimagesearch.com - pyimagesearch.com/2018/06/25/raspberry-pi-face-recognition/
#Function Name: facialDetectionStream
#What does it do?: Turns on camera stream for 15 seconds and uses facial recognition algorithm
# to detect if faces detected are in the database or not.
#Parameters: None
#Date: April 1, 2019
#Returns: array with names of faces detected while video stream was running

def facialDectectionStream():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--cascade", default="haarcascade_frontalface_default.xml",
                    help="path to where the face cascade resides")
    ap.add_argument("-e", "--encodings", default="encodings.pickle",
                    help="path to serialized db of facial encodings")
    args = vars(ap.parse_args())

    # load the known faces and embeddings along with OpenCV's Haar
    # cascade for face detection
    print("[INFO] loading encodings + face detector...")
    data = pickle.loads(open(args["encodings"], "rb").read())
    detector = cv2.CascadeClassifier(args["cascade"])

    # initialize the video stream and allow the camera sensor to warm up
    print("[INFO] starting video stream...")
    # vs = VideoStream(src=0).start()
    vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)

    #global variable to hold what faces were detected
    faceDetected = []
    
    #start timer
    start = time.time()
    
    
    # start the FPS counter
    fps = FPS().start()

    # loop over frames from the video file stream
    while True:
        # grab the frame from the threaded video stream and resize it
        # to 500px (to speedup processing)
        frame = vs.read()
        frame = imutils.resize(frame, width=500)

        # convert the input frame from (1) BGR to grayscale (for face
        # detection) and (2) from BGR to RGB (for face recognition)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # detect faces in the grayscale frame
        rects = detector.detectMultiScale(gray, scaleFactor=1.1,
                                          minNeighbors=5, minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)

        # OpenCV returns bounding box coordinates in (x, y, w, h) order
        # but we need them in (top, right, bottom, left) order, so we
        # need to do a bit of reordering
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

        # compute the facial embeddings for each face bounding box
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(data["encodings"],
                                                     encoding)
            name = "Unknown"

            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name = max(counts, key=counts.get)

            # update the list of names
            names.append(name)
            if name not in (faceDetected):
                faceDetected.append(name)


        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(boxes, names):
            # draw the predicted face name on the image
            cv2.rectangle(frame, (left, top), (right, bottom),
                          (0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, (0, 255, 0), 2)

        # display the image to our screen
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF


        # break the camera stream after 15 seconds
        end = time.time()
        timeElapsed = end - start
        if timeElapsed > 15:
            break

        # update the FPS counter
        fps.update()

    # stop the timer and display FPS information
    fps.stop()

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()

    return(faceDetected)

#Author: David Nguyen
#Function Name: sendTextMessage
#Parameters: msg - message for text and email
#Date: April 1, 2019
#Returns: Message sent to phone number
def sendTextMessage(msg):
    # account_side and auth_token taken and set in account.py
    client = Client(account_sid, auth_token)
    twilio_number = "+12897780212"
    number_toSend = "+19059215160"
    try:
        print("Message sent successfully")
        message = client.messages.create(body = msg,from_ = twilio_number,to = number_toSend)
    except:
        print("Message failed")
        # print(message.sid)
    return

#Author: Thanh Tran
#Function Name: sendEmail
#Parameters: msg - message for text and email
#Date: April 1, 2019
#Returns: Email sent to email
def sendEmail(msg):
    port = 465
    sender_email = "tmantmang@gmail.com"
    Subject = "Unknown Person At The Door"
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (sender_email, sender_email, Subject, msg )
    context = ssl.create_default_context()
    try:
        # Use gmail server to send email to self
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                # password taken and set in account.py
                server.login(sender_email, password)
                server.sendmail(sender_email, sender_email, message)
    except:
        print("Email failed")       
    return

#Author: David Nguyen
#Function Name: toggleStream
#Parameters: status - weather to turn on and off camera for streaming purposes
#Date: April 1, 2019
#Returns: signal to toggle camera
def toggleStream(status):
    if status == "ON":
        subprocess.call (["sudo", "service", "motion", "start"])
        time.sleep(2)
        subprocess.call (["sudo", "motion"])
        time.sleep(30)
    elif status == "OFF":
        subprocess.call (["sudo", "service", "motion", "stop"])
    return

#Author: Thanh Tran
#Function Name: toggleLED
#Parameters: led - led gpio object, status - weather to turn on and off LED
#Date: April 1, 2019
#Returns: signal to toggle LED
def toggleLED(led, status):
    if status == "ON":
        return led.on()
    elif status == "OFF":
        return led.off()

#Variables
weburl = "http://192.168.1.14" #site of hosted site
msg = "Check who's at your door: " + weburl

#GPIO variables
pir = MotionSensor(4)
led = LED(18)
ledyellow = LED(21)
ledred= LED(16)

#Main Program STARTS
#script to keep running and make motion detector active
while True:
    if pir.motion_detected:
        toggleLED(led, "ON")
        facesDetected = facialDectectionStream()
        if "unknown" in facesDetected and len(facesDetected) == 1 or len(facesDetected) == 0:
            # Send text to notify user of unknown presence
            # sendTextMessage(msg)
            # Send email to notify user of unknown presence
            sendEmail(msg)
            toggleLED(ledred, "ON")
        else:
            toggleLED(ledyellow, "ON")
        toggleStream("ON")
    else:
        # Reset facesDetected list as it is used to determine
        facesDetected = []
        toggleLED(led, "OFF")
        toggleLED(ledred, "OFF")
        toggleLED(ledyellow, "OFF")
        toggleStream("OFF")


