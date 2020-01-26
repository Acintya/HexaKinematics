from Model import HexaModel
import numpy as np
import zmq
import json
import time

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")



while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % message)
    message = json.loads(message)
    RequestType = message["Type"]
    #print("Received request: %s" % _effector_position)

    #  Send reply back to client
    #  In the real world usage, after you finish your work, send your output here
    if RequestType == "IKP":
        start = time.clock()

        hexa_iwf = HexaModel.HexaModel("IWF_Hexa")
        _effector_position = message["EndEffectorPosition"]
        _effector_orientation = message["EndEffectorOrientation"]
        acuatorAngels = hexa_iwf.InverseKinematic(_effector_position, _effector_orientation)

        elapsed = (time.clock() - start) * 1000 #[ms]

        relOutOfRange = False
        for angle in acuatorAngels:
            if np.isnan(angle):
                relOutOfRange = True
                break;
        if relOutOfRange:
            IKPRes = {"ResState": "Failed", "Message": "The pose of end-effector is out of range."}
            socket.send_json(IKPRes)
        else:
            IKPRes = {"ResState": "OK", "AcuatorAngels": acuatorAngels, "CalcTime": elapsed}
            socket.send_json(IKPRes)

    elif RequestType == "FKP":
        socket.send(b"FKP")
    else:
        socket.send(b"Wrong type of request.")

