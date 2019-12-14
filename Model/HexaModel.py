class HexaModel(object):
    def __init__(self, name, actuatorPos, sphereJointPos, orientationAlpha, orientationBeta, orientationGamma, baseLink,
                 plattformLink, radiusBase, radiusPlattform, distance):
        self.name = name
        self.actuatorPos = actuatorPos,
        self.sphereJointPos = sphereJointPos,
        self.orientationAlpha = orientationAlpha,
        self.orientationBeta = orientationBeta,
        self.orientationGamma = orientationGamma,
        self.baseLink = baseLink,
        self.plattformLink = plattformLink,
        self.radiusBase = radiusBase,
        self.radiusPlattform = radiusPlattform,
        self.distance = distance