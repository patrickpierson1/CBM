from Objects.cell import Cell
from Objects.BatteryPack import BatteryPack
import tkinter as tk
import math
import csv
from tkinter import Canvas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

def ThermalProfileLive(T0, batteryPack, stateOfCharge, fileName, speed=10):
    def create_dial(canvas, x, y, radius, label):
        """Creates a circular dial with a pointer."""
        canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius, outline="black", width=2
        )
        canvas.create_text(x, y + radius + 20, text=label, font=("Arial", 12))
        return canvas.create_line(x, y, x, y - radius, fill="red", width=3)

    def update_dial(canvas, line, x, y, radius, value, min_val, max_val):
        """Updates the dial pointer based on the value."""
        angle = (value - min_val) / (max_val - min_val) * 180 - 90
        rad_angle = math.radians(angle)
        x_end = x + radius * math.cos(rad_angle)
        y_end = y + radius * math.sin(rad_angle)
        canvas.coords(line, x, y, x_end, y_end)

    def run_simulation():
        """Simulates the thermal profile and updates the dials and graphs."""
        nonlocal t, soc, wh, T, reader, end

        for _ in range(speed):  # Process `speed` rows per second
            try:
                row = next(reader)
            except StopIteration:
                end = True
                break

            # Compute simulation values
            P = float(row['kW']) * 1000
            R = batteryPack.CurrentResistance(wh)
            Voc = batteryPack.CurrentVoltage(wh)
            I = ((-Voc) + math.sqrt(((-Voc) ** 2) - (4 * -R * -(P)))) / (2 * -R)
            Vdrop = I * R
            V = Voc - Vdrop
            soc = 100 * (1 - (wh / (batteryPack.Capacity)))
            wh += P / 3600
            loss = (I ** 2) * R
            T += loss / (batteryPack.cellMass * batteryPack.cellK)

            # Real temperature and voltage (if present in the data)
            real_temp1 = None
            real_temp2 = None
            real_voltage = None
            if 't1' in row:
                real_temp1 = (float(row['t1']) - 32) * 5 / 9  # Convert from Fahrenheit to Celsius
            if 't2' in row:
                real_temp2 = (float(row['t2']) - 32) * 5 / 9  # Convert from Fahrenheit to Celsius
            if 'V' in row:
                real_voltage = float(row['V'])

            # Update dials
            update_dial(canvas, voltage_dial, 100, 100, 50, V, 0, batteryPack.maxVoltage)
            update_dial(canvas, current_dial, 300, 100, 50, I, 0, batteryPack.maxDischarge)
            update_dial(canvas, power_dial, 100, 300, 50, P / 1000, 0, 100)  # Max Power 100kW
            update_dial(canvas, temp_dial, 300, 300, 50, T, T0, 60)  # Max Temp 60°C

            # Add data to graphs
            time_data.append(t)
            voltage_data.append(V)
            Voc_data.append(Voc)
            real_voltage_data.append(real_voltage if real_voltage is not None else float('nan'))
            current_data.append(I)
            power_data.append(P / 1000)
            temp_data.append(T)
            real_temp_data1.append(real_temp1 if real_temp1 is not None else float('nan'))
            real_temp_data2.append(real_temp2 if real_temp2 is not None else float('nan'))

            # Increment time
            t += 1

            # Check for termination conditions
            if soc <= 0 or V <= batteryPack.minVoltage or T >= 60 or I >= batteryPack.maxDischarge:
                print("Fault detected! Ending simulation.")
                return

        # Schedule the next update
        if not end:
            root.after(100, run_simulation)

    def update_graph(frame):
        """Updates the live graph with the latest data."""
        ax1.clear()
        ax2.clear()

        # Voltage and Voc
        ax1.plot(time_data, voltage_data, label="Voltage (V)", color="blue")
        ax1.plot(time_data, Voc_data, label="Voc (V)", color="green")
        ax1.plot(time_data, real_voltage_data, label="Real Voltage (V)", color="orange", linestyle="--")
        ax1.set_ylabel("Voltage (V)")
        ax1.legend(loc="upper left")

        # Current, Power, Temperature, and Real Temperature
        ax2.plot(time_data, current_data, label="Current (A)", color="orange")
        ax2.plot(time_data, power_data, label="Power (kW)", color="purple")
        ax2.plot(time_data, temp_data, label="Temperature (°C)", color="red")
        ax2.plot(time_data, real_temp_data1, label="Real Temp1 (°C)", color="magenta", linestyle="--")
        ax2.plot(time_data, real_temp_data2, label="Real Temp2 (°C)", color="blue", linestyle="--")
        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("Current / Power / Temperature")
        ax2.legend(loc="upper left")

    # Initialize variables
    t = 0
    soc = stateOfCharge
    wh = 0.01 * (100 - soc) * batteryPack.Capacity
    T = T0
    end = False

    # Deques for live plotting
    time_data = deque(maxlen=100)
    voltage_data = deque(maxlen=100)
    Voc_data = deque(maxlen=100)
    real_voltage_data = deque(maxlen=100)
    current_data = deque(maxlen=100)
    power_data = deque(maxlen=100)
    temp_data = deque(maxlen=100)
    real_temp_data1 = deque(maxlen=100)
    real_temp_data2 = deque(maxlen=100)

    # Read file
    file = open('DriverProfiles/' + fileName, mode='r')
    reader = iter(csv.DictReader(file))

    # Create GUI
    root = tk.Tk()
    root.title("Battery Thermal Simulation")
    canvas = tk.Canvas(root, width=400, height=400, bg="white")
    canvas.pack(side=tk.LEFT)

    # Create dials
    voltage_dial = create_dial(canvas, 100, 100, 50, "Voltage (V)")
    current_dial = create_dial(canvas, 300, 100, 50, "Current (A)")
    power_dial = create_dial(canvas, 100, 300, 50, "Power (kW)")
    temp_dial = create_dial(canvas, 300, 300, 50, "Temperature (°C)")

    # Create matplotlib figure for live graph
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8))
    fig.subplots_adjust(hspace=0.5)
    graph_canvas = FigureCanvasTkAgg(fig, root)
    graph_canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Start simulation and graph animation
    ani = animation.FuncAnimation(fig, update_graph, interval=100)
    root.after(100, run_simulation)
    root.mainloop()




cell = Cell(0.07,0.013,700,5.0,4.2,2.5,3.6,9)
batteryPack = BatteryPack(110, 3, cell)
ThermalProfileLive(20, batteryPack, 52, 'halfendurance.csv', 10)