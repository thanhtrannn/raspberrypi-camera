import argparse
from subprocess import call

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--text",
                    help="text to use for text to speech")
args = vars(ap.parse_args())

print(args["text"])

call("espeak " + args["text"] + " 2>/dev/null", shell=True)

#call("espeak test 2>/dev/null", shell=True)