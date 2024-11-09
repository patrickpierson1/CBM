import numpy as np
from scipy.integrate import quad

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
        self.setCapacity()
        
    def setCapacity(self):
        self.capacity = quad(self.V, 0, self.ampacity, args = (self.ampacity))[0]

    def V(self, x, m):
        q = 3
        p = 4
        return (self.nomVoltage + 
                ((self.maxVoltage - self.nomVoltage) * ((1 - (x / m))**q)) -
                ((self.nomVoltage - self.minVoltage) * ((x / m)**p)))
        
    def R(self, x, m):
        q = 2
        p = 10
        return (self.resistance + 
                ((1.2 * self.resistance - self.resistance) * ((1 - (x / m))**q)) -
                ((self.resistance - 2 * self.resistance) * ((x / m)**p)))