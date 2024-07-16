# AutoHAP
Automates input for the software Carrier HAP4.2 (WIP)

!!!CURRENTLY WORK IN PROGRESS BUGS EXIST USE AT OWN RISK!!!

Current list of functions

1. General
    - Inputs room name
    - Calculates and inputs floor area
    - Calculates and inputs room height
2. Internals
    - Inputs electrical equipment wattage (WIP)
    - Inputs people occupancy (WIP)
3. Walls, Windows, Doors
    - Detects and inputs direction of exterior walls (Assumes up as North)
    - Calculates and inputs wall area
    - Calculates and inputs window area
    - Calculates and inputs door area
4. Roofs, Skylights
    - Inputs exposure direction (WIP)
    - Inputs roof area (WIP)
    - Inputs roof slope (WIP)
    - Inputs skylight area (WIP)
5. Infiltration
    - Inputs design cooling (WIP)
    - Inputs deisgn heating (WIP)
    - Inputs energy analayis (WIP)
6. Floors (WIP)
7. Paritions (WIP)

This is a WIP

HOW TO USE
For standard Windows 10/11 installation only (Tested on Windows 10)

Prerequisite
1. Have a copy of HAP 4.20 Carrier Software installed
2. Install [AutoIt](https://www.autoitscript.com/site/autoit/downloads/) automation software
3. Have a copy of AutoCAD LT 2024 or higher or AutoCAD 2020 or higher (currently tested with AutoCAD LT 2024 and AutoCAD 2020)
4. Install [python 3.8](https://www.python.org/downloads/) or higher (currently tested on python 3.11)

Installation
1. Download repo
2. Using the "drawing_template.dwg" file draw floor plan using the template as a guide
NOTES:
   - Layer names must not be changed
   - All polylines must be closed
   - Currently no tolerances with coordinates (WIP)
4. Use APPLOAD to load the autohap.lsp file
5. Use AUTOHAP command to activate script and select all objects
6. Save output (do not change name (WIP)) to the same directory as the scripts
7. AutoHAP will now begin to auto fill the data with the selected information (Mouse cursor will freeze please do not try to move during automation use CTRL ALT DEL to escape if needed)
