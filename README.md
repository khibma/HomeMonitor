HomeMonitor
===========

python code for raspberry pi, webcam, temp sensor to watch house and send emails

Setup:

sudo apt-get install python-smbus

sudo apt-get install i2c-tools

sudo apt-get install motion

sudo nano /etc/motion/motion.conf

width = 640

height = 480

threshold = 3000

quality 100

target_dir /home/pi/Monitor


sudo mkdir Monitor


----------
BOOT Script
----------
sudo nano /etc/init.d/HM

--paste code in

sudo chmod +x /etc/init.d/HM

sudo update-rc.d HM defaults



Links:
Temperature Sensor
http://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/overview

Dropbox:
http://raspi.tv/2013/how-to-use-dropbox-with-raspberry-pi
>git clone https://github.com/andreafabrizi/Dropbox-Uploader.git

>./dropbox_uploader.sh upload /home/pi/name_of_upload_file
