from optparse import OptionParser
import serial
import xmodem
import os, sys, time
import logging
import pyprind
import platform

import sys

class Logger(object):
    def __init__(self):
        
        
        self.terminal = sys.stdout

    def write(self, message):
        self.terminal.write(message)
        index = message.find("ETA")
        if (index != -1) :
            lcd_msg=message[index-1:index+4]
            lcd_msg+=message[index+8:index+13]
                
    
    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass 

s=serial.Serial()
lcd_logger = Logger()

format_prep_cmd=[b'\x00\x05\x20\x01\x00\x04\xff\xff\x00\x00\xb9\x03',
                 b'\x00\x05\x20\x01\x00\x04\xff\xff\x00\x22\xbd\x23',
                 b'\x00\x05\x20\x01\x00\x04\xff\xff\x00\x10\xab\x32',
                 b'\x00\x05\x20\x01\x00\x04\xff\xff\x00\x10\xab\x32']

format_prep_rply=[b'\x80\x05\x20\x01\x00\x08\xff\xff\x00\x01\x00\x00\x00\x00\x13\xc9',
                 b'\x80\x05\x20\x01\x00\x0c\xff\xff\x00\x23\x00\x00\x00\x00\xc2\x20\x16\x00\x2d\xf4',
                 b'\x80\x05\x20\x01\x00\x10\xff\xff\x00\x11\x00\x00\x00\x08\x00\x00\x00\x00\x00\x40\x00\x00\x13\xef',
                 b'\x80\x05\x20\x01\x00\x10\xff\xff\x00\x11\x00\x00\x00\x08\x00\x00\x00\x00\x00\x40\x00\x00\x13\xef']

format_rply = b'\x80\x05\x20\x01\x00\x08\xff\xff\x00\x0b\x00\x00\x00\x00\x55\x67'

format_cmd=[b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x00\x00\x00\x00\x02\x00\x00\xb0\x74',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x02\x00\x00\x00\x02\x00\x00\xd0\x97',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x04\x00\x00\x00\x02\x00\x00\x71\xb2',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x06\x00\x00\x00\x02\x00\x00\x11\x51',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x08\x00\x00\x00\x02\x00\x00\x23\xd9',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x0a\x00\x00\x00\x02\x00\x00\x43\x3a',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x0c\x00\x00\x00\x02\x00\x00\xe2\x1f',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x0e\x00\x00\x00\x02\x00\x00\x82\xfc',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x10\x00\x00\x00\x02\x00\x00\x87\x0f',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x12\x00\x00\x00\x02\x00\x00\xe7\xec',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x14\x00\x00\x00\x02\x00\x00\x46\xc9',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x16\x00\x00\x00\x02\x00\x00\x26\x2a',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x18\x00\x00\x00\x02\x00\x00\x14\xa2',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x1a\x00\x00\x00\x02\x00\x00\x74\x41',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x1c\x00\x00\x00\x02\x00\x00\xd5\x64',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x1e\x00\x00\x00\x02\x00\x00\xb5\x87',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x20\x00\x00\x00\x02\x00\x00\xde\x82',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x22\x00\x00\x00\x02\x00\x00\xbe\x61',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x24\x00\x00\x00\x02\x00\x00\x1f\x44',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x26\x00\x00\x00\x02\x00\x00\x7f\xa7',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x28\x00\x00\x00\x02\x00\x00\x4d\x2f',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x2a\x00\x00\x00\x02\x00\x00\x2d\xcc',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x2c\x00\x00\x00\x02\x00\x00\x8c\xe9',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x2e\x00\x00\x00\x02\x00\x00\xec\x0a',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x30\x00\x00\x00\x02\x00\x00\xe9\xf9',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x32\x00\x00\x00\x02\x00\x00\x89\x1a',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x34\x00\x00\x00\x02\x00\x00\x28\x3f',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x36\x00\x00\x00\x02\x00\x00\x48\xdc',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x38\x00\x00\x00\x02\x00\x00\x7a\x54',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x3a\x00\x00\x00\x02\x00\x00\x1a\xb7',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x3c\x00\x00\x00\x02\x00\x00\xbb\x92',
            b'\x00\x05\x20\x01\x00\x0c\xff\xff\x00\x0a\x00\x3e\x00\x00\x00\x02\x00\x00\xdb\x71']

format_end_cmd = b'\x00\x05\x20\x01\x00\x04\xff\xff\x00\x0c\x78\x8f'
format_end_rpl = b'\x80\x05\x20\x01\x00\x08\xff\xff\x00\x0d\x00\x00\x00\x00\x98\xe2'

flash_start_cmd=[b'\x00\x05\x20\x01\x00\x04\xff\xff\x00\x10\xab\x32',
                 b'\x00\x05\x20\x01\x00\x14\xff\xff\x00\x02\x00\x00\x00\x00\x00\x1f\xad\x80\x00\x1f\xad\x80\x00\x00\x04\x00\x50\xb1']

flash_start_rply=[b'\x80\x05\x20\x01\x00\x10\xff\xff\x00\x11\x00\x00\x00\x08\x00\x00\x00\x00\x00\x40\x00\x00\x13\xef',
                  b'\x80\x05\x20\x01\x00\x08\xff\xff\x00\x03\x00\x00\x00\x00\x57\x4a\x43']

flash_end_cmd=b'\x00\x05\x20\x01\x00\x04\xff\xff\x00\x04\xf9\x87'                  
flash_end_rply=b'\x80\x05\x20\x01\x00\x0c\xff\xff\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\xa1\x5f'

def getc(size, timeout=1):
    return s.read(size)

def format_whole_chip():
    for i in range (0,len(format_prep_cmd)):
        reply = format_respond(format_prep_cmd[i],format_prep_rply[i])
        if not reply: return reply
    
    for cmd in format_cmd:
        reply = format_respond(cmd,format_rply)
        if not reply: return reply

    reply= format_respond(format_end_cmd,format_end_rpl)
    if not reply: return reply

    for i in range (0,len(flash_start_cmd)):
        reply = format_respond(flash_start_cmd[i],flash_start_rply[i])
        if not reply: return reply

    return reply

def format_respond(cmd,resp):
    counter=0
    c=b''
    while 1:
        s.write(cmd)
        s.flush()
        counter+=1
        st = time.time()
        et = time.time() - st
        while s.in_waiting <len(resp):
            et = time.time() - st
            if et > 5:
                break    
        c=s.read(s.in_waiting)
        print("------------\r\n")
        print("-----C------\r\n")
        print(cmd)
        print("-----R------\r\n")
        print(c)
        print("-----E------\r\n")
        print(resp)
        print("------------\r\n")
        
        index=c.find(resp)
        if index !=-1:
            s.flushInput()
            return True
        else:
            if (counter > 30):
                s.close()
                return False

def upload(port,files):
    error_count=0
    c_count=0
    retry=0
    start_time=time.time()
    s.baudrate=115200
    s.port=port
    s.timeout=1
    s.open()
    s.setRTS(False)
    s.setDTR(False)
    s.flushInput()

    while 1:
        c=s.read()
        s.flushInput()
        print(c)

        if c!=b'\x15' or  c==b'C':
            c_count=c_count+1

        if c!=b'\x15' and c!=b'C':
            error_count=error_count+1
        if c_count>1:
            print("Start uploading uart_hs.bin")
            break
        if error_count>3:
            print( "Error - Not reading the start flag")
            retry=retry+1
            error_count=0
            c_count=0
            start_time = time.time()
            s.close()
            time.sleep(0.3)
            s.baudrate=115200
            s.port=port
            s.timeout=1
            s.open()
            s.setRTS(False)
            s.setDTR(False)
            s.flushInput()
        if retry>3:
            print( "Exiting")
            s.close()
            return -1
        
    statinfo = os.stat(files[0])

    bar=pyprind.ProgBar(statinfo.st_size/1024+2,stream=lcd_logger)
    def putc(data, timeout=1):
        bar.update()
        return s.write(data)
    m = xmodem.XMODEM(getc, putc, mode='xmodem1k')
    stream = open(files[0],'rb')
    r = m.send(stream,quiet=True)
    if not r:
        print( "Exiting")
        s.close()
        return -1

    s.close()
    s.baudrate=921600
    s.open()
    print("uart_hs.bin uploaded, start uploading ated_hs.bin")

    statinfo = os.stat(files[1])
    bar=pyprind.ProgBar(statinfo.st_size/1024+2,stream=lcd_logger)

    m = xmodem.XMODEM(getc, putc, mode='xmodem1k')
    stream = open(files[1],'rb')
    r=m.send(stream,quiet=True)
    if not r:
        print( "Exiting")
        s.close()
        return -1

    print("ated_hs.bin uploaded, start Formating")
    time.sleep(1)
    s.close()
    s.baudrate=921600
    s.open()

    result = format_whole_chip()
    if (result == False):
        print( "Exiting")
        s.close()
        return -1

    while 1:
        c=s.read()
        c=c.decode("utf-8") 
        s.flushInput()
        print(c)

        if c=="C":
            c_count=c_count+1

        if c!=0 and c!="C":
            error_count=error_count+1
        if c_count>1:
            print("Start uploading Firmware")
            break
        if error_count>3:
            print( "Error - Not reading the start flag")
            retry=retry+1
            error_count=0
            c_count=0
            start_time = time.time()
            s.close()
            time.sleep(0.3)
            s.baudrate=115200
            s.port=port
            s.timeout=1
            s.open()
            s.setRTS(False)
            s.setDTR(False)
            s.flushInput()
        if retry>3:
            print( "Exiting")
            s.close()
            return -1

    statinfo_bin = os.stat(files[2])
    
    bar_user = pyprind.ProgBar(statinfo_bin.st_size/1024+2,stream=lcd_logger)
    def putc_user(data, timeout=1):
        bar_user.update()
        
        return s.write(data)
    stream = open(files[2], 'rb')
    m = xmodem.XMODEM(getc, putc_user, mode='xmodem1k')
    r=m.send(stream,quiet=True)
    if not r:
        print( "Exiting")
        s.close()
        return -1

    reply= format_respond(flash_end_cmd,flash_end_rply)
    if not reply:
        print( "Exiting")
        s.close()
        return -1
    print("Bin file uploaded. The board reboots now.")

    time.sleep(1)
    s.write(b'C\r')
    s.flush()
    s.flushInput()
    time.sleep(0.1)
    s.setRTS(False)
    s.setDTR(False)
    time.sleep(0.1)
    s.close()
    Finish_time=time.time()
    print("Full upload time: ",Finish_time-start_time)
    return 0



