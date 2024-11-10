import csv
import math

def ThermalProfile(T0, batteryPack, cont, stateOfCharge, fileName):

    file = open('DriverProfiles/' + fileName, mode = 'r')
    reader = csv.DictReader(file)

    t = 0.0
    laps = 0
    T = T0
    totalLoss = 0
    soc = stateOfCharge
    wh = 0.01 * (100- soc) * batteryPack.Capacity
    
    keys = []

    for key in reader.fieldnames:
        keys.append(key)

    data = {}
    data['Voltage(no drop)Data'] = []
    data['VoltageData'] = []
    data['TempData'] = []
    data['CurrentData'] = []
    data['WattHourData'] = []
    data['PowerData'] = []
    data['timeData'] = []
    data['ResistanceData'] = []
    data['SOCData'] = []
    data['LossData'] = []
    data['VoltageDropData'] = []

    if keys.__contains__('t1'):
        data['realTempData 1'] = []
    if keys.__contains__('t2'):
        data['realTempData 2'] = []
    if keys.__contains__('V'):
        data['realVoltageData'] = []

    end = False

    while True:

        for row in reader:

            t += 1
            P = (float(row['kW']) * 1000)
            R = batteryPack.CurrentResistance(wh)
            V = batteryPack.CurrentVoltage(wh)     
            I = ((-V) + math.sqrt(((-V) ** 2) - (4 * -R * -(P)))) / (2 * -R)
            Vdrop = I * R
            V -= Vdrop
            soc = 100 * (1 - (wh / (batteryPack.Capacity)))
            wh += P / 3600
            loss = ((I ** 2) * (R))
            totalLoss += loss
            wh += (loss) / 3600
            T += ((loss) / (batteryPack.cellMass * batteryPack.cellK))

            if soc == 0:
                print('Dropped below minimum capacity')
                end = True
                break
            if V <= batteryPack.minVoltage:
                print('Dropped below min Voltage')
                end = True
                break
            if T >= 60:
                print('Over heated above 60 degrees')
                end = True
                break
            if V >= batteryPack.maxVoltage * 1.05:
                print('max Voltage Achived')
                end = True
                break
            if soc > 100:
                print('max Capacity Achived')
                end = True
                break
            if I >= batteryPack.maxDischarge:
                print('max discharge fault')
                end = True
                break
            if keys.__contains__('t1'):
                data['realTempData 1'].append((float(row['t1']) - 32) * 5 / 9)
            if keys.__contains__('t2'):
                data['realTempData 2'].append((float(row['t2']) - 32) * 5 / 9)
            if keys.__contains__('V'):
                data['realVoltageData'].append(float(row['V']))

            data['VoltageData'].append(V)
            data['Voltage(no drop)Data'].append(V + Vdrop)
            data['TempData'].append(T)
            data['timeData'].append(t)
            data['ResistanceData'].append(R)
            data['LossData'].append(loss)
            data['CurrentData'].append(I)
            data['WattHourData'].append(wh)
            data['PowerData'].append(P / 1000)
            data['SOCData'].append(soc)
            data['VoltageDropData'].append(Vdrop)

        if not(end) and (cont):          

            laps += 1
            file.close()
            file = open('DriverProfiles/' + fileName, mode = 'r')
            reader = csv.DictReader(file)
        else:
            break

    print('end Voltage: ' + str(round(V, 2)))
    print('kWh used: ' + str(round(wh / 1000, 2)))
    print('Wh loss: ' + str(round(totalLoss / 3600, 2)))
    print('minutes: ' + str(round(t / 60, 2)))
    print('Laps: ' + str(laps))
    print('end Temp: ' + str(round(T, 2)))
    print()
    return data