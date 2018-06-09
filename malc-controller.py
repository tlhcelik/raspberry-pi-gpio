# Written By: Talha Celik
# Necmettin Erbakan Univercity
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
#from RPLCD import CharLCD
from datetime import datetime
from time import gmtime, strftime
import os
import time

#lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23])
#lcd.clear()

argv_list = ["",""]
def get_args(humidity = 30, irrigation_range = 3):
    if humidity == "--self-test":
	self_test()
	sys.exit(0)
    if len(sys.argv) < 2:
	print "[!] Use to: python malc-controller.py [min-humidity and tmep] [irrigation-range]"
 	print "[!] System Exit"
	sys.exit(0)
    else:
	argv_list[0] = int(humidity)
	argv_list[1] = int(irrigation_range)
    return argv_list

def write_log(log):
    if (os.path.isfile('log.html')):
        
        my_values = log.split('<br>')
        print my_values[0]
        print my_values[1]
        print my_values[2]
        print my_values[3]
        print my_values[4]
        print my_values[5]
        print "------------------"
        pattern = '''
        <!DOCTYPE html>
            <html>
            <head>
                <title>Uygulama Proje</title>
		<link rel='stylesheet' href='style.css'>
            </head> 
            <body>
		<div class="fullscreen-bg">
        	<video loop="true" muted="true" autoplay="true" poster="img/videoframe.jpg" class="fullscreen-bg__video">
           	<source src="bg.mp4" type="video/mp4"> 
	</video>
   		 </div>
<div class='content'>
		<center>
		<table border='5px'>
	           <th><h1>System Time</h1></th>
			<th><h1>{6}</h1></th>
		   <tr>
		        <td><h3>{0}</h3></td>
                        <td><h3>{1}</h3></td>
                    </tr>
                    <tr>
                        <td><h3>{2}</h3></td>
                        <td><h3>{3}</h3></td>
                    </tr>
                    <tr>
                        <td><h3>{4}</h3></td>
                        <td><h3>{5}</h3></td>
                    </tr>
                </table>
                </center>
</div>
            </body>
            </html>'''.format(
                my_values[0],
                my_values[1],
                my_values[2],
                my_values[3],
                my_values[4],
                my_values[5],
                str(datetime.now().strftime('%d-%m-%y %H:%M'))
            )
        f = open ('log.html','w')
        f.write(pattern)
        f.close()
    else:
        f = open('log.html','w')
        f.write(log)
        f.close


GPIO.setmode(GPIO.BOARD) # kart numarasina gore
GPIO.setwarnings(False)

#role pinleri
LIGHT_PIN = 11 # isiklandirma
HUMIDITY_PIN = 13 # nem
IRRIGATION_PIN = 15 # sulama
DHT_MODEL = 11 # dht11 modelini kullanacak
DHT_PIN = 4 # boardda 7. pin

GPIO.setup(LIGHT_PIN, GPIO.OUT) # relay 1 , light
GPIO.setup(HUMIDITY_PIN, GPIO.OUT) # relay 2 , humidity
GPIO.setup(IRRIGATION_PIN, GPIO.OUT) # relay 3 , irrigation

def clear_relay(): #roleleri kapatir
    GPIO.output(LIGHT_PIN,GPIO.HIGH)
    GPIO.output(HUMIDITY_PIN,GPIO.HIGH)
    GPIO.output(IRRIGATION_PIN,GPIO.HIGH)

# LOW  -> OPEN
# HIGH -> CLOSE

def start_irrigation(): # sulamayi baslat
    GPIO.output(IRRIGATION_PIN,GPIO.LOW)
    time.sleep(30) # 30 second delay
    GPIO.output(IRRIGATION_PIN,GPIO.HIGH)

def self_test():

    print '[*]Relay Control start<br>'
    time.sleep(1)
    GPIO.output(LIGHT_PIN,GPIO.LOW)
    time.sleep(1)
    GPIO.output(LIGHT_PIN,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(HUMIDITY_PIN,GPIO.LOW)
    time.sleep(1)
    GPIO.output(HUMIDITY_PIN,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(IRRIGATION_PIN,GPIO.LOW)
    time.sleep(1)
    GPIO.output(IRRIGATION_PIN,GPIO.HIGH)
    print '[*]Relay Control end<br>'



if (os.path.isfile('irrigation.txt')): # sulama dosyasi varsa
    #log_msg += '[*]irrigation.txt does exsist<br>'
    f = open('irrigation.txt','r')
    l_day = f.read()
    f.close()
    #log_msg +='[*]Irrigation start %s th <br>'%str(l_day)
else:    
    #log_msg +='[*]irrigation.txt does not exsist<br>'
    f = open('irrigation.txt','w')
    f_day = datetime.now().day
    l_day = (datetime.now().day + 3) % 31
    f.write(str(l_day))
    f.close()
    #log_msg +='[*]Irrigation start %d th <br>'%l_day

"""
if (os.path.isfile('light.txt')): # isiklandirma dosyasi varsa
    print 'light.txt does exsist'
    f = open('light.txt','r')
    l_hour = f.read()
    f.close()
    print 'Lighting start {0} a clock'.format(l_hour)
    print datetime.now().hour
else:
    print 'light.txt does not exsist'
    f = open('light.txt','w')
    f_hour = datetime.now().hour
    l_hour = (datetime.now().hour + 10) % 24
    f.write(str(l_hour))
    f.close()
    print 'Lighting start {0} a clock'.format(l_hour)
"""
try:
    coming_args = get_args(sys.argv[1],sys.argv[2])
    good_humidity = coming_args[0]
    irrigation_range = coming_args[1]
    print good_humidity,irrigation_range

    while True:
        log_msg = ''
        humidity, temperature = Adafruit_DHT.read_retry(DHT_MODEL, DHT_PIN)
        #lcd.cursor_pos = (0, 0)
        #lcd.write_string('Tem:{0}C - {1}'.format(temperature,datetime.now().hour)) 
        #lcd.cursor_pos = (1, 0)
        #lcd.write_string('Hum:{0}% - {1}'.format(humidity,datetime.now().minute))

        log_msg += '[*]Irrigation start to {0} th<br>'.format(l_day)
        log_msg += '[*]Humidity {0} <br>'.format(humidity)
        log_msg += '[*]Temperature {0} <br>'.format(temperature)

        #log_msg += '[*]Humidity:   %d <br>'%humidity
	    #log_msg += '[*]Temperature: %d C<br>'%temperature
        
        if (datetime.now().hour >= 12):
            #12 saat acik
            #12 saat kapali
            log_msg += '[*]Light is open<br>'
            GPIO.output(LIGHT_PIN,GPIO.LOW)
        else:
            log_msg += '[*]Light is close<br>'
            GPIO.output(LIGHT_PIN,GPIO.HIGH)
        
        if (humidity <= good_humidity):
            log_msg +='[*]Humidity start<br>'
            GPIO.output(HUMIDITY_PIN,GPIO.LOW)
        else:
            log_msg +='[*]Humidity good<br>'
            GPIO.output(HUMIDITY_PIN,GPIO.HIGH)

        if (datetime.now().day == int(l_day)): # sulama
            #irrigation start
            log_msg +='[*]irrigation start<br>'
            start_irrigation()
            l_day = (datetime.now().day + irrigation_range) % 31
            f = open('irrigation.txt','w')
            f.write(str(l_day))
            f.close()
        else:
            log_msg += '[*]Irrigation close<br>'
            GPIO.output(IRRIGATION_PIN,GPIO.HIGH) 
		
        
        write_log(log_msg)
        log_msg = ''

except KeyboardInterrupt:
	
	print '[*]System Exit'
	GPIO.output(LIGHT_PIN,GPIO.HIGH)
	GPIO.output(HUMIDITY_PIN,GPIO.HIGH)
	GPIO.output(IRRIGATION_PIN,GPIO.HIGH)

    #lcd.clear()

