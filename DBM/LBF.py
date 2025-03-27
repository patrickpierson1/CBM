import numpy as np
import matplotlib.pyplot as plt
from os import scandir

CO = 0

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
            R.append(float(data[2]) - CO)
    return t, V, R

def graphV(t, V):
    
    plt.scatter(t, V)
    a, b, c, d = LFB_V(t, V)
    plt.plot(t, a*(t**3) + b*(t**2) + c*t + d, color = 'b')
    plt.show()

def graphR(t, R):
    
    plt.scatter(t, R, color = 'r')
    a, b, c, d, e = LFB_R(t, R)
    plt.plot(t, a*(t**4) + b*(t**3) + c*(t**2) + d*t+e, color = 'b')
    plt.show()

def LFB_R(t, R):
    a, b, c, d, e = np.polyfit(t, R, 4)
    return a, b, c, d, e

def LFB_V(t, V):
    a, b, c, d = np.polyfit(t, V, 3)
    return a, b, c, d

def main():
    
    files = getFiles()
    fileName = files[int(input("Enter file number: "))]
    t, V, R = getData(fileName)
    
    graphV(np.array(t), np.array(V))
    graphR(np.array(t), np.array(R))

main()