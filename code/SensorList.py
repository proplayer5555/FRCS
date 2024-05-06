from Sensor import *
import os

class Sensorlist:
    def __init__(self):
        self._List = []

    def getsensordata(self):
        list = []
        for elem in self._List:
            if elem.getstatus():
                id, incline, humidity, velocity, afq, hoffset, vlcoffset = elem.getdata()
                list.append((id, incline, humidity, velocity, afq, hoffset, vlcoffset))
        return list

    def get_sensor(self,index):
        if index == "all":
            list = []
            for item in self._List:
                list.append(item)
            return list
        else:
            for item in self._List:
                if item._sensorid == index:
                    return item

    def checkConnectivity(self):
        listofallsensors = self.get_sensor("all")
        failedsensorlist = []
        success = True
        current_dir = os.getcwd()
        for item in listofallsensors:
            if not os.path.exists(current_dir+f"/Sensors/{item.getfile()}"):
                failedsensorlist.append(item)
                success = False
        return success, failedsensorlist

    def addsensor(self,sensor):
        self._List.append(sensor)