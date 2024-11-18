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
    plt.plot(data['State of charge (%)'], data['Max Power (kW)'])
    plt.gca().invert_xaxis()
    
    if data.keys().__contains__('Discharge Limit'):
        plt.hlines(data['Discharge Limit'], 0, 100, color = 'red', label = 'Max discharge limit', linestyle = 'dashed')

    plt.xlabel('State of charge (%)')
    plt.ylabel('Max kW achivable')
    plt.title(title)
    plt.grid()
    plt.legend()
    plt.show()