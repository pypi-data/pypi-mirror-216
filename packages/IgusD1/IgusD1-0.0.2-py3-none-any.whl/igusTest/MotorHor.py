import igusD1
import time
#  Motor horizontal (hor)

def isRefHorizontal(ser):
    dataList = []
    data = str(igusD1.initialisierung.readData("1A", ser))
    dataList = data.split('\\')

    igusD1.initialisierung.error(dataList, ser)
    if (dataList[3] != "xff"):
        ref_horizontal(ser)


def horIsActive(ser):
    dataList = []
    isActive = True
    while (isActive == True):
        # Wait unitl its not active anymore
        dataList.clear()  # clear list
        data = str(igusD1.initialisierung.readData("1A", ser))  # new values to variable
        dataList = data.split('\\')
        if dataList[7] == "xff":
            isActiv = True
        elif dataList[7] != "xff":
            isActive = False


def ref_horizontal(ser):
    print("Is Refernzing hor now")
    ser.write(bytes.fromhex("75"))
    ser.write(bytes.fromhex("76"))
    time.sleep(0.01)
    ser.write(bytes.fromhex("67"))
    horIsActive(ser)


def pos1_horizontal(ser):
    isRefHorizontal(ser)
    ser.write(bytes.fromhex("6A"))
    ser.write(bytes.fromhex("74"))
    time.sleep(0.01)
    ser.write(bytes.fromhex("67"))
    time.sleep(0.1)
    print("MotorHor is going to pos1")
    ser.write(bytes.fromhex("71"))
    horIsActive(ser)
    print("MotorHor Pos1: " + str(igusD1.initialisierung.readData("1A", ser)))


def pos2_horizontal(ser):
    isRefHorizontal(ser)
    ser.write(bytes.fromhex("73"))
    ser.write(bytes.fromhex("6B"))
    time.sleep(0.01)
    ser.write(bytes.fromhex("67"))
    time.sleep(0.1)
    print("MotorHor is going to pos2")
    ser.write(bytes.fromhex("71"))
    horIsActive(ser)
    print("MotorHor Pos2: " + str(igusD1.initialisierung.readData("1A", ser)))


def pos3_horizontal(ser):
    isRefHorizontal(ser)
    ser.write(bytes.fromhex("6A"))
    ser.write(bytes.fromhex("6B"))
    time.sleep(0.01)
    ser.write(bytes.fromhex("67"))
    time.sleep(0.1)
    print("MotorHor is going to pos3")
    ser.write(bytes.fromhex("71"))
    horIsActive(ser)
    print("MotorHor Pos3: " + str(igusD1.initialisierung.readData("1A", ser)))