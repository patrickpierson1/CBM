import matplotlib.pyplot as plt

def GraphTP(data, selected, title):
    fig = plt.figure()
    for key in selected:
        plt.plot(data['timeData'], data[key], label = key)

    plt.grid()
    plt.legend()
    plt.title(title)
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
    fig = plt.figure()
    plt.plot(data['State of Charge'], data['OC Voltage'])
    plt.grid()
    plt.ylabel('Open Circuit Voltage')
    plt.xlabel('State of Charge')
    plt.title(title)
    plt.show()   

def GraphPkwh(data, title):
    fig = plt.figure()
    plt.plot(data['kWh consumed'], data['Max Power (kW)'])
    ma = max(data['Max Power (kW)'])
    mi = min(data['Max Power (kW)'])
    colors = ['lime', 'limegreen', 'forestgreen', 'green', 'darkgreen', 'goldenrod', 'darkgoldenrod', 'chocolate', 'coral', 'red', 'crimson']
    # colors.reverse()
    c = 0
    for i in data['SOC']:
        plt.vlines(i[1], mi, ma, label = str(i[0]), color = colors[c], linestyle = 'dashed')
        c += 1
    
    if data.keys().__contains__('Discharge Limit'):
        plt.hlines(data['Discharge Limit'], 0, max(data['kWh consumed']), color = 'red', label = 'Max discharge limit', linestyle = 'dashed')

    plt.xlabel('kWh consumed')
    plt.ylabel('Max kW achivable')
    plt.title(title)
    plt.grid()
    plt.legend()
    plt.show()