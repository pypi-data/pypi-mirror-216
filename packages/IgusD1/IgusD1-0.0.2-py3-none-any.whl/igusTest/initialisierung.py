import serial
import time
#from importlib import resources
#import io


def openSer():
    global ser
    ser = serial.Serial('COM3', 9600, timeout=0)
    return ser

def startMotors(ser):
    ser.write(bytes.fromhex("6E"))
    ser.write(bytes.fromhex("65"))


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


def reset(ser):
    ser.write(bytes.fromhex("6c"))
    time.sleep(0.1)
    ser.write(bytes.fromhex("76"))


def error(dataList, ser):

    if (dataList[1] == "xff"):
        print("Motor vertical has an error!")
        reset(ser)
    elif (dataList[2] == "xff"):
        print("Motor horizontal has an error!")
        reset(ser)

