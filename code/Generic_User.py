import os


class Generic_User:
    def __init__(self, name, password):
        self._name = name
        self._password = password


    def __str__(self):
        return f"Username: {self._name} \nPassword: {self._password}\nAdmin status:{False}"

    def printuser(self):
        print(self)

    def validate_login(self, name, password):
        if self._name == name and self._password == password:
            if hasattr(self, "_admin"):
                return True, True
            else:
                return True, False
        return False, False

    def writetofile(self):
        current_dir = os.getcwd()
        input_file = os.path.join(current_dir, 'Userlist.txt')
        with open(input_file, 'r+', encoding="utf-8") as file:
            lines = file.readlines()
            file.seek(0)
            new_line = f"{self._name}|{self._password}|0\n"
            lines.insert(0, new_line)
            file.writelines(lines)

class Admin(Generic_User):

    def __init__(self, name, password, isadmin):
        self._name = name
        self._password = password
        isadmin = int(isadmin)
        self._admin = bool(isadmin)

    def __str__(self):
        return f"Username: {self._name} \nPassword: {self._password}\nAdmin status:{self._admin}"
