import csv
import math

def ThermalProfile(T0, batteryPack, cont, stateOfCharge, fileName, title):

    file = open('DriverProfiles/' + fileName, mode = 'r')
    reader = csv.DictReader(file)

    t = 0.0
    laps = 0
    T = T0
    totalLoss = 0
    soc = stateOfCharge
    wh = 0.01 * (100 - soc) * batteryPack.Capacity
    
    keys = []

    for key in reader.fieldnames:
        keys.append(key)

    data = {}
    data['Open Circuit Voltage (V)'] = []
    data['Voltage (V)'] = []
    data['Temperature (°C)'] = []
    data['Current (A)'] = []
    data['Watt-hours consumed (Wh)'] = []
    data['Power (kW)'] = []
    data['time (s)'] = []
    data['Resistance (ohms)'] = []
    data['State of Charge (%)'] = []
    data['Losses (W)'] = []
    data['Voltage Drop (V)'] = []

    if keys.__contains__('t1'):
        data['real Temperature 1 (°C)'] = []
    if keys.__contains__('t2'):
        data['real Temperature 2 (°C)'] = []
    if keys.__contains__('V'):
        data['real Voltage (V)'] = []

    end = False

    while True:

        for row in reader:

            t += 1
            P = (float(row['kW']) * 1000)
            R = batteryPack.CurrentResistance(wh)
            Voc = batteryPack.CurrentVoltage(wh)     
            I = ((-Voc) + math.sqrt(((-Voc) ** 2) - (4 * -R * -(P)))) / (2 * -R)
            Vdrop = I * R
            V = Voc - Vdrop
            soc = 100 * (1 - (wh / (batteryPack.Capacity)))
            wh += P / 3600
            loss = ((I ** 2) * (R))
            totalLoss += loss / 3600
            wh += (loss) / 3600
            T += ((loss) / (batteryPack.cellMass * batteryPack.cellK))
            
            if V <= batteryPack.minVoltage:
                end = True
                data['break'] = 'Dropped below minimum Voltage'
                break
            if T >= 60:
                end = True
                data['break'] = 'Over heated above 60 degrees'
                break
            if V >= batteryPack.maxVoltage * 1.05:
                end = True
                data['break'] = 'Reached maximum Voltage'
                break

            if I >= batteryPack.maxDischarge:
                end = True
                data['break'] = 'Maximum discharge fault'
                break
            if keys.__contains__('t1'):
                data['real Temperature 1 (°C)'].append((float(row['t1']) - 32) * 5 / 9)
            if keys.__contains__('t2'):
                data['real Temperature 2 (°C)'].append((float(row['t2']) - 32) * 5 / 9)
            if keys.__contains__('V'):
                rV = float(row['V'])
                data['real Voltage (V)'].append(rV)

            data['Voltage (V)'].append(V)
            data['Open Circuit Voltage (V)'].append(Voc)
            data['Temperature (°C)'].append(T)
            data['time (s)'].append(t)
            data['Resistance (ohms)'].append(R)
            data['Losses (W)'].append(loss)
            data['Current (A)'].append(I)
            data['Watt-hours consumed (Wh)'].append(wh)
            data['Power (kW)'].append(P / 1000)
            data['State of Charge (%)'].append(soc)
            data['Voltage Drop (V)'].append(Vdrop)

        laps += 1
        if not(end) and (cont):          
            file.close()
            file = open('DriverProfiles/' + fileName, mode = 'r')
            reader = csv.DictReader(file)
        else:
            break
        
    data['Wh used'] = wh - (0.01 * (100 - stateOfCharge) * batteryPack.Capacity)
    data['Efficency'] = 100 - (100 * ((totalLoss) / data['Wh used']))
    data['laps'] = laps
    return data