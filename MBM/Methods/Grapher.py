import matplotlib.pyplot as plt

def GraphTP(data, selected, showData):
    fig, ax = plt.subplots(1, 1, figsize=(10, 4))
    text = []
    realParms = []
    for key in data.keys():

        for parameter in selected:
            if parameter.__contains__('real'):
                if not(realParms.__contains__(parameter)):
                    plt.plot(data[key]['time (s)'], data[key][parameter], label = parameter)
                    realParms.append(parameter)
            else:
                plt.plot(data[key]['time (s)'], data[key][parameter], label = key + ': ' + parameter)
            

        curText = (key + '\n' +
                'end Voltage: ' + str(round(data[key]['Voltage (V)'][-1], 2)) + '\n' +
                'kWh used: ' + str(round(data[key]['Wh used'] / 1000, 2)) + '\n' +
                'Wh loss: ' + str(round(sum(data[key]['Losses (W)']) / 36000, 2)) + '\n' +
                'minutes: ' + str(round(data[key]['time (s)'][-1] / 60, 2)) + '\n' +
                'laps: ' + str(data[key]['laps']) + '\n' +
                'end Temp ' + str(round(data[key]['Temperature (°C)'][-1], 2)) + '\n' +
                'Efficency: ' + str(round(data[key]['Efficency'], 2)) + '%')
        
        if data[key].__contains__('break'):
            curText += '\n' + data[key]['break']

        text.append(curText)
    plt.legend(fontsize = 6)
    plt.grid()
    i = 0
    if showData:
        for t in text:
            props = dict(boxstyle='round', facecolor='grey', alpha=0.15)
            ax.text(1.03, 1 - (i * (1/len(text))), t, transform=ax.transAxes, fontsize=9, verticalalignment='top', bbox=props)
            i += 1
    plt.tight_layout()
    plt.show()

def GraphDP(data, type1, type2, title):
    fig = plt.figure(figsize=(10,4))
    i = 0
    for key in data.keys():
        if key == 'temps' or key == 'times':
            continue
        st = (str(key) + ' amps; ' + 
            'max temp: ' + str(round(data['temps'][i], 2)) + ' C; ' +
            'in: ' + str(round(data['times'][i]/60, 2)) + ' minutues')
        plt.plot(data[key][0], data[key][1], label = st)
        i += 1

    plt.grid()
    plt.legend(fontsize = 6)
    plt.xlabel(type1 + ' used')
    plt.ylabel(type2 + ' Voltage')
    plt.title(title)
    plt.show()   

def GraphVsoc(data, title):
    fig = plt.figure(figsize=(10,4))
    plt.plot(data['State of Charge'], data['OC Voltage'])
    plt.gca().invert_xaxis()
    plt.grid()
    plt.ylabel('Open Circuit Voltage')
    plt.xlabel('State of Charge')
    plt.title(title)
    plt.show()   

def GraphPkwh(data, showData):
    fig, ax = plt.subplots(1, 1, figsize=(10, 4))
    text = []
    i = 0
    for key in data.keys():
        
        if i > 1:
            break
        plt.plot(data[key]['M State of charge (%)'], data[key]['Max Peak Power (kW)'], label = key + 'Max Peak Power (kW)', linestyle = '--')
        plt.plot(data[key]['C State of charge (%)'], data[key]['Max Continuous Power (kW)'], label = key + 'Max Continuous Power (kW)')
        
        batteryPack = data[key]['batteryPack']

        if data[key].keys().__contains__('cont Discharge Limit'):   
            plt.scatter(data[key]['cont Discharge Limit'][1], data[key]['cont Discharge Limit'][0], color = 'red', zorder = 2)
        
        if data[key].keys().__contains__('max Discharge Limit'):
            plt.scatter(data[key]['max Discharge Limit'][1], data[key]['max Discharge Limit'][0], color = 'red', zorder = 2)

        text.append(key + '\n' + 
            'Cell Mass: ' + str(round(batteryPack.cellMass, 2)) + ' Kg\n' +
            'Max Voltage: ' + str(round(batteryPack.maxVoltage, 2)) + ' Volts\n' +
            'Nominal Voltage: ' + str(round(batteryPack.nomVoltage, 2)) + ' Volts\n' +
            'Min Voltage: ' + str(round(batteryPack.minVoltage, 2)) + ' Volts\n' +
            'Capacity: ' + str(round(batteryPack.Capacity / 1000, 2)) + ' kWh\n' +
            'Peak current: ' + str(round(batteryPack.maxDischarge, 2)) + ' Amps\n' +
            'Continuous current: ' + str(round(batteryPack.contDischarge, 2)) + ' Amps\n' +
            'Resistance: ' + str(round(batteryPack.CurrentResistance(0), 2)) + ' ohms')
        i += 1

    plt.gca().invert_xaxis()
    plt.title('Max Power vs SOC')
    plt.xlabel('State of charge (%)')
    plt.ylabel('Max Power (kW)')
    plt.grid()
    plt.legend(fontsize = 6)
    
    i = 0
    if showData:
        for t in text:
            props = dict(boxstyle='round', facecolor='grey', alpha=0.15)
            ax.text(1.03, 1 - (i * (1/len(text))), t, transform=ax.transAxes, fontsize=9, verticalalignment='top', bbox=props)
            i += 1
    plt.tight_layout()         
    
    plt.show()