
class molicellP42A:
    def __init__(self):

        self.mass = 0.07 # kg
        self.resistance = 0.016 # Ohms
        self.K = 830 # Specific heat: J/(kg T)
        self.ampacity = 4.2 # ah
        self.maxCrate = 11
        self.contCrate = 7

        self.maxVoltage = 4.2
        self.minVoltage = 2.5
        self.nomVoltage = 3.6 
        # self.setCapacity()
        self.capacity = self.nomVoltage * self.ampacity
        
        
        
    # def setCapacity(self):
    #     self.capacity = quad(self.Vah, 0, self.ampacity)[0]

    # V(wh) = i wh^3 + j wh^2 + kwh + d
    
    def V(self, wh):
        return ((-0.0010026288424835525*(wh**3)) +
                (0.016872148199448996*(wh**2)) -
                (0.12682887577639235*(wh)) +
                (4.204924198718271))
    # constant resistance
    def R(self, wh):
        return ((2.8428042114002936e-06*(wh**4)) -
                (8.521904508774402e-05*(wh**3)) +
                (0.000898953287697768)*(wh**2) -
                (0.004059380957155576*(wh)) + 
                (0.023445877378438087))
    
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