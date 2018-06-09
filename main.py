#!/usr/bin/env python

# main controller script
# start for 
# #python main.py &

from datetime import datetime
from time import gmtime, strftime
import os 

flag = True

    
if (os.path.isfile('irrigation.txt')): # sulama dosyasi varsa
    print 'irrigation.txt does exsist'
    
    f = open('irrigation.txt','r')
    l_day = f.read()
    f.close()
    print 'Irrigation start {0} th'.format(l_day)
else:    
    print 'irrigation.txt does not exsist'
    f = open('irrigation.txt','w')
    f_day = datetime.now().day
    l_day = (datetime.now().day + 3) % 31
    f.write(str(l_day))
    f.close()
    print 'Irrigation start {0} th'.format(l_day)

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

while(flag):
    if (datetime.now().hour == l_hour): # burasi olmadi
        #lighthing start
        print 'sgtat'
        l_hour = (datetime.now().hour + 10) % 24

    if (datetime.now().day == l_day):
        #irrigation start
        l_day = (datetime.now().day + 3) % 31

    




