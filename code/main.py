from FRCS import *
from Mailinglist import *
from SensorList import *

if __name__ == '__main__':
    #item creation
    x = FRCS()
    mailinglist = mailing_system()
    s1 = Sensor("Kouri", 0, (45, 85), "sens0.txt", 7.0, 25.0, False, 0.0, 0.0)
    s2 = Sensor("Strofilia", 1, (49, 5), "sens1.txt", 9.0, 10.0, True, 0.0, 0.0)
    s3 = Sensor("Volou", 2, (9, -25), "sens2.txt", 15.0, -2.0, True, 0.0, 0.0)
    s4 = Sensor("Dessert", 3, (5, 5), "sens3.txt", 0.0, 0.0, True, 0.0, 0.0)
    sensorlistitem = Sensorlist()
    sensorlistitem.addsensor(s1)
    sensorlistitem.addsensor(s2)
    sensorlistitem.addsensor(s3)
    sensorlistitem.addsensor(s4)
    parameterdataitem = Parameter_Data()
    x.welcome()#message for login plus a sort description of the system
    status = x.login() #login status
    x.Show_Menu(status,sensorlistitem,parameterdataitem,mailinglist) #show menu for the correct status
