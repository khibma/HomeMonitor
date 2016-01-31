HomeMonitor
===========
python code for raspberry pi, webcam, temp sensor to watch house and send emails

Start here with setting up the Pi
---------------------------------
>sudo apt-get update

>sudo apt-get upgrade

>sudo raspi-config    (set timezone, locale, expand file partion, etc)

>sudo nano /etc/default/keyboard    ` 'gb' -> 'us'`

>sudo nano /etc/network/interfaces
```
#probably can comment out the rest
auto wlan0
allow-hotplug wlan0
iface wlan0 inet manual
  wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
iface default inet dhcp
```

>sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```
network={
 ssid="RouterName"
 psk="password"
}
```

Check to make sure temperature works:  (more info in links below)

>sudo modprobe w1-gpio

>sudo modprobe w1-therm

>cd /sys/bus/w1/devices

>ls

>cd 28- <tab>

>cat w1_slave

Should see: YES


>sudo apt-get install python-smbus

>sudo apt-get install motion

>sudo nano /etc/motion/motion.conf

daemon on

width = 640

height = 480

threshold = 3000

quality 100

target_dir /home/pi/Monitor

lightswitch 25

ffmpeg_cap_new off   #this disables the saving of a movie

>sudo nano /etc/default/motion

start_motion_daemon=yes


Make a directory and give motion control over it:

>sudo mkdir Monitor

>chgrp motion /home/pi/Monitor

>chmod g+rwx /home/pi/Monitor

>chmod -R g+w /home/pi/Monitor/


-----------
BOOT Script
-----------
>sudo nano /etc/init.d/HM

--get code from BOOT and paste in

--Then set permissions and update

>sudo chmod +x /etc/init.d/HM

>sudo update-rc.d HM defaults



Links:
------
Temperature Sensor
http://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/overview

Dropbox:
http://raspi.tv/2013/how-to-use-dropbox-with-raspberry-pi
>git clone https://github.com/andreafabrizi/Dropbox-Uploader.git

>./dropbox_uploader.sh upload /home/pi/name_of_upload_file

Giving motion more permissions over directory:
http://raspberrypi.stackexchange.com/questions/12378/what-permissions-does-motion-require-to-write-to-specific-directory

Setting up GMAIL:
sudo apt-get install python-pip   (or python3-pip)
sudo pip install --upgrade google-api-python-client
using by:
`
import sendGmail
sendGmail.sendEmail("to@email.com", "from@gmail.com", "subject line", "msg body", ['file1.jpg'])
`
Command line has been hardcoded to send the flag which should skip the need to open a browser and confirm the device is "ok" to send

