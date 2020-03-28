'''
Created on Feb 3, 2020

@author: 14106
'''
import os
import io
import sys
import glob
# import array
import serial
import binascii
from asyncore import read

gSerialPortList = []
gNordicSer = serial.Serial()
gFileContents = []

""" 
Lists serial port names
    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of the serial ports available on the system
"""
def AvailableSerialPorts():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


""" 
@ Connect serial port
""" 
def ConnectSerialPort():
    global gNordicSer
    inputPort = input("Select port: ")
    COMPort = r"COM" + inputPort
    
    for index in range(len(gSerialPortList)):
        if (COMPort == gSerialPortList[index]):
            print(COMPort, "selected")
            gNordicSer.baudrate = 115200
            gNordicSer.port = COMPort
            gNordicSer.bytesize = 8
            gNordicSer.parity = serial.PARITY_NONE
            gNordicSer.dtr = 1;
            gNordicSer.rts = 1;
            gNordicSer.xonxoff = 0
            gNordicSer.write_timeout = 10
            break
    try:
        gNordicSer.open()
        locPortNoti = "Device " + COMPort + " opened\r\n";
        print(locPortNoti)
    except:
        print("Cannot open ", COMPort)

#     if (gNordicSer.is_open):
#         gNordicSer.write(str.encode(locPortNoti))

""" 
@ File open and print function
""" 
def OpenAndSendFile():
    global gFileContents
    
    locFilePath = input("Enter file name: ")
    
    print("Opening file: " + locFilePath)
    with open(locFilePath, 'rb') as locFile:
        gFileContents = locFile.read()
        locFileLen = len(gFileContents) 
    print("File length (byte)", locFileLen)
    print(gFileContents)
    print(type(gFileContents))

'''
@ Main execution
'''
gSerialPortList = AvailableSerialPorts()

if (0 == len(gSerialPortList)):
    print("No available port")
else:
    print("Available ports: ", gSerialPortList)
    ConnectSerialPort()

while 1:
    OpenAndSendFile()
    
    if (gNordicSer.is_open):
        gNordicSer.write(gFileContents)
