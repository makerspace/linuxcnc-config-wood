speed = 3000
xmax = 850
ymax = 885
stepover = 42
print("%")
print("N45 G64 P5.0 Q5.0") # Set blending tolerance
print("G21") # Set units to mm
print("G90") # Set to absolute positioning
print("G0 x0 y0 F4000") # Move to start position

# Start up sindle
print("M03 s10000")
# Wait for spindle to reach speed
print("G4 P5")

print("G1 z0 F300")

x = 0
for i in range(0, ymax+stepover, stepover):
    i = min(i, ymax)
    print(f"G1 y{i} F{speed}")
    if x == 0:
        print(f"G1 x{xmax} F{speed}")
        x = 1
    else:
        print(f"G1 x0 F{speed}")
        x = 0


# Perpendicular pass
print("G1 z10")
print("G0 x0 y0 F4000")
print("G1 z0 F300")
y = 0
for i in range(0, xmax+stepover, stepover):
    i = min(i, xmax)
    print(f"G1 x{i} F{speed}")
    if y == 0:
        print(f"G1 x{i} y{ymax} F{speed}")
        y = 1
    else:
        print(f"G1 x{i} y0 F{speed}")
        y = 0

# Stop spindle
print("G1 z10")
print("M30")
print("%")
