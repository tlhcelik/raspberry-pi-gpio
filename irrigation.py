#!/usr/bin/env python

from datetime import datetime
from time import gmtime, strftime
import os 

flag = True

print datetime.now().day    
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


if (datetime.now().day == int(l_day)):
    #irrigation start
    print 'ir start'
    l_day = (datetime.now().day + 3) % 31
    f = open('irrigation.txt','w')
    f.write(str(l_day))
    f.close()