import matplotlib.pyplot as plt

def GraphTP(data, selected):
    fig = plt.figure()
    for key in selected:
        plt.plot(data['timeData'], data[key], label = key)

    plt.grid()
    plt.legend()
    plt.show()

def GraphDP(data):
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
    plt.xlabel('amp hours used')
    plt.ylabel('cell Voltage')
    plt.show()
        