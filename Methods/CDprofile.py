# discharge profile of a cell with respect to ah consumed
def CellAhDischargeProfile(cell, T0):

    currents = [0.1, 1, 5, 10, 20, 30]

    data = {}
    data['temps'] = []
    data['times'] = []

    for I in currents:

        ah = 0
        t = 0
        Vdata = []
        ahdata = []
        T = T0

        while True:
            
            V = cell.Vah(ah)
            R = cell.R(ah, cell.ampacity)
            Vdrop = I * R
            V -= Vdrop

            loss = (I**2) * R

            ah += I/3600
            ah += loss / (V * 3600)

            Vdata.append(V)
            ahdata.append(ah)

            t += 1

            T += ((loss) / (cell.mass * cell.k))

            if V <= cell.minVoltage:
                break
        
        data[str(I)] = (ahdata, Vdata)
        data['temps'].append(T)
        data['times'].append(t)
        
    return data

# discharge profile of a cell with respect to ah consumed
def CellWhDischargeProfile(cell, T0):

    currents = [0.1, 1, 5, 10, 20, 30]

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
            R = cell.R(wh, cell.capacity)
            P = I * V
            Vdrop = I * R
            V -= Vdrop

            loss = (I**2) * R

            wh += P/3600
            wh += loss / (V * 3600)

            Vdata.append(V)
            ahdata.append(wh)

            t += 1

            T += ((loss) / (cell.mass * cell.k))

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