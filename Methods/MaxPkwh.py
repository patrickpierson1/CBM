

def MaxPkw(batteryPack):

    data = {}
    data['Max Power (kW)'] = []
    data['State of charge (%)'] = []
    data['Max Current (Amps)'] = []
    data['SOC'] = []

    wh = 0
    
    foundDischargeLimit = False

    while True:
        V = batteryPack.CurrentVoltage(wh)
        R = batteryPack.CurrentResistance(wh)
        I = MaxCurrent(wh, batteryPack)

        Vdrop = I * R
        
        V -= Vdrop
        P = V * I
        wh += P / 3600
        if I != batteryPack.maxDischarge and not(foundDischargeLimit):
            data['Discharge Limit'] = P / 1000
            foundDischargeLimit = True
        
        data['Max Power (kW)'].append(P / 1000)
        data['Max Current (Amps)'].append(I)
        data['State of charge (%)'].append(((batteryPack.Capacity - wh) / batteryPack.Capacity) * 100)

        if V <= batteryPack.minVoltage:
            break
        if wh >= batteryPack.Capacity:
            break
        if I <= 1:
            break
    
    for i in range(11):
        wh = ((i / 10) * batteryPack.Capacity)
        data['SOC'].append(((100 - (10 * i)), (wh / 1000)))
    
    return data

def MaxCurrent(wh, batteryPack):
    V = batteryPack.CurrentVoltage(wh)
    R = batteryPack.CurrentResistance(wh)
    I = batteryPack.maxDischarge

    if V - (I * R) > batteryPack.minVoltage * 1.01:
        return I
    else:
        Vdrop = V - (batteryPack.minVoltage * 1.01)
        return (Vdrop / R)