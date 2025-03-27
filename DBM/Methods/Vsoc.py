
def Vsoc(batteryPack):
    wh = 0
    V = batteryPack.maxVoltage
    soc = 100
    I = 10
    data = {}
    data['OC Voltage'] = []
    data['State of Charge'] = []
    while True:
        data['OC Voltage'].append(V)
        data['State of Charge'].append(soc)
        P = I * V
        wh += P / 3600
        V = batteryPack.CurrentVoltage(wh)
        soc = 100 * (1 - (wh / batteryPack.Capacity))

        if V <= batteryPack.minVoltage:
            break
        if soc == 0:
            break
    
    return data
