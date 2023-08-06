import serial
import time
#from importlib import resources
#import io


def openSer(COM, Baud, timeout):
    global ser
    ser = serial.Serial(COM, Baud, timeout=timeout)
    return ser

def startMotors(ser):
    ser.write(bytes.fromhex("6E"))
    ser.write(bytes.fromhex("65"))


def reset(ser):
    ser.write(bytes.fromhex("6c"))
    time.sleep(0.1)
    ser.write(bytes.fromhex("76"))


def error(ser):
    dataList = readData("1A", ser)
    if (dataList[0] == "xff"):
        print("Motor vertical has an error!")
        print("To reset both Motors call function: reset()")
        disable(ser)
    elif (dataList[1] == "xff"):
        print("Motor horizontal has an error!")
        print("To reset both Motors call function: reset()")
        disable(ser)

def disable(ser):
    ser.write(bytes.fromhex("6E"))


def closeSer(ser):
    ser.close()

def readData(hexCode, ser):
    ser.write(bytes.fromhex(hexCode))
    time.sleep(0.1)
    hex_response = ser.readline()
    time.sleep(0.1)
    return hex_response





