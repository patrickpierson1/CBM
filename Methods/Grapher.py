import matplotlib.pyplot as plt

def GraphTP(data, selected):
    fig = plt.figure()
    for key in selected:
        plt.plot(data['timeData'], data[key], label = key)

    plt.grid()
    plt.legend()
    plt.show()

def GraphDP(data, type1, type2):
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
    plt.show()   

def GraphVsoc(data):
    fig = plt.figure()
    plt.plot(data['State of Charge'], data['OC Voltage'])
    plt.grid()
    plt.ylabel('Open Circuit Voltage')
    plt.xlabel('State of Charge')
    plt.show()   