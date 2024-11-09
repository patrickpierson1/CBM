# discharge profile of a cell with respect to ah consumed
def CellAhDischargeProfile(cell, T0):

    currents = [0.1, 1, 5, 10, 20, 30]

    data = {}
    data['temps'] = []
    data['times'] = []

    for I in currents:
        V = cell.maxVoltage
        ah = 0
        
        t = 0
        Vdata = []
        ahdata = []

        T = T0

        while V >= cell.minVoltage:
            
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

            V = cell.V(ah, cell.ampacity)
        
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
        V = batteryPack.maxVoltage
        wh = 0
        
        t = 0
        Vdata = []
        whdata = []

        T = T0

        while V >= batteryPack.minVoltage:
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

                
        

        
