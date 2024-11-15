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
    wh = 0.01 * (100 - soc) * batteryPack.Capacity
    
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
        data['Current delta'] = []
        data['Voltage delta'] = []
        data['realCurrent'] = []
        data['realResistance'] = []
        data['realVoltageDrop'] = []

    end = False

    while True:

        for row in reader:

            t += 1
            P = (float(row['kW']) * 1000)
            R = batteryPack.CurrentResistance(wh)
            # R = 1
            Voc = batteryPack.CurrentVoltage(wh)     
            I = ((-Voc) + math.sqrt(((-Voc) ** 2) - (4 * -R * -(P)))) / (2 * -R)
            Vdrop = I * R
            V = Voc - Vdrop
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
                rV = float(row['V'])
                rI = P / rV
                rVdrop = math.fabs(Voc - rV)
                if I == 0:
                    rR = 0
                else:
                    rR = rVdrop / rI
                
                # else:
                #     rR = rVdrop / rI
                # if rR > 1 or rR < 0:
                #     rR = 0
                data['realVoltageData'].append(rV)
                data['Voltage delta'].append(rV - V)
                data['Current delta'].append(rI - I)
                data['realCurrent'].append(rI)
                data['realResistance'].append(rR)
                data['realVoltageDrop'].append(rVdrop)

            data['VoltageData'].append(V)
            data['Voltage(no drop)Data'].append(Voc)
            data['TempData'].append(T)
            data['timeData'].append(t)
            data['ResistanceData'].append(R)
            data['LossData'].append(loss)
            data['CurrentData'].append(I)
            data['WattHourData'].append(wh)
            data['PowerData'].append(P / 1000)
            data['SOCData'].append(soc)
            data['VoltageDropData'].append(Vdrop)

        laps += 1
        if not(end) and (cont):          
            file.close()
            file = open('DriverProfiles/' + fileName, mode = 'r')
            reader = csv.DictReader(file)
        else:
            break
        
    data['Wh used'] = wh - (0.01 * (100 - stateOfCharge) * batteryPack.Capacity)
    data['laps'] = laps
    return data