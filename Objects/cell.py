import numpy as np
from scipy.integrate import quad

# initial slope condition:


class Cell:
    def __init__(self, mass, resistance, k, ampacity, maxVoltage, minVoltage, nomVoltage, maxCrate):

        self.mass = mass # kg
        self.resistance = resistance # Ohms
        self.K = k # Specific heat: J/(kg T)
        self.ampacity = ampacity # ah
        self.maxCrate = maxCrate

        self.maxVoltage = maxVoltage
        self.minVoltage = minVoltage
        self.nomVoltage = nomVoltage 
        self.setCapacity()
        
    def setCapacity(self):
        self.capacity = quad(self.Vah, 0, self.ampacity)[0]

    # V(wh) = i wh^3 + j wh^2 + kwh + d
    def V(self, wh):
        d = self.maxVoltage
        k = self.k()
        j = self.j(k)
        i = self.i(j, k)
        return ((i * (wh ** 3))
                + (j * (wh **2))
                + (k * (wh))
                + (d))
    
    # constant resistance
    def R(self, wh):
        return self.resistance 
    
    # V(ah) = a ah^3 + b ah^2 + c ah + d
    def Vah(self, ah):
        d = self.maxVoltage
        c = self.c()
        b = self.b()
        a = self.a(b)
        return ((a * (ah ** 3))
                + (b * (ah ** 2))
                + (c * (ah))
                + (d))

    # coeficient equations
    def c(self):
        return - 0.5 * self.maxVoltage / self.ampacity 
    
    def b(self):
        c = self.c()
        return (((3 * ((4 * self.nomVoltage)
                    - (3 * self.maxVoltage)
                    - (self.minVoltage))) 
                    / (self.ampacity ** 2))
                - ((3 * c) / self.ampacity))
        
    def a(self, b):
        c = self.c()
        return (((4 * (self.nomVoltage - self.maxVoltage)) / (self.ampacity ** 3))
            - ((2 * c) / (self.ampacity ** 2))
            - ((4 * b) / (3 * self.ampacity)))
    
    def k(self):
        return - 0.5 * self.maxVoltage / self.capacity
        
    def j(self, k):
        return (((3 * ((4 * self.nomVoltage)
                            - (3 * self.maxVoltage)
                            - (self.minVoltage))) 
                        / (self.capacity ** 2))
                    - ((3 * k) / self.capacity))
            
    def i(self, j, k):
        return (((4 * (self.nomVoltage - self.maxVoltage)) / (self.capacity ** 3))
            - ((2 * k) / (self.capacity ** 2))
            - ((4 * j) / (3 * self.capacity)))       