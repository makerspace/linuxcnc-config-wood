from argparse import ArgumentParser
parser = ArgumentParser(description="Generate G-code for the Stockholm Makerspace CNC router")
parser.add_argument("--mode", choices=["vacuum", "surface"], required=True, help="Either vacuum the wasteboard, or surface the wasteboard")
args = parser.parse_args()

mode = args.mode

xmax = 850
ymax = 885
stepover = 42

z_probe_x = 831
z_probe_y = 15
z_probe_horizontal_margin = 130

print("%")

if mode == "vacuum":
    spindle_rpm = 0
    avoid_probe = True
    touch_off = True
    perpendicular_pass = False
    z_feed = 0
    speed = 7000
    z_speed = 1000
    print("; Vacuums the wasteboard")
    print("; Before starting:")
    print("; 1. Unload any tool in the spindle")
    print("; 2. Attach the dust shoe")
    print("; 3. Lower the spindle to the lowest position")
    print("; 4. Touch off the z-axis")
    print("; 5. Ensure there's nothing on the table except for the z-probe")
elif mode == "surface":
    spindle_rpm = 10000
    avoid_probe = False
    touch_off = False
    perpendicular_pass = True
    z_feed = 0
    speed = 3000
    z_speed = 300
    print("; Surfaces the wasteboard")
    print("; Before starting:")
    print("; 1. Unmount the z-probe")
    print("; 2. Attach the dust shoe")
    print("; 3. Load a 50mm cutter")
    print("; 4. Touch off z=0 to the height you want to flatten to, typically 0.1-0.5mm below the current surface")
else:
    raise ValueError("Invalid mode")

z_retract = z_feed + 10

if mode == "vacuum":
    print("(MSG, Ensure no tool is loaded)")
    print("(MSG, Ensure nothing is on the table)")
    print("M06 T1")

print("N45 G64 P5.0 Q5.0") # Set blending tolerance
print("G21") # Set units to mm
print("G90") # Set to absolute positioning
print("G53 G0 x0 y0") # Move to start position

# Start up sindle
print(f"M03 s{spindle_rpm}")
# Wait for spindle to reach speed
print("G4 P5")

print(f"G1 z{z_feed} F{z_speed}")

x = 0
for i in range(0, ymax+stepover, stepover):
    i = min(i, ymax)
    mx = xmax
    if i > z_probe_y - z_probe_horizontal_margin and i < z_probe_y + z_probe_horizontal_margin:
        mx = z_probe_x - z_probe_horizontal_margin

    print(f"G53 G1 y{i} F{speed}")
    if x == 0:
        print(f"G53 G1 x{mx} F{speed}")
        x = 1
    else:
        print(f"G53 G1 x0 F{speed}")
        x = 0


if perpendicular_pass:
    # Perpendicular pass
    print(f"G1 z{z_retract} F{z_speed}")
    print(f"G53 G0 x0 y0")
    print(f"G1 z{z_feed} F{z_speed}")
    y = 0
    for i in range(0, xmax+stepover, stepover):
        i = min(i, xmax)
        print(f"G53 G1 x{i} F{speed}")
        if y == 0:
            print(f"G53 G1 x{i} y{ymax} F{speed}")
            y = 1
        else:
            print(f"G53 G1 x{i} y0 F{speed}")
            y = 0

# Stop spindle
print(f"G1 z{z_retract} F{z_speed}")
print("M30") # Program end
print("%")
