#!/usr/bin/env python

# light controller script


from datetime import datetime
from time import gmtime, strftime
import os 

flag = True

    
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
        #irrigation start
        print 'sgtat'
        l_hour = (datetime.now().hour + 10) % 24



