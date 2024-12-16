# discharge profile of a cell with respect to ah consumed
def CellAhDischargeProfile(cell, T0):

    # currents = [0.5, 1, 3, 5, 10, 15, 20]
    # currents = [0.01]
    currents = []
    
    curC = 0.5
    
    while curC <= cell.maxCrate:
        currents.append(curC * cell.ampacity)
        if curC == cell.maxCrate:
            break
        elif curC * 2 > cell.maxCrate:
            curC = cell.maxCrate
        else:
            curC *= 2

    data = {}
    data['temps'] = []
    data['times'] = []

    for I in currents:

        ah = 0
        wh = 0
        t = 0
        Vdata = []
        ahdata = []
        T = T0

        while True:
            
            V = cell.Vah(ah)
            R = cell.R(wh)
            Vdrop = I * R
            V -= Vdrop
            
            # P = V * I
            # wh += P/3600

            loss = (I**2) * R

            ah += I/3600
            # ah += loss / (V * 3600)
            # wh += loss / (3600)


            Vdata.append(V)
            ahdata.append(ah)

            t += 1
            T += ((loss) / (cell.mass * cell.K))

            if V <= cell.minVoltage:
                break
        
        data[str(I)] = (ahdata, Vdata)
        data['temps'].append(T)
        data['times'].append(t)
        
    return data

# discharge profile of a cell with respect to ah consumed
def CellWhDischargeProfile(cell, T0):

    currents = [0.5, 1, 3, 5, 10, 15, 20]

    data = {}
    data['temps'] = []
    data['times'] = []

    for I in currents:

        wh = 0
        t = 0
        Vdata = []
        ahdata = []
        T = T0

        while True:
            
            V = cell.V(wh)
            R = cell.R(wh)
            P = I * V
            Vdrop = I * R
            V -= Vdrop

            loss = (I**2) * R

            wh += P/3600
            wh += loss / (V * 3600)

            Vdata.append(V)
            ahdata.append(wh)

            t += 1
            T += ((loss) / (cell.mass * cell.K))

            if V <= cell.minVoltage:
                break
        
        data[str(I)] = (ahdata, Vdata)
        data['temps'].append(T)
        data['times'].append(t)
        
    return data

def PackWhDischargeProfile(batteryPack, T0):

    currents = [5, 10, 20, 30, 50, 75, 100]

    data = {}
    data['temps'] = []
    data['times'] = []

    for I in currents:
        
        wh = 0
        t = 0
        Vdata = []
        whdata = []
        T = T0

        while True:
            
            V = batteryPack.CurrentVoltage(wh)
            R = batteryPack.CurrentResistance(wh)
            Vdrop = I * R
            V -= Vdrop
            P = V * I

            loss = (I**2) * R

            wh += P/3600
            wh += loss / (3600)

            Vdata.append(V)
            whdata.append(wh)

            t += 1
            T += ((loss) / (batteryPack.cellMass * batteryPack.cellK))

            if V <= batteryPack.minVoltage:
                break

        data[str(I)] = (whdata, Vdata)
        data['temps'].append(T)
        data['times'].append(t)
        
    return data