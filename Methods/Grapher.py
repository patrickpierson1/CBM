import matplotlib.pyplot as plt

def GraphTP(data, selected, title):
    # fig = plt.figure()
    # for key in selected:
    #     plt.plot(data['timeData'], data[key], label = key)

    # plt.grid()
    # plt.legend()
    # plt.title(title)
    # plt.show()


    fig, ax = plt.subplots(1, 1, figsize=(8, 4))

    for key in selected:
        plt.plot(data['timeData'], data[key], label = key)

    my_text = ('end Voltage: ' + str(round(data['VoltageData'][-1], 2)) + '\n' +
               'kWh used: ' + str(round(data['Wh used'] / 1000, 2)) + '\n' +
               'Wh loss: ' + str(round(sum(data['LossData']) / 3600, 2)) + '\n' +
               'minutes: ' + str(round(data['timeData'][-1] / 60, 2)) + '\n' +
               'laps: ' + str(data['laps']) + '\n' +
               'end Temp ' + str(round(data['TempData'][-1], 2)))

    # my_text += fr'$\mu=${mu:.3f}' + '\n' + fr'$\sigma=${sigma:.3f}'

    
    props = dict(boxstyle='round', facecolor='grey', alpha=0.15)  # bbox features
    ax.text(1.03, 0.98, my_text, transform=ax.transAxes, fontsize=12, verticalalignment='top', bbox=props)
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
    fig = plt.figure()
    plt.plot(data['State of Charge'], data['OC Voltage'])
    plt.grid()
    plt.ylabel('Open Circuit Voltage')
    plt.xlabel('State of Charge')
    plt.title(title)
    plt.show()   

def GraphPkwh(data, title):
    fig = plt.figure()
    plt.plot(data['State of charge (%)'], data['Max Power (kW)'], label = 'Max Power (kW)')
    # plt.plot(data['State of charge (%)'], data['Max Current (Amps)'], label = 'Max Current (Amps)')
    plt.gca().invert_xaxis()
    
    if data.keys().__contains__('Discharge Limit'):
        plt.hlines(data['Discharge Limit'], 0, 100, color = 'red', label = 'Max discharge limit', linestyle = 'dashed')

    plt.xlabel('State of charge (%)')
    plt.title(title)
    plt.grid()
    plt.legend()
    plt.show()