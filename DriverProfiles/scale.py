

filename = "DriverProfiles/EnduranceLap.csv"
destination = "DriverProfiles/Endurance_scaled.csv"

scale = 3

source = open(filename, "r")
destination = open(destination, "w")
keys = source.readline()
destination.write(keys)
for line in source:
    if line == keys:
        continue
    line = line.split(",")
    for i in range(len(line)):
        try:
            line[i] = str(float(line[i]) * scale)
        except:
            pass
    destination.write(",".join(line) + "\n")