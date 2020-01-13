from Communication import environment
from Model import HexaModel
import numpy as np

def InitHexaModel(model):
    model.name = "Hexa_IWF"
    #model.actuatorPos = ,
    #sphereJointPos, orientationAlpha, orientationBeta, orientationGamma, baseLink, plattformLink

hexa_iwf = HexaModel.HexaModel ("IWF_Hexa", 360, 51.96, 51.6, [0, -120, -120, -240, -240, 0])
InitHexaModel(hexa_iwf)
hexa_iwf.InverseKinematic()
env = environment.UnityEnvironment()
print ("****** env quit *****")

