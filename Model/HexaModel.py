import numpy as np

class HexaModel(object):
    def __init__(self, name, R_B, R_P, d, phi):
        self.name = name
        self.InitHexaParams(R_B, R_P, d, phi)

    def InitHexaParams(self, R_B, R_P, d, phi):
        if len(phi) != 6:
            return 'asd'

        self.actuatorPos = []
        self.sphereJointPos = []
        self.orientationA = []

        for angle in phi:
            a_pos = []
            index = phi.index(angle)
            a_x = R_B * np.cos((angle + np.power(-1, index) * np.arcsin(d / (2 * R_B))) * np.pi / 180)
            a_pos.append(a_x)
            a_y = R_B * np.sin((angle + np.power(-1, index) * np.arcsin(d / (2 * R_B))) * np.pi / 180)
            a_pos.append(a_y)
            a_z = 0
            a_pos.append(a_z)
            self.actuatorPos.append(a_pos)

            c_pos = []
            c_x = R_P * np.cos((angle + np.power(-1, index) * np.arcsin(d / (2 * R_P))) * np.pi / 180)
            c_pos.append(c_x)
            c_y = R_P * np.sin((angle + np.power(-1, index) * np.arcsin(d / (2 * R_P))) * np.pi / 180)
            c_pos.append(c_y)
            c_z = 0
            c_pos.append(c_z)
            self.sphereJointPos.append(c_pos)

            orientation = []
            alpha = -90
            orientation.append(alpha)
            beta = angle
            orientation.append(beta)
            gamma = 0
            orientation.append(gamma)
            self.orientationA.append(orientation)

        self.baseLink = 240
        self.plattformLink = 564

    def InverseKinematic(self, pos, rotation):
        self.q_a = []
        for i in range(6):
            #k = -2 * self.sphereJointPos[0] * self.baseLink
            #l = -2 * self.sphereJointPos[1] * self.baseLink
            #m = self.sphereJointPos[0] * self.sphereJointPos[0] + self.sphereJointPos[1] * self.sphereJointPos[1] + self.sphereJointPos[2] * self.sphereJointPos[2] + self.baseLink * self.baseLink + self.plattformLink * self.plattformLink
            q_a_i = (np.arctan2(m, np.sqrt(k * k + l * l - m * m) - np.arctan2(k, l))) * 180 / np.pi
            self.q_a.append(q_a_i)
        print(self.q_a)
