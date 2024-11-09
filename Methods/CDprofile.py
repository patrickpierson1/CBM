from Objects.cell import Cell
import matplotlib.pyplot as plt


def DischargeProfile(cell):


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

        T = 20

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
        

                
        

        
