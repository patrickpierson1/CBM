
class mollicellP50B:
    def __init__(self):

        self.mass = 0.07 # kg
        self.resistance = 0.013 # Ohms
        self.K = 830 # Specific heat: J/(kg T)
        self.ampacity = 5.22 # ah
        self.maxCrate = 9
        self.contCrate = 5

        self.maxVoltage = 4.2
        self.minVoltage = 2.5
        self.nomVoltage = 3.6 
        # self.setCapacity()
        self.capacity = self.nomVoltage * self.ampacity
        
        
        
    # def setCapacity(self):
    #     self.capacity = quad(self.Vah, 0, self.ampacity)[0]

    # V(wh) = i wh^3 + j wh^2 + kwh + d
    
    def V(self, wh):
        return ((-0.0005765195243976844*(wh**3)) +
                (0.011583831124273847*(wh**2)) -
                (0.10283815053158879*(wh)) +
                (4.199404493564835))
    # constant resistance
    def R(self, wh):
        return ((6.003454079908092e-07*(wh**4)) -
                (2.2788963597369644e-05*(wh**3)) +
                (0.0003014188006422359)*(wh**2) -
                (0.0016783757827011977*(wh)) + 
                (0.013695419182316364))
    
    # V(ah) = a ah^3 + b ah^2 + c ah + d
    def Vah(self, ah):
        d = self.maxVoltage
        c = self.c(self.ampacity)
        b = self.b(self.ampacity)
        a = self.a(self.ampacity)
        return ((a * (ah ** 3))
                + (b * (ah ** 2))
                + (c * (ah))
                + (d))

    # coeficient equations
    def c(self, m):
        return (self.minVoltage - self.maxVoltage) / m
    
    def b(self, m):
        return (6 / (m ** 2)) * ((2 * self.nomVoltage) 
                                              - self.maxVoltage 
                                              - self.minVoltage)
        
    def a(self, m):
        return (-6 / (m ** 3)) * ((2 * self.nomVoltage) 
                                              - self.maxVoltage 
                                              - self.minVoltage)