
class BatteryPack:
    def __init__(self, series, parallel, cell):
        self.Series = series
        self.Parallel = parallel
        self.Cell = cell
        self.cellMass = self.Cell.mass * self.Series * self.Parallel
        self.cellK = self.Cell.k

        self.RConnections = 0.45

        self.ampacity = self.Cell.ampacity * self.Parallel
        
        self.minVoltage = self.Series * self.Cell.minVoltage
        self.maxVoltage = self.Series * self.Cell.maxVoltage
        self.nomVoltage =  self.Series * self.Cell.nomVoltage
        self.Capacity = self.Cell.capacity * self.Series * self.Parallel
        self.maxDischarge = self.Cell.maxCrate * self.Cell.ampacity * self.Parallel
    

    def CurrentResistance(self, wh):
        
        return (self.Cell.R(wh / (self.Series * self.Parallel)) * self.Series / self.Parallel) + self.RConnections
    
    def CurrentVoltage(self, wh):
        return self.Series * self.Cell.V((wh / (self.Series * self.Parallel)))