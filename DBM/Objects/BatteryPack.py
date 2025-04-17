class BatteryPack:
    def __init__(self, series, parallel, cell):
        self.Series = series
        self.Parallel = parallel
        self.Cell = cell
        self.cellMass = self.Cell.mass * self.Series * self.Parallel
        self.cellK = self.Cell.K

        self.RConnections = 0.15

        self.ampacity = self.Cell.ampacity * self.Parallel
        
        self.minVoltage = self.Series * self.Cell.minVoltage
        self.maxVoltage = self.Series * self.Cell.maxVoltage
        self.nomVoltage =  self.Series * self.Cell.nomVoltage
        self.Capacity = self.Cell.capacity * self.Series * self.Parallel
        self.maxDischarge = self.Cell.maxCrate * self.Cell.ampacity * self.Parallel
        self.contDischarge = self.Cell.contCrate * self.Cell.ampacity * self.Parallel
    

    def CurrentResistance(self, wh):
        return (self.Cell.R(wh / (self.Series * self.Parallel)) * self.Series / self.Parallel) + self.RConnections
    
    def CurrentVoltage(self, wh):
        # print(self.Cell.V(wh / (self.Series * self.Parallel)))
        return self.Series * self.Cell.V((wh / (self.Series * self.Parallel)))