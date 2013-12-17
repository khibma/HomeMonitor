import os, sys
import glob
import time
import datetime

photos = []
dailyFlag = True

def read_temp_raw():
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c #, temp_f
    
def check4newPhoto():
    
    localPhotos = glob.glob("*.jpg")
    
    global photos
    
    newPhotos = set(localPhotos).difference(photos)
    if len(newPhotos) > 0:
        new = True
        photos = localPhotos
    else:
        new = False
    
    return new, newPhotos

def sendEmail(temp, photos):
    
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage
    
    msg = MIMEMultipart()
    TO = 'xxx@gmail.com'
    msg['Subject'] = "Report from the House!" 
    
    # Gmail Sign In
    gmail_sender = 'xxx@gmail.com'
    gmail_passwd = 'xxx'
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)
    
    msgBody = "The house is {}c".format(temp)
    msgText = MIMEText(msgBody , 'html')
    msg.attach(msgText)   
    
    # Attach any new photos
    if photos is not None:
        for photo in photos:
            
            fp = open(os.path.join(sys.path[0],photo), 'rb')                                                    
            img = MIMEImage(fp.read())
            fp.close()
            img.add_header('Content-ID', '<{}>'.format(str(photo)))
            msg.attach(img)    
            
    try:
        server.sendmail(gmail_sender, [TO], msg.as_string() ) #BODY)
        print ('email sent')
        server.quit()
    except:
        print ('error sending mail')
    
    

if __name__ == "__main__":

    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    # When it gets below this value, send an email
    tempTheshold = 10
    global dailyFlag

    now = datetime.datetime.now()
    temp = read_temp()
    
    # Loop forever
    while True:

        #Every 1 minute, check the temperature and email if its to low.
        compare = datetime.datetime.now() - now
        if compare.seconds > 60:
            temp = read_temp()
            now = datetime.datetime.now()

            if temp < tempTheshold:
                sendEmail(temp, None)
                print "ITS COLD: {}C".format(temp)
        
        # Check for a new photo. New photo is handled by 'motion'
        newPhotoFlag, photoList = check4newPhoto()
        if newPhotoFlag:
            sendEmail(temp, photoList)
        
        #daily temperature send
        if now.hour == 12 and dailyFlag:
            sendEmail(temp, None)
            dailyFlag = False
        if now.hour == 1:
            dailyFlag = True
        
        #Check every 10 seconds.
        time.sleep(10)
        print temp