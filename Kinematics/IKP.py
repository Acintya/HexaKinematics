from Model import HexaModel

class IKP(object):

    def __init__(self, name, score):
        self.name = name
        self.score = score

    def InversKinematic(Hexamodel):
        print("%s: %s" % (self.name, self.score))

ikp = IKP(747, 555)
ikp.print_socre()