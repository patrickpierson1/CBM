from scipy.integrate import quad

class Cell:
    def __init__(self, mass, resistance, k, ampacity, maxVoltage, minVoltage, nomVoltage, maxCrate, contCrate):

        self.mass = mass # kg
        self.resistance = resistance # Ohms
        self.K = k # Specific heat: J/(kg T)
        self.ampacity = ampacity # ah
        self.maxCrate = maxCrate
        self.contCrate = contCrate

        self.maxVoltage = maxVoltage
        self.minVoltage = minVoltage
        self.nomVoltage = nomVoltage 
        self.setCapacity()
        
    def setCapacity(self):
        self.capacity = quad(self.Vah, 0, self.ampacity)[0]

    # V(wh) = i wh^3 + j wh^2 + kwh + d
    def V(self, wh):
        d = self.maxVoltage
        c = self.c(self.capacity)
        b = self.b(self.capacity)
        a = self.a(self.capacity)
        return ((a * (wh ** 3))
                + (b * (wh **2))
                + (c * (wh))
                + (d))
    
    # constant resistance
    def R(self, wh):
        return self.resistance 
    
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