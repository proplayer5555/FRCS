import os


class Sensor:
    def __init__(self, name, sensorid, coordinates, file, fuel_quantity, terrain_incline, status, offset_hm, offset_vlc):
        self._name = name
        self._sensorid = sensorid
        self._coordinates = coordinates
        self._file = file
        self._fuel_quantity = fuel_quantity
        self._terrain_incline = terrain_incline
        self._status = status
        self._offset_hm = offset_hm
        self._offset_vlc = offset_vlc

    def __str__(self):
        return f"Name: {self._name:<15} \tId: {self._sensorid:>4}\n"
    def getdata(self):#function to return specific sensor data needed for the calculations including the first reading of the humidity and velocity values from the file
        current_dir = os.getcwd()
        input_file = os.path.join(current_dir + "/Sensors", self._file)
        with open(input_file, 'r', encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                humidity, velocity = map(str.strip, line.split('|', maxsplit=1))
                break
        return self._sensorid, self._terrain_incline, humidity, velocity, self._fuel_quantity , self._offset_hm, self._offset_vlc

    def show_sensor_data(self):
        current_dir = os.getcwd()
        input_file = os.path.join(current_dir + "/Sensors", self._file)
        humidity_list, velocity_list = [], []
        avgh, avgv = 0, 0
        line_count = 0
        counter=0
        recenthumidity = 0
        recentvelocity = 0
        with open(input_file, 'r', encoding="utf-8") as file:
            lines = file.readlines()
            line_count = len(lines)
            for line in lines:
                humidity, velocity = map(str.strip, line.split('|', maxsplit=1))
                humidity_list.append(float(humidity))
                velocity_list.append(float(velocity))
                if counter ==0 :
                    recenthumidity, recentvelocity = float(humidity), float(velocity)
                    counter += 1
        for item, item2 in zip(humidity_list, velocity_list):
            avgh += float(item)
            avgv += float(item2)
        print(f"Moisture Content\tMin: {min(humidity_list)} Max: {max(humidity_list)}")
        print(f"Air Velocity\t    Min: {min(velocity_list)} Max: {max(velocity_list)}")
        return avgh/line_count, avgv/line_count , recenthumidity, recentvelocity
    def getid(self):
        return self._sensorid
    
    def getname(self):
        return self._name

    def getfile(self):
        return self._file

    def getstatus(self):
        return self._status
    #shows all items to edit
    def showall(self):
        current_dir = os.getcwd()
        input_file = os.path.join(current_dir + "/Sensors", self._file)
        with open(input_file, 'r', encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                humidity, velocity = map(str.strip, line.split('|', maxsplit=1))
                break
        if (self._status == True):
            statusmsg = "Active"
            choice = input(
                f"\n1 Edit name:\t{self._name:>31}\n2 Edit Coordinates:\t{self._coordinates[0]:>20} {self._coordinates[1]}\n3 Edit file name:\t{self._file:>27}\n"
                f"4 Edit Fuel Quantity:\t{self._fuel_quantity:>17}\n5 Edit Slope:\t{self._terrain_incline:>26} degrees\n"
                f"6 Edit Moisture content offset:\tMC:{humidity:>4} Offset:{self._offset_hm:>4}\n7 Edit Air velocity offset:\t"
                f"Vel:{velocity:>7} Offset:{self._offset_vlc:>4}\n8 Toggle sensor status:\t{statusmsg:>18}\n9 Cancel\n")
        else:
            statusmsg = "Inactive"
            choice = input(f"\n1 Edit name:\t{self._name:>31}\n2 Edit Coordinates:\t{self._coordinates[0]:>20} {self._coordinates[1]}\n3 Edit file name:\t{self._file:>27}\n"
                  f"4 Edit Fuel Quantity:\t{self._fuel_quantity:>17}\n5 Edit Slope:\t{self._terrain_incline:>26} degrees\n"
                  f"6 Edit Moisture content offset:\tMC:{humidity:>4} Offset:{self._offset_hm:>4}\n7 Edit Air velocity offset:\t"
                  f"Vel:{velocity:>7} Offset:{self._offset_vlc:>4}\n8 Toggle sensor status:\t{statusmsg:>21}\n9 Cancel\n")
        return choice

    def edit_sensor_name(self, name):
        self._name = name
        
    def edit_coordinates(self,coo1,coo2):
        self._coordinates = (coo1, coo2)

    def edit_filename(self,filename):
        current_Dir = os.getcwd()
        os.rename(current_Dir+"/Sensors/"+self._file, current_Dir+"/Sensors/"+filename)
        self._file = filename

    def edit_fuel_quantity(self, fqa):
        self._fuel_quantity = fqa

    def edit_slope(self, slope):
        self._terrain_incline = slope
    
    def edit_offset_mc(self,offset):
       self._offset_hm=offset

    def edit_offset_avc(self,offset):
       self._offset_vlc=offset

    def toggle_status(self):
        if self._status:
            self._status = False
            printthis = "Deactivated"
        else:
            self._status = True
            printthis = "Activated"
        print(f"Status of sensor {self._name} with id {self._sensorid} updated successfully to {printthis}")
    def printall(self):
        if self._status:
            status = "Activated"
            return f"\nName: {self._name:^33}\nSensorId: {self._sensorid:>11}\nCoordinates: {self._coordinates[0]:>9}, {self._coordinates[1]}\nAfq: {self._fuel_quantity:>18}\nSlope: {self._terrain_incline:>17}\nStatus: {status:>21}"
        else:
            status = "Deactivated"
            return f"\nName: {self._name:^31}\nSensorId: {self._sensorid:>11}\nCoordinates: {self._coordinates[0]:>9}, {self._coordinates[1]}\nAfq: {self._fuel_quantity:>18}\nSlope: {self._terrain_incline:>17}\nStatus: {status:>23}"