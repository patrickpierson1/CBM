import matplotlib.pyplot as plt
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
    def Vwh(self, ah):
        d = self.maxVoltage
        c = self.c(self.capacity)
        b = self.b(self.capacity)
        a = self.a(self.capacity)
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
cell = molicellP42A()
ax = plt.gca()
ax.xaxis.set_tick_params(width=2)  # Thicker x-axis ticks
ax.yaxis.set_tick_params(width=2)  # Thicker y-axis ticks
# ax.invert_xaxis()
ax.grid(linewidth=1)

Vd = []
Vm = []
soc = []
R = []
r = []
for i in range(0, int(cell.capacity) * 100 + 100):
    wh = i / 100
    if (cell.V(wh) > cell.minVoltage):
        Vd.append(cell.V(wh))
        R.append(cell.R(wh) * 1000)
        r.append(14)
    if (cell.Vwh(wh) > cell.minVoltage):
        Vm.append(cell.Vwh(wh))
    
    soc.append(wh)
 

plt.plot(soc[0:len(Vd)], Vd, label='Test Data Voltage', color='blue', linewidth=2)  # Adjust color and width as needed
plt.plot(soc[0:len(Vm)], Vm, label='Calculated Voltage', color='orange', linewidth=2)  # Adjust color and width as needed
# plt.plot(soc[0:len(Vd)], R, label='Measured Resistance', color='blue', linewidth=2)  # Adjust color and width as needed
# plt.plot(soc[0:len(r)], r, label='Datasheet Resistance', color='orange', linewidth=2, linestyle = 'dashed')  # Adjust color and width as needed

plt.legend(loc='upper right', fontsize=10)  # Adjust legend font size

# plt.axhline(y=cell.minVoltage, color='red', linestyle = 'dashed', label = 'Minimum voltage')  # Adjust y, color, style, and width as needed
# plt.axvline(x=100, color='black', linewidth=2)  # Adjust y, color, style, and width as needed
plt.ylabel('mili-ohms')
plt.xlabel('watt-hours consumed')
plt.show()