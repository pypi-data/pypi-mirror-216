import igusD1
import time

def isRefVertical(ser):
    dataList = []
    data = str(igusD1.initialisierung.readData("1A", ser))
    dataList = data.split('\\')
    igusD1.initialisierung.error(dataList, ser)
    if (dataList[3] != "xff"):
        ref_vertikal(ser)


def vertIsActive(ser):
    dataList = []
    isActive = True
    while (isActive == True):
        # Wait unitl its not active anymore
        dataList.clear()  # clear list
        data = str(igusD1.initialisierung.readData("1A", ser))  # new values to variable
        dataList = data.split('\\')
        if dataList[4] == "xff":
            isActiv = True
        elif dataList[7] != "xff":
            isActive = False



def ref_vertikal(ser):
    print("Is Referencing vert now")
    ser.write(bytes.fromhex("72"))
    ser.write(bytes.fromhex("73"))
    time.sleep(0.01)
    ser.write(bytes.fromhex("66"))
    time.sleep(0.01)
    vertIsActive(ser)



def pos1_vertikal(ser):
    isRefVertical(ser)
    ser.write(bytes.fromhex("68"))
    ser.write(bytes.fromhex("73"))
    time.sleep(0.01)
    ser.write(bytes.fromhex("66"))
    time.sleep(0.1)
    print("MotorVert is going to pos1")
    ser.write(bytes.fromhex("70"))
    vertIsActive(ser)
    data = str(igusD1.initialisierung.readData("1A", ser))
    print("MotorVert Pos1: " + data)


def pos2_vertikal(ser):
    isRefVertical(ser)
    ser.write(bytes.fromhex("72"))
    ser.write(bytes.fromhex("69"))
    time.sleep(0.01)
    ser.write(bytes.fromhex("66"))
    time.sleep(0.1)
    print("MotorVert is going to pos2")
    ser.write(bytes.fromhex("70"))
    vertIsActive(ser)
    print("MotorVert Pos2: " + str(igusD1.initialisierung.readData("1A", ser)))


def pos3_vertikal(ser):
    isRefVertical(ser)
    ser.write(bytes.fromhex("68"))
    ser.write(bytes.fromhex("69"))
    time.sleep(0.01)
    ser.write(bytes.fromhex("66"))
    time.sleep(0.1)
    print("MotorVert is going to pos3")
    ser.write(bytes.fromhex("70"))
    vertIsActive(ser)
    print("MotorVert Pos3: " + str(igusD1.initialisierung.readData("1A", ser)))