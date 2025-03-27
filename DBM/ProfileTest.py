from os import scandir
from Objects.BatteryPack import BatteryPack
from DBM.Objects.SavedCells.Samsung50s import Cell
from Methods.dT import ThermalProfile

def calculate(FileName):
    samsung50s = Cell(0.07,0.013,830,5,4.2,2.5,3.6,9,5)
    V66 = BatteryPack(110,3, samsung50s)

    soc0 = 41
    allDis = []
    allSoc = []

    minDis = None
    minSoc = None
    for i in range(60):
        soc = soc0 + i
        data = ThermalProfile(20, V66, False, soc, FileName, '')
        
        total = 0
        n = 0
        
        for i in range(len(data['real Voltage (V)'])):
            total += (data['real Voltage (V)'][i] - data['Voltage (V)'][i])
            n += 1

        dis = abs(float(total) / float(n))

        allDis.append(dis)
        allSoc.append(soc)

        if minDis == None:
            minDis = dis
            minSoc = soc
        
        if minDis > dis:
            minDis = dis
            minSoc = soc

        print(str(soc) + ' : ' + str(dis))

    print('Lowest discrepency: ' + str(minDis) + ' at ' + str(minSoc) + ' soc')

def FindDriverProfiles():
    files = []
    for entry in scandir('DriverProfiles'):
        if entry.is_file():
            name = entry.name
            t = name.split('.')
            type = t[1]
            if type == 'csv':
                files.append(name)
        
    return files

if __name__ == "__main__":
    files = FindDriverProfiles()
    # print(files)
    calculate('rc_95-Endurance-2nd Half (Bryce)kWandT.csv')