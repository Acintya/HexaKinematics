import numpy as np

# Geometrical parameters [mm]
R_B = 119.435
R_P = 44.045
d = 20.1
phi = [0, -120, -120, -240, -240, 0]

class HexaModel(object):
    def __init__(self, name):
        self.name = name
        self.InitHexaParams()

    def InitHexaParams(self):
        if len(phi) != 6:
            return

        self.actuatorPos = []
        self.sphereJointPos = []
        self.orientationA = []

        index = 1
        for angle in phi:
            a_x = R_B * np.cos((angle * np.pi / 180 + np.power(-1, index) * np.arcsin(d / (2 * R_B))))
            a_y = R_B * np.sin((angle * np.pi / 180 + np.power(-1, index) * np.arcsin(d / (2 * R_B))))
            a_z = 0
            a_pos = [a_x, a_y, a_z]
            self.actuatorPos.append(a_pos)

            c_x = R_P * np.cos((angle * np.pi / 180 + np.power(-1, index) * np.arcsin(d / (2 * R_P))))
            c_y = R_P * np.sin((angle * np.pi / 180 + np.power(-1, index) * np.arcsin(d / (2 * R_P))))
            c_z = 0
            c_pos = [c_x, c_y, c_z]
            self.sphereJointPos.append(c_pos)

            index += 1

        alpha = -90
        beta = phi
        gamma = 0
        self.orientationA.append(alpha)
        self.orientationA.append(beta)
        self.orientationA.append(gamma)

        self.baseLink = 106
        self.plattformLink = 190

    def InverseKinematic(self, pos, orientation):
        # output for the angles of six acuators
        self.q_a = []
        #generate homogeneous transformation matrix T_p
        #compute the vector r_c, which describs the position of C_i with respect to A_i
        for i in range(6):
            alphaA = -90 * np.pi / 180
            betaA = self.orientationA[1][i] * np.pi / 180
            gammaA = 0
            a_i_x = self.actuatorPos[i][0]
            a_i_y = self.actuatorPos[i][1]
            a_i_z = self.actuatorPos[i][2]
            T_A_i = np.array([[np.cos(betaA) * np.cos(gammaA), -1 * np.cos(betaA) * np.sin(gammaA), np.sin(betaA), a_i_x],
                             [np.sin(alphaA) * np.sin(betaA) * np.cos(gammaA) + np.cos(alphaA) * np.sin(gammaA), (-1) * np.sin(alphaA) * np.sin(betaA) * np.sin(gammaA) + np.cos(alphaA) * np.cos(gammaA), (-1) * np.sin(alphaA) * np.cos(betaA), a_i_y],
                             [(-1) * np.cos(alphaA) * np.sin(betaA) * np.cos(gammaA) + np.sin(alphaA) * np.sin(gammaA), np.cos(alphaA) * np.sin(betaA) * np.sin(gammaA) + np.sin(alphaA) * np.cos(gammaA), np.cos(alphaA) * np.cos(gammaA), a_i_z],
                             [0, 0, 0, 1]
                              ])
            T_A_i_inv = np.linalg.inv(T_A_i)

            alphaOrientation = orientation[0]
            betaOrientation = orientation[1]
            gammaOrientation = orientation[2]
            R_p_x = np.array([[1, 0, 0],
                              [0, np.cos(alphaOrientation), -np.sin(alphaOrientation)],
                              [0, np.sin(alphaOrientation), np.cos(alphaOrientation)]
                              ])
            R_p_y = np.array([[np.cos(betaOrientation), 0, np.sin(betaOrientation)],
                              [0, 1, 0],
                              [-np.sin(betaOrientation), 0, np.cos(betaOrientation)]
                              ])
            R_p_z = np.array([[np.cos(gammaOrientation), -np.sin(gammaOrientation), 0],
                              [np.sin(gammaOrientation), np.cos(gammaOrientation), 0],
                              [0, 0, 1]
                              ])
            R_p = np.dot(R_p_x, R_p_y)
            R_p = np.dot(R_p, R_p_z)
            np.resize(R_p, (4, 4))

            effectorPosVector = [pos[0], pos[1], pos[2], 1]
            T_p = np.vstack((R_p, [0, 0, 0]))
            T_p = np.insert(T_p, 3, values=effectorPosVector, axis=1)

            # r_ci = T_Ai^-1 * T_p * c_i
            c_i_vector = self.sphereJointPos[i]
            c_i_vector.append(1)
            np.reshape(c_i_vector, (4, 1))


            r_C_i = np.dot(T_A_i_inv, T_p)
            r_C_i = np.dot(r_C_i, c_i_vector)
            x_c_i = r_C_i[0]
            y_c_i = r_C_i[1]
            z_c_i = r_C_i[2]

            k = -2 * x_c_i * self.baseLink
            l = -2 * y_c_i * self.baseLink
            m = x_c_i * x_c_i + y_c_i * y_c_i + z_c_i * z_c_i + self.baseLink * self.baseLink - self.plattformLink * self.plattformLink
            q_a_i = (np.arctan2(m, np.sqrt(k * k + l * l - m * m) - np.arctan2(k, l))) * 180 / np.pi
            self.q_a.append(q_a_i)

        return self.q_a


