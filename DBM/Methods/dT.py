import csv
import math

def ThermalProfile(T0, batteryPack, cont, stateOfCharge, fileName, title):

    file = open('CBM/DriverProfiles/' + fileName, mode = 'r')
    reader = csv.DictReader(file)

    t = 0.0
    laps = 0
    T = T0
    totalLoss = 0
    soc = stateOfCharge
    wh = 0.01 * (100 - soc) * batteryPack.Capacity
    # print(wh)
    V = batteryPack.CurrentVoltage(wh)
    # print(V)
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
        data['real average Temp (°C)'] = []

    if keys.__contains__('V'):
        data['real Voltage (V)'] = []

    end = False

    V_lag = 0.0
    dt = 0.1  

    while True:

        for row in reader:
            t += dt
            P = (float(row['kW']) * 1000)  # Power in watts
            R = batteryPack.CurrentResistance(wh)  # Current internal resistance
            Voc = batteryPack.CurrentVoltage(wh)  # Open-circuit voltage
            # print(P)
            # Calculate current if power is nonzero
            if P != 0:
                # P = (Voc - IR - V_lag)I
                # P = (Voc - IR - V_lag0 - dt(-Vlag0 + RI))I
                # P = (Voc - I(R + dt*R) - V_lag0(1 - dt))I
                # 0 = -R(1 + dt)I^2 + (Voc - V_lag0(1 - dt))I - P
                # 0 = R(1 + dt)I^2 - (Voc - V_lag0(1 - dt))I + P

                I = (((Voc - V_lag * (1 - dt)) 
                     - math.sqrt(((Voc - V_lag * (1 - dt)) ** 2) 
                                 - (4 * R * (1 + dt) * P))) 
                    / (2 * R * (1 + dt)))


                # I = (Voc - math.sqrt((Voc ** 2) - (4 * R * P))) / (2 * R)
            else:
                I = 0.0

            # Update the lag voltage using the RC dynamics
            V_lag += dt * (-V_lag + R * I)
            
            # Calculate terminal voltage
            Vdrop = R * I + V_lag
            V = Voc - Vdrop

            soc = 100 * (1 - (wh / batteryPack.Capacity))
            wh += (Voc * I) / 36000
            loss = Vdrop * I
            totalLoss += loss / 36000
            T += ((loss / 10) / (batteryPack.cellMass * batteryPack.cellK))
            # print(V)
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

            if keys.__contains__('V'):
                rV = float(row['V'])
                data['real Voltage (V)'].append(rV)

            if keys.__contains__('t1'):
                realtemps = []
                for key in keys:
                    if key.__contains__('t'):
                        realtemps.append((float(row[key]) - 32) * 5 / 9)
                data['real average Temp (°C)'].append(sum(realtemps) / len(realtemps))

            
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

        laps += 1
        if not(end) and (cont):          
            file.close()
            file = open('CDM/DriverProfiles/' + fileName, mode = 'r')
            reader = csv.DictReader(file)
        else:
            break
        
    data['Wh used'] = wh - (0.01 * (100 - stateOfCharge) * batteryPack.Capacity)
    data['Efficency'] = 100 - (100 * ((totalLoss) / data['Wh used']))
    data['laps'] = laps
    return data