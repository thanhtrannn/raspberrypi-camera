# import the necessary packages
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os
import picamera
import datetime
from time import sleep


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", default="photoDatabase",
                help="path to input directory of faces + images")
ap.add_argument("-e", "--encodings", default="encodings.pickle",
                help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="hog",
                help="face detection model to use: either `hog` or `cnn`")
# custom arguments
ap.add_argument("-n", "--name", required=True,
                help="name to add to database in the format first_last")
args = vars(ap.parse_args())

# Author: David
# Function Name: takePhoto
# Parameters: none (uses name from command line arguments)
# Date:April 3rd 2019
# Returns: none
# Function: takes 5 photos and places it in database folder


def takePhotos():
    camera = picamera.PiCamera()

    # variable to hold current timestamp
    # format: month/day/year/hour/minute/second
    timestamp = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

    # create the directory using the name from argument line
    os.mkdir("/home/pi/PycharmProjects/raspberrypi-camera/photoDatabase/" + args["name"])

    try:
        sleep(3) # warm up camera
    finally:
        x = 5
        camera.start_preview() # for testing purposes, view camera stream
        # take 5 photos, 2 seconds apart
        while x > 0:
            sleep(2)
            # take picture and append the timestamp
            camera.capture("/home/pi/PycharmProjects/raspberrypi-camera/photoDatabase/" + args["name"] + "/" + timestamp + ".jpg")
            x -= 1
        camera.stop_preview() # for testing purposes, close camera stream
        camera.close()

# Author: Adrian https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/
# Function Name: buildDatabase (originally encode_faces)
# Parameters: none (3 arguments from command line that are defaulted [dataset, encodings and detection method] )
# Date:June 18 2018
# Returns: none
# Function: goes through database folder of images and creates "encodings.pickle"
#           this 128-d face embeddings for each face
#           this file is essentially the


def buildDatabase():
    # grab the paths to the input images in our dataset
    print("[INFO] quantifying faces...")
    imagePaths = list(paths.list_images(args["dataset"]))

    # initialize the list of known encodings and known names
    knownEncodings = []
    knownNames = []

    # loop over the image paths
    for (i, imagePath) in enumerate(imagePaths):
        # extract the person name from the image path
        print("[INFO] processing image {}/{}".format(i + 1,
            len(imagePaths)))
        name = imagePath.split(os.path.sep)[-2]

        # load the input image and convert it from RGB (OpenCV ordering)
        # to dlib ordering (RGB)
        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect the (x, y)-coordinates of the bounding boxes
        # corresponding to each face in the input image
        boxes = face_recognition.face_locations(rgb,
            model=args["detection_method"])

        # compute the facial embedding for the face
        encodings = face_recognition.face_encodings(rgb, boxes)

        # loop over the encodings
        for encoding in encodings:
            # add each encoding + name to our set of known names and
            # encodings
            knownEncodings.append(encoding)
            knownNames.append(name)

    # dump the facial encodings + names to disk
    print("[INFO] serializing encodings...")
    data = {"encodings": knownEncodings, "names": knownNames}
    f = open(args["encodings"], "wb")
    f.write(pickle.dumps(data))
    f.close()


# MAIN
takePhotos()
buildDatabase()
