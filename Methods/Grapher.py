import matplotlib.pyplot as plt

def GraphTP(data, selected, title):
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))

    for key in selected:
        plt.plot(data['time (s)'], data[key], label = key)

    text = ('end Voltage: ' + str(round(data['Voltage (V)'][-1], 2)) + '\n' +
               'kWh used: ' + str(round(data['Wh used'] / 1000, 2)) + '\n' +
               'Wh loss: ' + str(round(sum(data['Losses (W)']) / 3600, 2)) + '\n' +
               'minutes: ' + str(round(data['time (s)'][-1] / 60, 2)) + '\n' +
               'laps: ' + str(data['laps']) + '\n' +
               'end Temp ' + str(round(data['Temperature (°C)'][-1], 2)) + '\n' +
               'Efficency: ' + str(round(data['Efficency'], 2)) + '%')
    
    
    if data.keys().__contains__('Accuracy'):
        text += '\nAccuracy: ' + str(round(data['Accuracy'], 2)) + '%'
    
    props = dict(boxstyle='round', facecolor='grey', alpha=0.15)  # bbox features
    ax.text(1.03, 0.98, text, transform=ax.transAxes, fontsize=12, verticalalignment='top', bbox=props)
    plt.tight_layout()
    plt.legend()
    plt.grid()
    plt.show()

def GraphDP(data, type1, type2, title):
    fig = plt.figure()
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
    plt.legend()
    plt.xlabel(type1 + ' used')
    plt.ylabel(type2 + ' Voltage')
    plt.title(title)
    plt.show()   

def GraphVsoc(data, title):
    fig = plt.figure(figsize=(8,4))
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

        if len(data.keys()) == 1:
            if data[key].keys().__contains__('Discharge Limit'):
                plt.hlines(data[key]['Discharge Limit'], 0, 100, color = 'red', label = key + 'Max discharge limit', linestyle = 'dashed')


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
    plt.legend()
    
    i = 0
    if showData:
        for t in text:
            props = dict(boxstyle='round', facecolor='grey', alpha=0.15)  # bbox features
            ax.text(1.03, 1 - (i * (1/len(text))), t, transform=ax.transAxes, fontsize=9, verticalalignment='top', bbox=props)
            i += 1
    plt.tight_layout()         
    
    plt.show()