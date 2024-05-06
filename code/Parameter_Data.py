class Parameter_Data:
    def __init__(self):
        self._par1 = 21.37
        self._par2 = 3.42
        self._par3 = 0.085
        self._par4 = 48.09
        self._par5 = -0.6
        self._par6 = 11.9
        self._par7 = 0.44
        self._par8 = 0.0096
        self._par9 = 1.05

    def get_parameters(self):
        list = []
        list.append(self._par1)
        list.append(self._par2)
        list.append(self._par3)
        list.append(self._par4)
        list.append(self._par5)
        list.append(self._par6)
        list.append(self._par7)
        list.append(self._par8)
        list.append(self._par9)
        return list

    def __str__(self):
        return f"Parameter 1: {self._par1} \tParameter 2: {self._par2}\nParameter 3: {self._par3} \tParameter 4: {self._par4}\nParameter 5: {self._par5}\tParameter 6: {self._par6}\nParameter 7: {self._par7}\tParameter 8: {self._par8}\nParameter 9: {self._par9}\n"

    def edit(self):
        while True:
            print(self)
            parameter_name = input("Enter the parameter you want to change (_par1, _par2, etc.): ")
            if not hasattr(self, parameter_name):
                print(f"\nInvalid parameter name: {parameter_name}.\n")
                continue
            try:
                new_value = float(input("Enter the new value for the parameter: "))
            except ValueError:
                print(f"\nInvalid parameter value.\n")
                continue

            setattr(self, parameter_name, new_value)
            print(f"Parameter {parameter_name} updated successfully to {new_value}.")
            break
