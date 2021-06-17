#!/usr/bin/python
import os
import sys, getopt
import firmware_upload as fwupload

def print_usage():
    print ('wm2000_recovery.py -bl <bootloader> -mon <mmonitor> -tios <tios> -app0 <APP0> -app1 <APP1>')
    print ('All parameters are required if there is an app1. If there is no app1 app0 is also optional.') 
    sys.exit(2)
    
def get_padding_size(file_path):
    FL_BLOCK_SIZE = 4*1024
    file_stats=os.stat(file_path)
    size_in_bytes=file_stats.st_size
    if (size_in_bytes%FL_BLOCK_SIZE != 0):
        size_After_Padding= size_in_bytes + FL_BLOCK_SIZE-(size_in_bytes%FL_BLOCK_SIZE)
    else:
        size_After_Padding = size_in_bytes
    
    return size_After_Padding

def main(argv):
    bl = ''
    mon = ''
    os=''
    appzero=''
    appone=''
    sp=''
    try:
        opts, args = getopt.getopt(argv, '' ,["help", "bl=","mon=","tios=","app0=","app1=","serial="])    
    except getopt.GetoptError:
        print ("ooofdsa")
        print_usage()
    if len(opts) == 0: 
        print_usage()
        
    for opt, arg in opts:
        if opt == 'help':
            print ('wm2000_recovery.py -bl <bootloader> -mon <mmonitor> -tios <tios> -app0 <APP0> -app1 <APP1>')
            print ('All parameters are required if there is an app1. If there is no app1 app0 is also optional.') 
            sys.exit()
        elif opt in ("--bl"):
            bl = arg
        elif opt in ("--mon"):
            mon = arg
        elif opt in ("--tios"):
            os = arg
        elif opt in ("--app0"):
            appzero = arg
        elif opt in ("--app1"):
            appone = arg
        elif opt in ("--serial"):
            sp = arg
        else:
            print (arg + "is not supported")
    if (appone != '' and appzero == '' ) or sp=='':
        print_usage()
    
    bootloader = open( bl,"rb")
    monitor = open (mon,"rb")
    tios = open (os,"rb")
    app0 = None
    app1 = None
    app0size=0
    
    if appzero != '':
        app0 = open(appzero,"rb") 
        app0size= get_padding_size(appzero)
    if appone != '':
        app1 = open(appone,"rb")

    with open ("generatedfw.bin","wb") as f:
        bootloader_data = bootloader.read()
        bootloader_data = bootloader_data.ljust(0x10000,b'\00')
        bootloader.close()
        fw=bootloader_data
        
        monitor_data = monitor.read()
        monitor_data = monitor_data.ljust(0xD8000,b'\00')
        monitor.close()
        fw+=monitor_data
        
        tios_data = tios.read() #Tios release is already justified to 4KB boundary.
        tios.close()
        fw+=tios_data
        
        if app0 != None:
            app0_data = app0.read()
            app0_data = app0_data.ljust(app0size,b'\00')
            app0.close()
            fw+=app0_data
        
        if app1 != None:
            app1_data = app1.read()
            fw+=app1_data
            app1.close()
        
        f.write(fw)   
        
    print ( fwupload.upload(sp,["./fw/uploader/uart_hs.bin","./fw/uploader/ated_hs.bin","./generatedfw.bin"]) )

if __name__ == "__main__":
    main(sys.argv[1:])
    