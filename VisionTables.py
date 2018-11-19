from networktables import NetworkTables

connected = False


def connectionListener(connected, info):
        print(info, '; Connected=%s' % connected)
        connected = True


def sendX(x):
    if connected:
        sd.visionY = x
    else:
        print("Waiting for connection")

def sendY(y):
    if connected:
        sd.visionY = y
    else:
        print("Waiting for connection")

NetworkTables.initialize(server='10.33.24.2')
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)
sd = NetworkTables.getTable("SmartDashboard")




