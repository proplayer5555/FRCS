from Parameter_Data import *
from SensorList import *
import math

class Fire_Risk_Calculator():
    def __init__(self):
        pass

    def calculate_risk(self,sensorlistitem, paramaterdataitem):
        parameters = paramaterdataitem.get_parameters()
        sensorlist = sensorlistitem.getsensordata()

        output = []

        for item in sensorlist:
            fdi , rof = self.calculate(item, parameters)
            output.append((fdi, rof, item[0]))
        threshold = 1000
        criticalsensorlist = []
        for item in output:
            if item[0] > threshold:
                criticalsensorlist.append((sensorlistitem.get_sensor(item[2]), item[0], item[1]))
        return criticalsensorlist

    def calculate(self,sensoras,parameters):
        slope = sensoras[1]
        MC = float(sensoras[2]) + float(sensoras[5])
        U = float(sensoras[3]) + float(sensoras[6])
        AFQ = sensoras[4]

        #In case offset is too much
        if (MC < 0):
            MC = 0.0
        if (U < 0):
            U = 0.0

        Yj = parameters[0] - parameters[1] * MC + parameters[2] * MC * MC
        Aj = parameters[3] * MC * math.exp(parameters[4] * MC) + parameters[5]
        Nj = parameters[6] - parameters[7] * pow(MC, parameters[8])
        FDI = Yj + Aj * math.exp(U * Nj)


        if (AFQ < 8):
            FQCF = 0.1 + (1.02 / (1 + 7266.83 * math.exp(-1.362 * AFQ)))
        else:
            if (MC < 9):
                FQCF = (6.03 + 5.81 * AFQ) / 53.44
            elif (MC < 18):
                FQCF = (11.19 + 2.92 * AFQ) / 35.02
            else:
                FQCF = (0.055 + 0.0023 * AFQ) / 0.074

        if slope > 0:
            SlopeCorrection = math.exp(0.069 * slope)
        else:
            SlopeCorrection = math.exp(-0.069 * slope) / (2 * math.exp(-0.069 * slope) - 1)

        ROF = SlopeCorrection * FQCF * FDI

        return FDI, ROF