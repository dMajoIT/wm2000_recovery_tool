from optparse import OptionParser
import serial
import xmodem
import os
import sys
import time
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
        if (index != -1):
            lcd_msg = message[index-1:index+4]
            lcd_msg += message[index+8:index+13]

    def flush(self):
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.
        pass


s = serial.Serial()


def getc(size, timeout=1):
    return s.read(size)


def get_response(resp):
    c = b''
    counter = 0
    while 1:
        counter += 1
        c = c+s.read(10)
        print(c)
        print(resp)

        index = c.find(resp)
        if index != -1:
            s.flushInput()
            return True
        else:
            if (counter > 100):
                s.close()
                return False


def upload(port, files):
    error_count = 0
    c_count = 0
    retry = 0
    start_time = time.time()
    s.baudrate = 115200
    s.port = port
    s.timeout = 1
    s.open()
    s.setRTS(False)
    s.setDTR(False)
    s.flushInput()

    while 1:
        c = s.read()
        s.flushInput()
        print(c)

        if c == b'C':
            c_count = c_count+1

        if c != 0 and c != b'C':
            error_count = error_count+1
        if c_count > 1:
            print("Start uploading uart_hs.bin")
            break
        if error_count > 3:
            print("Error - Not reading the start flag")
            retry = retry+1
            error_count = 0
            c_count = 0
            start_time = time.time()
            s.close()
            time.sleep(0.3)
            s.baudrate = 115200
            s.port = port
            s.timeout = 1
            s.open()
            s.setRTS(False)
            s.setDTR(False)
            s.flushInput()
        if retry > 3:
            print("Exiting")
            s.close()
            return -1

    statinfo = os.stat(files[0])
    bar = pyprind.ProgBar(statinfo.st_size/1024+2)

    def putc(data, timeout=1):
        bar.update()
        return s.write(data)
    m = xmodem.XMODEM(getc, putc, mode='xmodem1k')
    stream = open(files[0], 'rb')
    m.send(stream, quiet=True)
    s.baudrate = 921600
    print("uart_hs.bin uploaded, start uploading ated_hs.bin")

    statinfo = os.stat(files[1])
    bar = pyprind.ProgBar(statinfo.st_size/1024+2)

    m = xmodem.XMODEM(getc, putc, mode='xmodem1k')
    stream = open(files[1], 'rb')
    m.send(stream, quiet=True)

    print("ated_hs.bin uploaded, start Formating")
    time.sleep(1)
    respond1 = b'\x80\x05\x20\x01\x00\x08'
    respond2 = b'\x80\x05\x20\x01\x00\x14'
    # breakpoint()
    s.baudrate = 921600
    cmd = b'\x00\x05\x20\x01\x00\x04\xFF\xFF\x00\x00\xB9\x03'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1

    cmd = b'\x00\x05\x20\x01\x00\x04\xFF\xFF\x00\x22\xBD\x23'
    s.write(cmd)
    s.flush()

    result = get_response(respond2)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x04\xFF\xFF\x00\x24\xDD\xE5'
    s.write(cmd)
    s.flush()

    result = get_response(respond2)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x04\xFF\xFF\x00\x22\xBD\x23'
    s.write(cmd)
    s.flush()

    result = get_response(respond2)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x00\x00\x00\x00\x02\x00\x00\xB0\x74'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x02\x00\x00\x00\x02\x00\x00\xD0\x97'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x04\x00\x00\x00\x02\x00\x00\x71\xB2'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x06\x00\x00\x00\x02\x00\x00\x11\x51'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x08\x00\x00\x00\x02\x00\x00\x23\xD9'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x0A\x00\x00\x00\x02\x00\x00\x43\x3A'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x0C\x00\x00\x00\x02\x00\x00\xE2\x1F'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x0E\x00\x00\x00\x02\x00\x00\x82\xFC'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x10\x00\x00\x00\x02\x00\x00\x87\x0F'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x12\x00\x00\x00\x02\x00\x00\xE7\xEC'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x14\x00\x00\x00\x02\x00\x00\x46\xC9'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x16\x00\x00\x00\x02\x00\x00\x26\x2A'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x18\x00\x00\x00\x02\x00\x00\x14\xA2'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x1A\x00\x00\x00\x02\x00\x00\x74\x41'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x1C\x00\x00\x00\x02\x00\x00\xD5\x64'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x1E\x00\x00\x00\x02\x00\x00\xB5\x87'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x20\x00\x00\x00\x02\x00\x00\xDE\x82'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x22\x00\x00\x00\x02\x00\x00\xBE\x61'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x24\x00\x00\x00\x02\x00\x00\x1F\x44'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x26\x00\x00\x00\x02\x00\x00\x7F\xA7'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x28\x00\x00\x00\x02\x00\x00\x4D\x2F'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x2A\x00\x00\x00\x02\x00\x00\x2D\xCC'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x2C\x00\x00\x00\x02\x00\x00\x8C\xE9'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x2E\x00\x00\x00\x02\x00\x00\xEC\x0A'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x30\x00\x00\x00\x02\x00\x00\xE9\xF9'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x32\x00\x00\x00\x02\x00\x00\x89\x1A'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x34\x00\x00\x00\x02\x00\x00\x28\x3F'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x36\x00\x00\x00\x02\x00\x00\x48\xDC'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x38\x00\x00\x00\x02\x00\x00\x7A\x54'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x3A\x00\x00\x00\x02\x00\x00\x1A\xB7'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x0C\xFF\xFF\x00\x0A\x00\x3C\x00\x00\x00\x02\x00\x00\xBB\x92'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x04\xFF\xFF\x00\x0C\x78\x8F'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    cmd = b'\x00\x05\x20\x01\x00\x1C\xFF\xFF\x00\x02\x00\x00\x00\x00\x00\x3E\x00\x00\x00\x3E\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\xFA\x64'
    s.write(cmd)
    s.flush()

    result = get_response(respond1)
    if (result == False):
        return 1
    while 1:
        c = s.read()
        c = c.decode("utf-8")
        s.flushInput()
        print(c)

        if c == "C":
            c_count = c_count+1

        if c != 0 and c != "C":
            error_count = error_count+1
        if c_count > 1:
            print("Start uploading Firmware")
            break
        if error_count > 3:
            print("Error - Not reading the start flag")
            retry = retry+1
            error_count = 0
            c_count = 0
            start_time = time.time()
            s.close()
            time.sleep(0.3)
            s.baudrate = 115200
            s.port = port
            s.timeout = 1
            s.open()
            s.setRTS(False)
            s.setDTR(False)
            s.flushInput()
        if retry > 3:
            print("Exiting")
            s.close()
            return -1

    statinfo_bin = os.stat(files[2])
    lcd_logger = Logger()
    bar_user = pyprind.ProgBar(statinfo_bin.st_size/1024+2, stream=lcd_logger)

    def putc_user(data, timeout=1):
        bar_user.update()

        return s.write(data)
    stream = open(files[2], 'rb')
    m = xmodem.XMODEM(getc, putc_user, mode='xmodem1k')
    m.send(stream, quiet=True)
    print("Bin file uploaded.")
    time.sleep(1)
    s.write(b'C\r')
    s.flush()
    s.flushInput()
    time.sleep(0.1)
    s.setRTS(False)
    s.setDTR(False)
    time.sleep(0.1)
    s.close()
    Finish_time = time.time()
    print("Full upload time: ", Finish_time-start_time)
    return 0
