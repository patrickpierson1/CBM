import matplotlib.pyplot as plt
class melasta14Ah:
    def __init__(self):

        self.mass = 0.240 # kg
        # self.resistance = 0.0012 # Ohms
        self.K = 850 # Specific heat: J/(kg T)
        self.ampacity = 14 # ah
        self.maxCrate = 15
        self.contCrate = 10

        self.maxVoltage = 4.35
        self.minVoltage = 3.0
        self.nomVoltage = 3.8
        # self.setCapacity()
        self.capacity = 56.1
        
        
        
    # def setCapacity(self):
    #     self.capacity = quad(self.Vah, 0, self.ampacity)[0]

    # V(wh) = i wh^3 + j wh^2 + kwh + d
    
    def V(self, wh):
        return (((-3.3551716243743436e-13)*(wh**9))+
                ((7.802316780932224e-11)*(wh**8))+
                ((-7.595611758964299e-09)*(wh**7))+
                ((4.0215841161928824e-07)*(wh**6))+
                ((-1.2598779101816262e-05)*(wh**5))+
                ((0.00023799490005382568)*(wh**4))+
                ((-0.0026384054568509506)*(wh**3))+
                ((0.015951784780236962)*(wh**2))+
                ((-0.06433233461856949)*(wh**1))+
                ((4.362999914921135)))
                   
    # constant resistance
    def R(self, wh):
        return ((2.054816449031329e-09*(wh**4)) -
                (2.532535289792294e-07*(wh**3)) +
                (1.060724073545955e-05)*(wh**2) -
                (0.00018181841193232553*(wh)) + 
                (0.0021894134490824746))
    
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
# cell = melasta14Ah()
# ax = plt.gca()
# ax.xaxis.set_tick_params(width=2)  # Thicker x-axis ticks
# ax.yaxis.set_tick_params(width=2)  # Thicker y-axis ticks
# # ax.invert_xaxis()
# ax.grid(linewidth=1)

# Vd = []
# Vm = []
# soc = []
# R = []
# r = []
# for i in range(0, int(cell.capacity) * 100 + 1000):
#     wh = i / 100
#     soc.append(wh)
#     if (cell.V(wh) > cell.minVoltage):
#         Vd.append(cell.V(wh))
#         R.append(cell.R(wh) * 1000)
#         r.append(1.2)
#     if (cell.Vwh(wh) > cell.minVoltage):
#         Vm.append(cell.Vwh(wh))
# print(soc[len(Vd) - 1])
# print(sum(Vd) / len(Vd))
# print(sum(R) / len(R))
# plt.plot(soc[0:len(Vd)], Vd, label='Tested Voltage', color='blue', linewidth=2)  # Adjust color and width as needed
# plt.plot(soc[0:len(Vm)], Vm, label='Simulated Voltage', color='orange', linewidth=2)  # Adjust color and width as needed
# # plt.plot(soc[0:len(Vd)], R, label='tested Resistance', color='blue', linewidth=2)  # Adjust color and width as needed
# # plt.plot(soc[0:len(r)], r, label='Datasheet Resistance', color='orange', linewidth=2, linestyle = 'dashed')  # Adjust color and width as needed

# plt.legend(loc='upper right', fontsize=10)  # Adjust legend font size

# # plt.axhline(y=cell.minVoltage, color='red', linestyle = 'dashed', label = 'Minimum voltage')  # Adjust y, color, style, and width as needed
# # plt.axvline(x=100, color='black', linewidth=2)  # Adjust y, color, style, and width as needed
# plt.ylabel('Resistance (mOhm)')
# plt.xlabel('Energy Consumed (Wh)')
# plt.title('Melasta 14ah - Simulated Voltage vs Tested Voltage')
# # plt.title('Melasta 14ah - Datasheet Resistance vs Tested Resistance')
# plt.show()