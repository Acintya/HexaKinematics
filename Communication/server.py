from Model import HexaModel
import zmq
import json

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
        hexa_iwf = HexaModel.HexaModel("IWF_Hexa", 360, 51.96, 51.6, [0, -120, -120, -240, -240, 0])
        _effector_position = message["EndEffectorPosition"]
        _effector_orientation = message["EndEffectorOrientation"]
        acuatorAngels = hexa_iwf.InverseKinematic(_effector_position, _effector_orientation)
        IKPRes = {"AcuatorAngels": acuatorAngels}
        socket.send_json(IKPRes)
    elif RequestType == "FKP":
        socket.send(b"FKP")
    else:
        socket.send(b"Wrong type of request.")

