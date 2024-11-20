

def MaxPkw(batteryPack):

    data = {}
    data['Max Peak Power (kW)'] = []
    data['Max Continuous Power (kW)'] = []
    data['M State of charge (%)'] = []
    data['C State of charge (%)'] = []
    data['SOC'] = []


    data['batteryPack'] = batteryPack

    whMax = 0
    whCont = 0
    
    foundDischargeLimit = False

    while True:
        VM = batteryPack.CurrentVoltage(whMax)
        VC = batteryPack.CurrentVoltage(whCont)
        R = batteryPack.CurrentResistance(whMax)
        Imax, Icont = MaxCurrent(VM, VC, R, batteryPack)

        VdropMax = Imax * R
        
        Vmax = VM - VdropMax
        Pmax = Vmax * Imax
        whMax += Pmax / 3600

        VdropCont = Icont * R
        
        Vcont = VC - VdropCont
        Pcont = Vcont * Icont
        whCont += Pcont / 3600

        if Icont != batteryPack.contDischarge and not(foundDischargeLimit):
            data['Discharge Limit'] = Pcont / 1000
            foundDischargeLimit = True

        
        data['Max Peak Power (kW)'].append(Pmax/ 1000)
        data['Max Continuous Power (kW)'].append(Pcont/ 1000)
        data['M State of charge (%)'].append(((batteryPack.Capacity - whMax) / batteryPack.Capacity) * 100)
        data['C State of charge (%)'].append(((batteryPack.Capacity - whCont) / batteryPack.Capacity) * 100)

        # if VC <= batteryPack.minVoltage:
        #     break
        # if wh >= batteryPack.Capacity:
        #     break
        if Icont <= 1:
            break
    
    for i in range(11):
        wh = ((i / 10) * batteryPack.Capacity)
        data['SOC'].append(((100 - (10 * i)), (wh / 1000)))
    
    return data

def MaxCurrent(VM, VC, R, batteryPack):
    
    Imax = batteryPack.maxDischarge
    Icont = batteryPack.contDischarge


    if VC - (Icont * R) <= batteryPack.minVoltage * 1.01:
        Icont = (VC - (batteryPack.minVoltage * 1.01)) / R
    if VM - (Imax * R) <= batteryPack.minVoltage * 1.01:
        Imax = (VM - (batteryPack.minVoltage * 1.01)) / R

    return Imax, Icont
    