from Generic_User import *
from Fire_Risk_Calculator import *
from SensorList import *
import string


#When the program starts it reads every user from the Userlist.txt file and initialises Generic_User - Admin items
def initialise_users(current_dir):
    input_file = os.path.join(current_dir, 'Userlist.txt')
    Userlist = []
    with open(input_file, 'r', encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            try:
                namefromtxt, passfromtxt, isadmin = map(str.strip, line.split('|', maxsplit=2))
            except ValueError:
                print("Corrupt Userlist.txt file")
                exit(100110)
            if not int(isadmin):
                x = Generic_User(namefromtxt, passfromtxt)
                Userlist.append(x)
            else:
                x = Admin(namefromtxt, passfromtxt, isadmin)
                Userlist.append(x)

    return Userlist

class FRCS:
    def __init__(self):
        pass

#Login function, takes the users and passes them to validate_login function and if all is ok prints message.
    def login(self):
        success = 0
        current_directory = os.getcwd()
        Userslist = initialise_users(current_directory)
        while not success:
            inputname = input("Enter your username please: ")
            inputpassword = input("Enter your password please: ")
            for elem in Userslist:
                success, status = elem.validate_login(inputname, inputpassword)
                if success and status:
                    print(f"\nWelcome, {inputname}! You are logged in as admin!")
                    return status
                if success and not status:
                    print(f"\nWelcome, {inputname}! You are logged in as user!")
                    return status
            if not success:
                print("Incorrect credentials, try again.\n")
#Print welcoming message and options
    def welcome(self):
        print("      ______   _____     _____    _____\n     |  ____| |  __ \   / ____|  / ____|\n     | |__    | |__) | | |      | (___\n     |  __|   |  _  /  | |       \___ \\\n     | |      | | \ \  | |____   ____) |\n     |_|      |_|  \_\  \_____| |_____/\tby CinderSoft\n")
        print("Welcome to FRCS the ultimate fire risk calculation system\n")
        while True:
            print("CURRENT MENU OPTIONS:\n")
            wannalogin = input("LOGIN: Would you like to Login?(y/n)\n").lower()
            if wannalogin == "y":
                break
            elif wannalogin == "n":
                exit(100110)
            else:
                print("Invalid input. Please enter y/n.\n")

#Intermediate function to calculate the fire risk of a given forest. Takes the items initialised in main as arguments
    def FRCS_calculate_risk(self,sensorlistitem,parameterdataitem,mailinglist):
        y = Fire_Risk_Calculator()
        criticalsensorlist = y.calculate_risk(sensorlistitem, parameterdataitem) #calls the risk calculation function and returns a list of the critical sensors
        print("\nCritical state sensor list:")
        for item in criticalsensorlist:#prints fire danger index and rate of spread
            print(f"{item[0]}With FDI: {item[1]:.2f} and ROS: {item[2]/1000:.2f}Km/h\n")

        if(criticalsensorlist): #if the list is not empty as in, there are sensors whose readings are above a certain threshold
            run = True
            while run:
                choice = input("Would you like to send an Alert (y/n)?\n").lower()#asks the user to send a mail or not
                if choice == "y":
                    print(mailinglist.create_mailing_list(criticalsensorlist))
                    run = False
                elif choice == "n":
                    print("\nAlert not sent")
                    run = False
                else:
                    print("Invalid input. Please enter y/n.\n")


#Intermediate function to show the data of the chosen sensor.
    def FRCS_show_sensor_data(self, sensorlistitem):
        show = "all"
        listofallsensors = sensorlistitem.get_sensor(show)
        for item in listofallsensors:
            print(item)
        run = True
        while run:
            choose = input("Insert Sensor Id to view data: ")#after printing all sensors asks for a specific one to show full data
            try:
                choose = int(choose)
            except ValueError:
                print("\nInvalid input try again.\n")
                continue
            found = False
            for item in listofallsensors: #finds the sensor in the list and prints its data
                if item.getid() == choose:
                    found = True
                    print(f"\nFor the chosen sensor with id {choose} the data are as follows:\n")
                    toprint = item.printall()
                    print(toprint)
                    avgh, avgv, hum, vel = item.show_sensor_data()
                    print(f"Current humidity: {hum:.2f} Average: {avgh:.2f}\nCurrent velocity: {vel:.2f} Average: {avgv:.2f}")
                    run = False
            if not found:
                print("\nInvalid input\n")
#Intermediate function to check if the Userlist.txt exists and if the files for each sensor exist in the specified directory
    def FRCS_checkconnectivity(self, sensorlistitem):
        current_dir = os.getcwd()
        show = "all"
        listofallsensors = sensorlistitem.get_sensor(show)#prints all sensors
        for item in listofallsensors:
            print(item)
        run = True
        success_sensor = True
        while run:
            choose = input(
                "Show connectivity status and dependencies for all sensors and the user list? (y/n)? \n").lower()
            if choose == "y":
                success_sensor, failedsensorlist = sensorlistitem.checkConnectivity()#checks the input and if yes is chosen returns with a list of sensors that are broken
                run = False
            elif choose == "n":
                print("Returning to main menu...\n")
                run = False
                return
            else:
                print("Invalid input. Please enter y/n.\n")

        if success_sensor and os.path.exists(current_dir+"/Userlist.txt"):
            print("All sensors / user list are online!")
        elif not success_sensor and os.path.exists(current_dir+"/Userlist.txt"):
            print("Some sensors are offline!\n")
            for item in failedsensorlist:
                print(item)
        elif success_sensor and not os.path.exists(current_dir+"/Userlist.txt"):
            print("Userlist.txt missing!\n")
#Intermediate function to create a new user
    def FRCS_Create_User(self):
        while True:
            print("Name and password must not contain spaces\n")
            name = input("Give the name of the User: ")
            password = input("Give the password for the User: ")
            contain_whitespace = any(char1 in string.whitespace for char1 in name+password)
            if contain_whitespace:
                print("\nAt least one of the inputs contains whitespace characters.\n")
            else:
                print("None of the inputs contain whitespace characters.\n")
                break

        newuser = Generic_User(name, password)
        newuser.writetofile()
        print(newuser)
#Intermediate funtion to edit the data of a sensor
    def FRCS_Edit_Sensor_Data(self, sensorlistitem):
        show = "all"
        listofallsensors = sensorlistitem.get_sensor(show)
        for item in listofallsensors:
            print(item)
        run = True
        choice = 0
        selection = 0
        while run:
            choose = input("Insert Sensor Id to view data: ")
            try:
                choose = int(choose)
            except ValueError:
                print("Invalid input try again.")
                continue
            success = False
            for item in listofallsensors:
                if item.getid() == choose:
                    choice = item.showall()
                    success = True
                    selection = item
                    run = False
                    break
            if not success:
                print("Sensor does not exist. Try again")
        match choice:
            case "1":
                name = input("Insert new name (only text allowed, no whitespaces): ")
                nametemp = name
                nametemp = nametemp.replace(" ", "")  # Remove spacestemp
                if not nametemp.isalpha():
                    print("Only Text allowed in Username")
                else:
                    selection.edit_sensor_name(name)
                    print(f"Name edited successfully to {name}")
            case "2":
                print("Enter coordinates.\nCoordinates must be within (+/-90deg) and (+/-180 deg)\n")
                try:
                    coo1 = float(input("Enter Latitude: "))
                except ValueError:
                    print("Invalid input")
                    return
                try:
                    coo2 = float(input("Enter Longtitude: "))
                except ValueError:
                    print("Invalid input")
                    return
                if (coo1 <-90 or coo1 >90) or (coo2 < -180 or coo2 > 180):
                    print("Invalid input")
                else:
                    selection.edit_coordinates(coo1, coo2)
                    print("Coordinates updated successfully")
            case "3":
                filename=input("Enter new filename.\nFile name must end in .txt: ")
                if (filename.endswith(".txt")):
                    selection.edit_filename(filename)
                    print("File name updated successfully")
                else:
                    print("File name did not end in .txt")
            case "4":
                print("FQA must be between 0-27 t/Ha")
                FQA = input("Enter Fuel Quantity: ")
                try:
                    FQA =float(FQA)
                except ValueError:
                    print("Invalid input")
                    return
                if FQA<0 or FQA>27:
                    print("Invalid input")
                else :
                    selection.edit_fuel_quantity(FQA)
                    print("FQA updated successfully")
            case "5":
                Slope = input("Enter new Slope.\nSlope must be between +/-36deg: ")
                try:
                    Slope=float(Slope)
                except ValueError:
                    print("Invalid input")
                    return
                if Slope < -36 or Slope>36:
                    print("Invalid input")
                else:
                    selection.edit_slope(Slope)
                    print("Slope updated successfully")
            case "6":
                mcoffset = input("Offset must be between +/-10:\n")
                try:
                    mcoffset=float(mcoffset)
                except ValueError:
                    print("Invalid input")
                    return
                if mcoffset < -10 or mcoffset>10:
                    print("Invalid input")
                else:
                    selection.edit_offset_mc(mcoffset)
            case "7":
                avcoffset = input("Offset must be between +/-10\n")
                try:
                    avcoffset = float(avcoffset)
                except ValueError:
                    print("Invalid input")
                    return
                if avcoffset < -10 or avcoffset>10:
                    print("Invalid input")
                else:
                    selection.edit_offset_avc(avcoffset)
                    print("Offset updated successfully")
            case "8":
                selection.toggle_status()
            case _:
                print("\nSensor not edited. Returning to main menu.")
#Intermediate function to insert-initialise a new sensor
    def FRCS_monitor_setup(self,sensorlistitem):
        incorrect = True
        while incorrect:
            name = input("Insert new name (Only Text allowed in Username): ")
            nametemp = name
            nametemp = nametemp.replace(" ", "")
            if not nametemp.isalpha():
                print("Only Text allowed in Username\n")
            else:
                print(f"Name successfully set to {name}")
                incorrect = False
        incorrect=True
        while incorrect:
            ID = input("Insert ID (Only numbers allowed in ID): ")
            try:
                ID=int(ID)
            except:
                print("\nInvalid input\n")
                continue

            listofallsensors = sensorlistitem.get_sensor("all")
            IDfound = False
            for item in listofallsensors:
                if item.getid() == ID:
                    IDfound = True

            if IDfound:
                print("\nID Already exists in the system\n")
            else:
                print(f"ID successfully set to {ID}\n")
                incorrect=False
        incorrect = True
        while incorrect:
            print("Enter coordinates.\nCoordinates must be within (+/-90deg) and (+/-180 deg)\n")
            try:
                coo1 = float(input("Enter Latitude: "))
            except ValueError:
                print("Invalid input\n")
                continue
            try:
                coo2 = float(input("Enter Longtitude: "))
            except ValueError:
                print("Invalid input\n")
                continue
            if (coo1 < -90 or coo1 > 90) or (coo2 < -180 or coo2 > 180):
                print("Invalid input\n")
            else:
                print("Coordinates set successfully\n")
                incorrect=False
        incorrect = True
        while incorrect:
            filename = input("Enter new filename.\nFile name must end in .txt\n")
            if (filename.endswith(".txt") and os.path.exists(os.getcwd()+"/Sensors/"+filename)):
                print("File name successfully set\n")
                incorrect = False
            else:
                print("File name did not end in .txt or file does not exist\n")
        incorrect = True
        while incorrect:
            print("FQA must be between 0-27 t/Ha")
            FQA = input("Enter Fuel Quantity: ")
            try:
                FQA = float(FQA)
            except ValueError:
                print("Invalid input\n")
                continue
            if FQA < 0 or FQA > 27:
                print("Invalid input\n")
            else:
                print("FQA successfully set\n")
                incorrect = False
        incorrect = True
        while incorrect:
            Slope = input("Enter new Slope.\nSlope must be between +/-36deg: ")
            try:
                Slope = float(Slope)
            except ValueError:
                print("Invalid input\n")
                continue
            if Slope < -36 or Slope > 36:
                print("Invalid input\n")
            else:
                print("Slope successfully set\n")
                incorrect = False
        newsensor = Sensor(name, ID, (coo1, coo2), filename, FQA, Slope, True, 0.0, 0.0)
        sensorlistitem.addsensor(newsensor)
        print(f"Sensor {ID} added to the list")
#Function that handles printing the menu and after taking the input of the user-admin calls the correct function
    def Show_Menu(self, status,sensorlistitem, parameterdataitem,mailinglist):
        while True:
            print("\nMENU OPTIONS:")
            if not status:
                choice = input("(1) Fire Risk Calculation\n(2) Show Sensor Data\n(3) Check Connectivity\n(4) Exit\nInput: ")
                match choice:
                    case "1":
                        self.FRCS_calculate_risk(sensorlistitem,parameterdataitem,mailinglist)
                    case "2":
                        self.FRCS_show_sensor_data(sensorlistitem)
                    case "3":
                        self.FRCS_checkconnectivity(sensorlistitem)
                    case "4":
                        exit(100110)
                    case _:
                        print("\nInvalid argument")

            else:
                choice = input("(1) Fire Risk Calculation\n(2) Show Sensor Data\n(3) Check Connectivity\n(4) Edit Sensor Data\n(5) Edit Formula Parameters\n(6) Monitor Setup\n(7) Create User\n(8) Exit\nInput: ")
                match choice:
                    case "1":
                        self.FRCS_calculate_risk(sensorlistitem, parameterdataitem,mailinglist)
                    case "2":
                        self.FRCS_show_sensor_data(sensorlistitem)
                    case "3":
                        self.FRCS_checkconnectivity(sensorlistitem)
                    case "4":
                        self.FRCS_Edit_Sensor_Data(sensorlistitem)
                    case "5":
                        parameterdataitem.edit()
                    case "6":
                        self.FRCS_monitor_setup(sensorlistitem)
                    case "7":
                        self.FRCS_Create_User()
                    case "8":
                        exit(100110)
                    case _:
                        print("\nInvalid argument")
