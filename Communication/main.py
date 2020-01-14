from Communication import environment
from Model import HexaModel
import numpy as np

#socket communication
env = environment.UnityEnvironment()
print ("****** env quit *****")

hexa_iwf = HexaModel.HexaModel ("IWF_Hexa", 360, 51.96, 51.6, [0, -120, -120, -240, -240, 0])

pos = [0, 0, -300]
orientation = [0, 0, 0]
hexa_iwf.InverseKinematic(pos, orientation)



