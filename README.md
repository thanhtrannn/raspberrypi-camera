# Doorbell Surveillance with Facial Recognition
Doorbell with multiple features that utilizes facial recognition. Raspberry Pi with breadboard, camera and motion sensor module, facial recognition algorithms and library in Python, and Apache to host website to show live feed.

## Prerequisites
### Hardware
* ABOX Raspberry Pi 3 B+ Ultimate Sttarter Kit ([link])(https://www.amazon.ca/gp/product/B07DGFH76Y/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)
* Aukru HC-SR501 Human Body Pyroelectricity Infrared PIR Motion Detector Sensor Module ([link])(https://www.amazon.ca/gp/product/B019SX734A/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1)
* SainSmart Camera Module Board 5MP Webcam ([link])(https://www.amazon.ca/gp/product/B00FGKYHXA/ref=ppx_yo_dt_b_asin_title_o08_s00?ie=UTF8&psc=1)
* Breadboard
* Breadboard Jumper Wire
* LED

### Environment and Tools
* **OS:** Raspbian
* **IDE:** PyCharm
* **Web Host:** Apache

### Languages
Python 3.6, PHP, HTML5, CSS3, JavaScript, jQuery, Bootstrap

### Python Dependencies
* imutils - Image processing
* picamera - Interface for camera module
* face_recognition - facial recognition library
* twilio.rest - Interaction with Twilio API
* gpiozero - interface to GPIO devices (Motion sensor, LED)

## Code
### Main.py
* **Facial Recognition:** Refer to the guide [here](https://www.pyimagesearch.com/2018/06/25/raspberry-pi-face-recognition/)
* Use Twilio API to send text message and email of the live camera feed to the owner, whe unidentified person is at the door
* Live stream of camera to website
* LED toggles depending on state of recognition
* Motion detection configuration

### encodes_faces.py
* Takes 5 pictures over 20 seconds and store in directory()
* Insert or updates (if parameters already exist) the database with new sets of photos

### Index.php
Site to view camera feed and contain functions for interaction:

* Text-to-speech through and input form submission (WIP)
    * Uses espeak module
    * sudo is required to run python scripts through webpage
    * sudo does not work with espeak on our raspberry pi

* Remotely add user to database by running encodes_faces.py
  * Requires parameter to set firstname_lastname

## Installing and Deployment
1. Install Raspbian (OS) to Raspberry Pi and update required kernals
1. Ensure all hardware are properly installed and working
    * Breadboard connectivity ([link])(https://thepihut.com/blogs/raspberry-pi-tutorials/27968772-turning-on-an-led-with-your-raspberry-pis-gpio-pins)
1. With python, test connectivity of module with above dependencies
1. Run encodes_face.py to create database of person/people
1. Add Twilio credentials with email and phone number in Main.py
1. Set startup to run Main.py on reboot
1. Deploy Index.php to Apache and set network configuration


## Author
**[Thanh Tran](https://github.com/thanhtrannn)**
**[David Nguyen](https://github.com/HalfLife7)**
