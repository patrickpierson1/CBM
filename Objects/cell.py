import numpy as np
from scipy.integrate import quad

# initial slope condition:
c = -0.25

class Cell:
    def __init__(self, mass, resistance, k, ampacity, maxVoltage, minVoltage, nomVoltage, maxCrate):

        self.mass = mass # kg
        self.resistance = resistance # Ohms
        self.k = k # Specific heat: J/(kg T)
        self.ampacity = ampacity # ah
        self.maxCrate = maxCrate

        self.maxVoltage = maxVoltage # V
        self.minVoltage = minVoltage # V
        self.nomVoltage = nomVoltage # V

        self.D = self.maxVoltage
        self.C = c
        self.B = self.b()
        self.A = self.a(self.B)

        self.setCapacity()

        self.K = (2 * c) / self.ampacity
        self.J = self.j()
        self.I = self.i(self.J)
        
    def setCapacity(self):
        self.capacity = quad(self.Vah, 0, self.ampacity)[0]
    
    def b(self):
        return (((3 * ((4 * self.nomVoltage)
                        - (3 * self.maxVoltage)
                        - (self.minVoltage))) 
                    / (self.ampacity ** 2))
                - ((3 * c) / self.ampacity))
    
    def a(self, b):
        return (((4 * (self.nomVoltage - self.maxVoltage)) / (self.ampacity ** 3))
         - ((2 * c) / (self.ampacity ** 2))
         - ((4 * b) / (3 * self.ampacity)))
        
    def Vah(self, x):
        return ((self.A * (x ** 3))
                + (self.B * (x **2))
                + (self.C * (x))
                + (self.D))
    
    def j(self):
        return (((3 * ((4 * self.nomVoltage)
                        - (3 * self.maxVoltage)
                        - (self.minVoltage))) 
                    / (self.capacity ** 2))
                - ((3 * self.K) / self.capacity))
        
    def i(self, j):
        return (((4 * (self.nomVoltage - self.maxVoltage)) / (self.capacity ** 3))
         - ((2 * self.K) / (self.capacity ** 2))
         - ((4 * j) / (3 * self.capacity)))
    
    def V(self, wh):
        return ((self.I * (wh ** 3))
                + (self.J * (wh **2))
                + (self.K * (wh))
                + (self.D))
        
    def R(self, x):
        q = 5
        p = 1.3
        return (self.resistance + 
                ((1.2 * self.resistance - self.resistance) * ((1 - (x / self.capacity))**q) * np.cos(x)) -
                ((self.resistance - (2 * self.resistance)) * ((x / self.capacity)**p))) 