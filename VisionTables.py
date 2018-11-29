from networktables import NetworkTables

connected = False


def connectionListener(connected, info):
        print(info, '; Connected=%s' % connected)


def sendX(x):
    sd.putNumber('visionX', x)
    print("visionX" + str(x))


def sendY(y):
        sd.putNumber('visionY', y)

def sendArea(area):
    sd.putNumber('visionArea', area)

NetworkTables.initialize(server='10.33.24.101')
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)
sd = NetworkTables.getTable("SmartDashboard")




