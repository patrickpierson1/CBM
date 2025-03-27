import numpy as np
import matplotlib.pyplot as plt
from os import scandir
from cell import Cell

CO = 0
# I = 0

def getFiles():
    files = []
    print("Select one of the following files:")
    i = 0
    for entry in scandir('DBM\TestData'):
        files.append(entry.name)
        print(str(i) + ": " + entry.name)
        i += 1
    
    return files

def getData(fileName):

    t = []
    V = []
    R = []
    file = open('DBM\TestData\\' + fileName, mode = 'r')
    for line in file:
        if line[0] == '/' and line[1] == '/':
            continue
        elif line[0:3] == "CO:":
            CO = float(line[4:-1])
        else:
            data = line.split(';')
            t.append(float(data[0]))
            V.append(float(data[1]))
            R.append((float(data[2]) - CO) / 1000)
    return t, V, R

def graphV(wh, V):
    

    # samsung50s = Cell(0.07,0.013,830,5.22,4.2,2.5,3.6,9,5)

    # vcalc = []

    # for i in wh:
    #     vcalc.append(samsung50s.V(i))
    #     if vcalc[-1] < 2.5:
    #         break


    plt.scatter(wh, V, color = 'r', s = 1, label = 'Data')
    a, b, c, d = LFB_V(wh, V)
    print('Voltage Line of best fit: ' + str(a) + 'x^3 + ' + str(b) + 'x^2 + ' + str(c) + 'x + ' + str(d))
    plt.plot(wh, a*(wh**3) + b*(wh**2) + c*wh + d, color = 'b', label = 'Line of best fit')
    # plt.plot(wh[0:len(vcalc)], vcalc, color = 'g', label = 'Modeled voltage')
    plt.legend()
    plt.xlabel('Wh')    
    plt.ylabel('Voltage')
    plt.grid()
    plt.show()

def graphR(wh, R):
    
    plt.scatter(wh, R, color = 'r', s = 1, label = 'Data')
    a, b, c, d, e = LFB_R(wh, R)
    print('Resistance Line of best fit: ' + str(a) + 'x^4 + ' + str(b) + 'x^3 + ' + str(c) + 'x^2 + ' + str(d) + 'x + ' + str(e))
    plt.plot(wh, a*(wh**4) + b*(wh**3) + c*(wh**2) + d*wh+e, color = 'b', label = 'Line of best fit')
    plt.legend()
    plt.plot()
    plt.grid()
    plt.show()

def LFB_R(wh, R):
    a, b, c, d, e = np.polyfit(wh, R, 4)
    return a, b, c, d, e

def LFB_V(wh, V):
    a, b, c, d = np.polyfit(wh, V, 3)
    return a, b, c, d

def convertToWh(t, V, I):
    wh = []
    total = 0
    prev = 0
    # wh.append(total)
    for i in range(len(t)):
        time = float(t[i] * 60)
        dt = time - prev
        prev = time
        cur = (V[i] * I * dt) / 3600
        total += cur
        wh.append(total)
        # print(total)
    return wh

def main():
    
    files = getFiles()
    fileName = files[int(input("Enter file number: "))]    
    t, V, R = getData(fileName)
    I = 3
    wh = convertToWh(t, V, I)
    # graphV(np.array(wh), np.array(V))
    graphR(np.array(wh), np.array(R))

main()