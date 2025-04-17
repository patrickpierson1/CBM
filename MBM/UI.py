from os import scandir
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon
import sys
import csv
from Objects.BatteryPack import BatteryPack
from Objects.cell import Cell
from Methods.dT import ThermalProfile
from Methods.Vsoc import Vsoc
from Methods.MaxPkwh import MaxPkw
from Methods.Grapher import (GraphTP, 
                            GraphDP, 
                            GraphVsoc,
                            GraphPkwh)
from Methods.CDprofile import (CellAhDischargeProfile,
                                CellWhDischargeProfile,
                                PackWhDischargeProfile,)

# global variables
T0 = 20.0
soc = 100
continuous = True

class Setup(QWidget):
    def __init__(self):
        super().__init__()
        MainLayout = QHBoxLayout()
        self.CellLayout = QVBoxLayout()
        self.BatteryPackLayout = QVBoxLayout()

        self.SetUpCell()
        self.SetUpBatteryPack()

        self.submit = QPushButton('Submit Parameters')
        self.submit.clicked.connect(self.submitParameter)
        self.BatteryPackLayout.addWidget(self.submit)

        self.CellLayout.addStretch()
        self.CellLayout.setSpacing(5)

        self.BatteryPackLayout.addStretch()
        self.BatteryPackLayout.setSpacing(5)

        MainLayout.addLayout(self.CellLayout)
        MainLayout.addLayout(self.BatteryPackLayout)
        self.setLayout(MainLayout)

    def submitParameter(self):
        global T0
        global soc
        if not(self.inputCellName.text() == ''):
            file = open('MBM\Objects\SavedCells\Cells.csv', mode  = 'a', newline = '')
            wrighter = csv.writer(file)
            Cellrow = [self.inputCellName.text(),
                            float(self.inputMass.text()), 
                            float(self.inputResistance.text()), 
                            float(self.inputK.text()), 
                            float(self.inputAmpacity.text()), 
                            float(self.inputMaxVoltage.text()), 
                            float(self.inputMinVoltage.text()), 
                            float(self.inputNomVoltage.text()),
                            float(self.inputmCrate.text()),
                            float(self.inputcCrate.text())]
            wrighter.writerow(Cellrow)
            file.close()

        if not(self.inputConfName.text() == ''):
            file = open('MBM\Objects\SavedBatteryPacks\BatteryPacks.csv', mode  = 'a', newline = '')
            wrighter = csv.writer(file)
            Confrow = [self.inputConfName.text(),
                    float(self.inputSeries.text()),
                    float(self.inputParallel.text())]
            wrighter.writerow(Confrow)
            file.close()
        
        T0 = float(self.inputInitialTemperature.text())
        soc = float(self.inputInitialStateOfCharge.text())
        self.close()

    def SetUpBatteryPack(self):
        self.BatteryPackLayout.addWidget(QLabel('BatteryPack'))
        self.BatteryPackLayout.addWidget(QLabel(' '))

        self.BatteryPackLayout.addWidget(QLabel('BatteryPack Name'))
        self.inputConfName = QLineEdit()
        self.BatteryPackLayout.addWidget(self.inputConfName)

        self.BatteryPackLayout.addWidget(QLabel('Series Connections'))
        self.inputSeries = QLineEdit(str(batteryPack.Series))
        self.BatteryPackLayout.addWidget(self.inputSeries)

        self.BatteryPackLayout.addWidget(QLabel('Parallel Connections'))
        self.inputParallel = QLineEdit(str(batteryPack.Parallel))
        self.BatteryPackLayout.addWidget(self.inputParallel)

        self.BatteryPackLayout.addWidget(QLabel('Initial Temperature'))
        self.inputInitialTemperature = QLineEdit(str(T0))
        self.BatteryPackLayout.addWidget(self.inputInitialTemperature)

        self.BatteryPackLayout.addWidget(QLabel('Initial State of Charge'))
        self.inputInitialStateOfCharge = QLineEdit(str(soc))
        self.BatteryPackLayout.addWidget(self.inputInitialStateOfCharge)
        
        self.BatteryPackLayout.addWidget(QLabel('Continuous Test'))
        self.inputContControl = QPushButton(str(continuous))
        self.inputContControl.clicked.connect(self.ContControl)
        self.BatteryPackLayout.addWidget(self.inputContControl)

        self.BatteryPackLayout

    def ContControl(self):
        global continuous
        continuous = not(continuous)
        self.inputContControl.setText(str(continuous))

    def SetUpCell(self):
        self.CellLayout.addWidget(QLabel('Cell Specifics'))
        self.CellLayout.addWidget(QLabel(' '))

        self.CellLayout.addWidget(QLabel('Cell Name'))
        self.inputCellName = QLineEdit()
        self.CellLayout.addWidget(self.inputCellName)

        self.CellLayout.addWidget(QLabel('Mass'))
        self.inputMass = QLineEdit(str(cell.mass))
        self.CellLayout.addWidget(self.inputMass)

        self.CellLayout.addWidget(QLabel('Resistance'))
        self.inputResistance = QLineEdit(str(cell.resistance))
        self.CellLayout.addWidget(self.inputResistance)

        self.CellLayout.addWidget(QLabel('K'))
        self.inputK = QLineEdit(str(cell.K))
        self.CellLayout.addWidget(self.inputK)

        self.CellLayout.addWidget(QLabel('Ampacity'))
        self.inputAmpacity = QLineEdit(str(cell.ampacity))
        self.CellLayout.addWidget(self.inputAmpacity)

        self.CellLayout.addWidget(QLabel('Max Voltage'))
        self.inputMaxVoltage = QLineEdit(str(cell.maxVoltage))
        self.CellLayout.addWidget(self.inputMaxVoltage)

        self.CellLayout.addWidget(QLabel('Min Voltage'))
        self.inputMinVoltage = QLineEdit(str(cell.minVoltage))
        self.CellLayout.addWidget(self.inputMinVoltage)

        self.CellLayout.addWidget(QLabel('Nominal Voltage'))
        self.inputNomVoltage = QLineEdit(str(cell.nomVoltage))
        self.CellLayout.addWidget(self.inputNomVoltage)

        self.CellLayout.addWidget(QLabel('max C rate discharge'))
        self.inputmCrate= QLineEdit(str(cell.maxCrate))
        self.CellLayout.addWidget(self.inputmCrate)

        self.CellLayout.addWidget(QLabel('continuous C rate discharge'))
        self.inputcCrate= QLineEdit(str(cell.contCrate))
        self.CellLayout.addWidget(self.inputcCrate)

class GraphWindow(QWidget):
    def __init__(self, cellNames, confNames, cells, confs, filename):
        super().__init__()
        self.cellNames = cellNames
        self.confNames = confNames
        self.cells = cells
        self.confs = confs
        self.filename = filename
        self.expanded = False

        self.MainLayout = QHBoxLayout()
        self.ParamLayout = QVBoxLayout()
        self.SourceLayout = QVBoxLayout()

        self.SourceLayout.addWidget(QLabel('Select battery pack A'))
        self.layout1 = QHBoxLayout()
        self.SelectedCell1 = QComboBox()
        self.SelectedCell1.addItems(self.cellNames)
        self.layout1.addWidget(self.SelectedCell1)

        self.SelectedConfig1 = QComboBox()
        self.SelectedConfig1.addItems(self.confNames)
        self.layout1.addWidget(self.SelectedConfig1)
        
        self.SourceLayout.addLayout(self.layout1)

        self.SourceLayout.addWidget(QLabel('Select battery pack B'))

        self.layout2 = QHBoxLayout()
        self.SelectedCell2 = QComboBox()
        self.SelectedCell2.addItem('None')
        self.SelectedCell2.addItems(self.cellNames)
        self.layout2.addWidget(self.SelectedCell2)

        self.SelectedConfig2 = QComboBox()
        self.SelectedConfig2.addItem('None')
        self.SelectedConfig2.addItems(self.confNames)
        self.layout2.addWidget(self.SelectedConfig2)
        
        self.SourceLayout.addLayout(self.layout2)

        self.showDataInput = QPushButton('Show pack data?')
        self.showData = True
        self.showDataInput.setCheckable(True)
        self.showDataInput.setChecked(True)
        self.showDataInput.clicked.connect(self.toggledata)
        
        self.SourceLayout.addWidget(self.showDataInput)

        self.run = QPushButton('Run')
        self.run.clicked.connect(self.Run)
        self.SourceLayout.addWidget(self.run)

        self.SourceLayout.addStretch()
        self.SourceLayout.setSpacing(10)

        self.MainLayout.addLayout(self.SourceLayout)
        
        self.setLayout(self.MainLayout)

    def Run(self):
        self.data = {}
        title1 = self.SelectedCell1.currentText() + ' - ' + self.SelectedConfig1.currentText()
        cell1 = self.cells[self.cellNames.index(self.SelectedCell1.currentText())]
        batteryPack1 = BatteryPack(self.confs[self.confNames.index(self.SelectedConfig1.currentText())][0],
                                  self.confs[self.confNames.index(self.SelectedConfig1.currentText())][1],
                                  cell1)
        
        self.data[title1] = ThermalProfile(T0, batteryPack1, continuous, soc, self.filename, title1)
        if self.SelectedCell2.currentText() != 'None' and self.SelectedConfig2.currentText() != 'None':
            title2 = self.SelectedCell2.currentText() + ' - ' + self.SelectedConfig2.currentText()
            cell2 = self.cells[self.cellNames.index(self.SelectedCell2.currentText())]
            batteryPack2 = BatteryPack(self.confs[self.confNames.index(self.SelectedConfig2.currentText())][0],
                                      self.confs[self.confNames.index(self.SelectedConfig2.currentText())][1],
                                      cell2)
            self.data[title2] = ThermalProfile(T0, batteryPack2, continuous, soc, self.filename, title2)
        
        if not(self.expanded):
            self.SelectedFields = []
            for key in self.data[title1].keys():
                if (key != 'timeData') and (key != 'laps') and (key != 'Wh used') and (key != 'Efficency'):
                    CurrentField = QCheckBox(key)
                    CurrentField.name = key
                    CurrentField.stateChanged.connect(self.selected)
                    self.ParamLayout.addWidget(CurrentField)
                        
            self.Submit = QPushButton('Graph Selected Fields')
            self.Submit.clicked.connect(self.SubmitGraph)
            self.ParamLayout.addWidget(self.Submit)
            self.MainLayout.addLayout(self.ParamLayout)
            self.expanded = True

    def selected(self):
        cur = self.sender()
        if cur.isChecked():
            self.SelectedFields.append(cur.name)
        else:
            self.SelectedFields.remove(cur.name)

    def toggledata(self):
        self.showData = not(self.showData)

    def SubmitGraph(self):
        GraphTP(self.data, self.SelectedFields, self.showData)

class DischargeGraphWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.MainLayout = QVBoxLayout()
        
        self.CellAh = QPushButton('Cell Voltage(amp hours)')
        self.CellAh.clicked.connect(self.GraphCellAh)
        self.MainLayout.addWidget(self.CellAh)

        self.CellWh = QPushButton('Cell Voltage(watt hours)')
        self.CellWh.clicked.connect(self.GraphCellWh)
        self.MainLayout.addWidget(self.CellWh)

        self.BatteryPackWh = QPushButton('Pack Voltage(watt hours)')
        self.BatteryPackWh.clicked.connect(self.GraphPackWh)
        self.MainLayout.addWidget(self.BatteryPackWh)

        self.setLayout(self.MainLayout)

    def GraphCellAh(self):
        global data
        global cell

        cell = self.cells[self.cellNames.index(self.SelectedCell.currentText())]
        data = CellAhDischargeProfile(cell, T0)
        title = self.SelectedCell.currentText()
        GraphDP(data, 'amp hours', 'Cell', title)
    
    def GraphCellWh(self):
        global data
        global cell

        cell = self.cells[self.cellNames.index(self.SelectedCell.currentText())]
        data = CellWhDischargeProfile(cell, T0)
        title = self.SelectedCell.currentText()
        GraphDP(data, 'watt hours', 'Cell', title)

    def GraphPackWh(self):
        global data
        global cell
        global batteryPack

        
        cell = self.cells[self.cellNames.index(self.SelectedCell.currentText())]
        batteryPack = BatteryPack(self.confs[self.confNames.index(self.SelectedConfig.currentText())][0],
                                      self.confs[self.confNames.index(self.SelectedConfig.currentText())][1],
                                      cell)
        data = PackWhDischargeProfile(batteryPack, T0)
        title = self.SelectedCell.currentText() + ' - ' + self.SelectedConfig.currentText()
        GraphDP(data, 'watt hours', 'Pack', title)

class PkwhGraphWindow(QWidget):
    def __init__(self, cellNames, confNames, cells, confs):
        super().__init__()
        self.MainLayout = QVBoxLayout()
        self.cellNames = cellNames
        self.confNames = confNames
        self.cells = cells
        self.confs = confs
        self.data = {}

        self.MainLayout.addWidget(QLabel('Select battery pack A'))
        self.layout1 = QHBoxLayout()
        self.SelectedCell1 = QComboBox()
        self.SelectedCell1.addItems(self.cellNames)
        self.layout1.addWidget(self.SelectedCell1)

        
        self.SelectedConfig1 = QComboBox()
        self.SelectedConfig1.addItems(self.confNames)
        self.layout1.addWidget(self.SelectedConfig1)
        
        self.MainLayout.addLayout(self.layout1)

        self.MainLayout.addWidget(QLabel('Select battery pack B'))

        self.layout2 = QHBoxLayout()
        self.SelectedCell2 = QComboBox()
        self.SelectedCell2.addItem('None')
        self.SelectedCell2.addItems(self.cellNames)
        self.layout2.addWidget(self.SelectedCell2)

        self.SelectedConfig2 = QComboBox()
        self.SelectedConfig2.addItem('None')
        self.SelectedConfig2.addItems(self.confNames)
        self.layout2.addWidget(self.SelectedConfig2)
        
        self.MainLayout.addLayout(self.layout2)

        self.showDataInput = QPushButton('Show pack data?')
        self.showData = True
        self.showDataInput.setCheckable(True)
        self.showDataInput.setChecked(True)
        self.showDataInput.clicked.connect(self.toggledata)
        
        self.MainLayout.addWidget(self.showDataInput)

        self.run = QPushButton('Run')
        self.run.clicked.connect(self.Run)
        self.MainLayout.addWidget(self.run)

        self.setLayout(self.MainLayout)

    def toggledata(self):
        self.showData = not(self.showData)
    
    def Run(self):
        self.data = {}
        title1 = self.SelectedCell1.currentText() + ' - ' + self.SelectedConfig1.currentText()
        cell1 = self.cells[self.cellNames.index(self.SelectedCell1.currentText())]
        batteryPack1 = BatteryPack(self.confs[self.confNames.index(self.SelectedConfig1.currentText())][0],
                                  self.confs[self.confNames.index(self.SelectedConfig1.currentText())][1],
                                  cell1)
        self.data[title1] = MaxPkw(batteryPack1)
        if self.SelectedCell2.currentText() != 'None' and self.SelectedConfig2.currentText() != 'None':
            title2 = self.SelectedCell2.currentText() + ' - ' + self.SelectedConfig2.currentText()
            cell2 = self.cells[self.cellNames.index(self.SelectedCell2.currentText())]
            batteryPack2 = BatteryPack(self.confs[self.confNames.index(self.SelectedConfig2.currentText())][0],
                                      self.confs[self.confNames.index(self.SelectedConfig2.currentText())][1],
                                      cell2)
            self.data[title2] = MaxPkw(batteryPack2)
        GraphPkwh(self.data, self.showData)

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.cellNames = []
        self.cells = []

        self.confNames = []
        self.confs = []

        self.MainLayout = QVBoxLayout()

        self.TopLayout = QHBoxLayout()

        self.ActionLayout = QHBoxLayout()

        self.setNewCellConfig = QPushButton('Set up a new cell / BatteryPack')
        self.setNewCellConfig.clicked.connect(self.SetCellConfig)
        self.TopLayout.addWidget(self.setNewCellConfig)

        AvailibleFiles = self.FindDriverProfiles()
        self.InputFile = QComboBox()
        self.InputFile.addItems(AvailibleFiles)
        self.TopLayout.addWidget(self.InputFile)

        self.FindCells()
        self.SelectedCell = QComboBox()
        self.SelectedCell.addItems(self.cellNames)
        self.TopLayout.addWidget(self.SelectedCell)

        self.FindBatteryPacks()
        self.SelectedConfig = QComboBox()
        self.SelectedConfig.addItems(self.confNames)
        self.TopLayout.addWidget(self.SelectedConfig)
        
        self.RefreshButton = QPushButton()
        self.RefreshButton.clicked.connect(self.Refresh)
        self.RefreshButton.setIcon(QIcon('Objects/Images/Refresh-Logo.png'))
        self.TopLayout.addWidget(self.RefreshButton)

        self.ThermalProfile = QPushButton('Run Drive Profile')
        self.ThermalProfile.clicked.connect(self.RunThermalProfile)
        self.ActionLayout.addWidget(self.ThermalProfile)

        self.DischargeProfile = QPushButton('Run Discharge Profile')
        self.DischargeProfile.clicked.connect(self.RunDischargeProfile)
        self.ActionLayout.addWidget(self.DischargeProfile)

        self.Vsoc = QPushButton('Voltage vs SOC')
        self.Vsoc.clicked.connect(self.RunVsoc)
        self.ActionLayout.addWidget(self.Vsoc)

        self.Pkwh = QPushButton('Max Power vs wh Consumed')
        self.Pkwh.clicked.connect(self.RunPkwh)
        self.ActionLayout.addWidget(self.Pkwh)

        self.MainLayout.addLayout(self.TopLayout)
        self.MainLayout.addLayout(self.ActionLayout)

        self.setLayout(self.MainLayout)

    def Refresh(self):
    
        for i in range(len(self.cellNames)):
            self.SelectedCell.removeItem(0)
        
        for i in range(len(self.confNames)):
            self.SelectedConfig.removeItem(0)
        
        self.FindCells()
        self.FindBatteryPacks()

        self.PkwhData = {}

        self.SelectedCell.addItems(self.cellNames)
        self.SelectedConfig.addItems(self.confNames)

    def SetCellConfig(self):
        global cell
        global batteryPack
        cell = self.cells[self.cellNames.index(self.SelectedCell.currentText())]
        batteryPack = BatteryPack(self.confs[self.confNames.index(self.SelectedConfig.currentText())][0],
                                      self.confs[self.confNames.index(self.SelectedConfig.currentText())][1],
                                      cell)

        self.TempWindow = Setup()
        self.TempWindow.show()

    def FindDriverProfiles(self):
        files = []
        for entry in scandir('DriverProfiles'):
            if entry.is_file():
                name = entry.name
                t = name.split('.')
                type = t[1]
                if type == 'csv':
                    files.append(name)
        
        return files
    
    def FindCells(self):
        
        file = open('MBM\Objects\SavedCells\Cells.csv', mode = 'r')
        reader = csv.DictReader(file)
        self.cellNames = []
        self.cells = []

        for row in reader:
            self.cellNames.append(str(row['name']))
            self.cells.append(Cell(float(row['mass']),
                                    float(row['resistance']), 
                                    float(row['k']), 
                                    float(row['ampacity']), 
                                    float(row['maxVoltage']), 
                                    float(row['minVoltage']), 
                                    float(row['nomVoltage']), 
                                    float(row['maxCrate']),
                                    float(row['contCrate'])))

    def FindBatteryPacks(self):
        
        file = open('MBM\Objects\SavedBatteryPacks\BatteryPacks.csv', mode = 'r')
        reader = csv.DictReader(file)
        self.confNames = []
        self.confs = []
        
        for row in reader:
            
            self.confNames.append(str(row['name']))
            self.confs.append((float(row['series']), float(row['parallel'])))

    def RunThermalProfile(self):
        self.DriveProfileWindow = GraphWindow(self.cellNames, self.confNames, self.cells, self.confs, self.InputFile.currentText())
        self.DriveProfileWindow.setWindowTitle('Drive Profile')
        self.DriveProfileWindow.show()
    
    def RunDischargeProfile(self):
        self.DischargeGraphWindow = DischargeGraphWindow()

        self.DischargeGraphWindow.cells = self.cells
        self.DischargeGraphWindow.cellNames = self.cellNames
        self.DischargeGraphWindow.SelectedCell = self.SelectedCell
        self.DischargeGraphWindow.confs = self.confs
        self.DischargeGraphWindow.confNames = self.confNames
        self.DischargeGraphWindow.SelectedConfig = self.SelectedConfig

        self.DischargeGraphWindow.setWindowTitle('Discharge Profile')
        self.DischargeGraphWindow.show()

    def RunVsoc(self):
        cell = self.cells[self.cellNames.index(self.SelectedCell.currentText())]
        
        batteryPack = BatteryPack(self.confs[self.confNames.index(self.SelectedConfig.currentText())][0],
                                      self.confs[self.confNames.index(self.SelectedConfig.currentText())][1],
                                      cell)
        data = Vsoc(batteryPack)
        title = self.SelectedCell.currentText() + ' - ' + self.SelectedConfig.currentText()
        
        GraphVsoc(data, title)

    def RunPkwh(self):
        self.PkwhWindow = PkwhGraphWindow(self.cellNames, self.confNames, self.cells, self.confs)
        self.PkwhWindow.setWindowTitle('Max Power vs SOC')
        self.PkwhWindow.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()