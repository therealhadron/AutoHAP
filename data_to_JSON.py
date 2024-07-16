import re
import json
import PolygonHelper
import os
import math

save_path = "./AutoHAP_data.json" # This is for this python script
final_data = {}
final_data["Spaces"] = []
save_path_autoit_json = "./AutoIt_data.json" # This is for autoit script

# Pre processes the autocad lisp output into a JSON file to be processed again into a final JSON file that will be read by autoit
# Saves the pre processed JSON file
def create_json(file_path):
    data = {}
    try:
        with open(file_path, 'r') as file:
            content = file.readlines()
            index = 0
            add_object = False
            text_list = []
            system_window_line_list = []
            data["Configuration"] = {}
            data["Room_Outline"] = []
            data["Building_Outline"] = []
            data["Window"] = []
            data["Door"] = []
            data["System_Window"] = []

            while index < len(content):
                line = content[index].replace('\n','')
                if line == "{": #Checks for start of object
                    add_object = True
                if add_object:
                    object = re.search(r"<([^>]+)>", line).group(1) if re.search(r"<([^>]+)>", line) else None
                    # Parsing layer name items
                    if object == "Layer_name":
                        layer_name = re.search(r'>\s*(.*)', content[index]).group(1)

                        if layer_name in ["Room_Outline", "Window", "Door", "System_Window", "Building_Outline"]:
                            coord_list, index = get_object_coordinates(content, index)
                            data[layer_name].append({"Coordinates":coord_list})
                        elif layer_name == "Configuration":
                            coord_list, index = get_object_coordinates(content,index)
                            data["Configuration"]["Coordinates"] = coord_list
                        elif layer_name == "System_Window_Line":
                            start_point = eval(re.sub(r'<.*?>', '', content[index+1]).replace('\n',''))
                            end_point = eval(re.sub(r'<.*?>', '', content[index+2]).replace('\n',''))
                            system_window_line_list.append({"Coordinates":[start_point, end_point]})
                        elif layer_name in ["Text", "Configuration_text"]:
                            text = re.search(r'>\s*(.*)', content[index+1]).group(1)
                            text = text.split('\P',-1)
                            text_contents = {}
                            for line in text:
                                text_key = (line.split(':',-1)[0]).strip()
                                text_value = (line.split(':',-1)[1]).strip()
                                text_contents[text_key] = text_value
                            if layer_name == "Configuration_text": data["Configuration"]["Text"] = text_contents
                            elif layer_name == "Text": text_list.append({"Text":text_contents, "Coordinates":eval(content[index+3])})
                        add_object = False
                index = index + 1
            data["Texts"] = text_list
            data["System_Window_Lines"] = system_window_line_list
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except IOError:
        print(f"Error reading file '{file_path}'.")
    with open(save_path, 'w', encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)

def get_object_coordinates(content, index):
    coord_list = []
    i = index + 2 #Skips to coordinates
    while content[i].replace('\n','') != "}":
        coord_list.append(eval(content[i]))
        i = i + 1 #loops thru coordinates
    return coord_list, i

def process_json_data():
    global final_data

    with open(save_path, 'r') as json_file:
        json_data = json.load(json_file)
    room_data = {}
    rooms = json_data["Room_Outline"]
    texts = json_data["Texts"]
    system_windows = json_data["System_Window"]
    system_window_lines = json_data["System_Window_Lines"]
    windows = json_data["Window"]
    doors = json_data["Door"]
    building_outlines = json_data["Building_Outline"]

    for building_outline in building_outlines: # Loops thru every building outline (multiple floors)
        building_outline = building_outline["Coordinates"]
        for room in rooms: # Loops thru every room
            room_vertex = room["Coordinates"]
            # Check if room is within current building outline
            if not PolygonHelper.is_coordinate_in_polygon(building_outline,PolygonHelper.get_polygon_center(room_vertex)):
                continue

            text_name, text_ceiling_height, spaces_floor_area = get_room_text(texts, room_vertex)

            # reset lists
            exterior_walls = []
            exterior_walls_area = []
            exterior_wall_window_area = []
            exterior_wall_door_area = []
            roofs = []
            roofs_area = []

            for i, room_coordinate in enumerate(room_vertex): # Loops thru every vertex coordinate in current room aka check each wall
                if i < len(room_vertex) - 1:
                    room_coordinate_1 = room_vertex[i]
                    room_coordinate_2 = room_vertex[i + 1]
                    
                    window_total_area, door_total_area = get_wall_window_area(room_coordinate_1, room_coordinate_2, system_window_lines, system_windows, windows, doors)
                    room_wall_length = PolygonHelper.calculate_side_length(room_coordinate_1, room_coordinate_2)

                    for j, building_coordinate in enumerate(building_outline): # Loops thru every vertex coordinate in building outline
                        if j < len(building_outline) - 1:
                            # room wall is shorter than building outline
                            is_room_wall_in_building_outline = PolygonHelper.is_point_on_line(room_coordinate_1, room_coordinate_2, building_outline[j]) and \
                                                                PolygonHelper.is_point_on_line(room_coordinate_1, room_coordinate_2, building_outline[j + 1])
                            # room wall is longer than building outline
                            is_building_outline_in_room_wall = PolygonHelper.is_point_on_line(building_outline[j], building_outline[j + 1], room_coordinate_1) and \
                                                                PolygonHelper.is_point_on_line(building_outline[j], building_outline[j + 1], room_coordinate_2)
                            if is_room_wall_in_building_outline or is_building_outline_in_room_wall:
                                exterior_walls.append(PolygonHelper.wall_direction(room_vertex, room_coordinate_1, room_coordinate_2)) # Exterior wall direction
                                exterior_wall_window_area.append(window_total_area)
                                exterior_wall_door_area.append(door_total_area)
                                exterior_walls_area.append(room_wall_length*float(text_ceiling_height)*12/144) # Exterior wall area

            room_data["General"] = insert_spaces_general(text_name, spaces_floor_area, text_ceiling_height)
            room_data["Internals"] = insert_spaces_internals()
            room_data["Walls_Windows_Doors"] = insert_walls_windows_doors(exterior_walls, exterior_walls_area, exterior_wall_window_area, exterior_wall_door_area)
            room_data["Roofs_Skylights"] = insert_roofs_skylights(roofs, roofs_area)
            room_data["Infiltration"] = insert_infiltration()
            room_data["Floors"] = insert_floors()
            room_data["Partitions"] = insert_spaces_partitions()

            final_data["Spaces"].append(room_data)
            room_data = {}

# Gets room text data
def get_room_text(texts, room_vertex):
    for text in texts:
        if PolygonHelper.is_coordinate_in_polygon(room_vertex, text["Coordinates"]):
            text_name = text["Text"]["name"] # Name of room
            text_ceiling_height = text["Text"]["height"] # Height of room
            spaces_floor_area = PolygonHelper.calculate_enclosed_area(room_vertex) # Area of room
            return text_name, text_ceiling_height, spaces_floor_area
    return None

def get_wall_window_area(room_coordinate_1, room_coordinate_2, system_window_lines, system_windows, windows, doors):
    window_total_area = 0
    door_total_area = 0
    for system_window_line in system_window_lines: # Loops all system lines to find which room it assoicates with
        system_window_line_coordinate_1 = system_window_line["Coordinates"][0]
        system_window_line_coordinate_2 = system_window_line["Coordinates"][1]
        system_window_line_1 = PolygonHelper.is_point_on_line(room_coordinate_1, room_coordinate_2, system_window_line_coordinate_1)
        system_window_line_2 = PolygonHelper.is_point_on_line(room_coordinate_1, room_coordinate_2, system_window_line_coordinate_2)
        if system_window_line_1 or system_window_line_2:
            for system_window in system_windows: # Loops all system windows to determine which one assoicates with the current system line
                system_window_coordinates = system_window["Coordinates"]
                if PolygonHelper.is_point_on_polygon(system_window_coordinates, system_window_line_coordinate_1) or \
                PolygonHelper.is_point_on_polygon(system_window_coordinates, system_window_line_coordinate_2):
                    for window in windows: # Loops all windows to determine which windows are within the current system window
                        if PolygonHelper.is_coordinate_in_polygon(system_window_coordinates, window["Coordinates"][0]):
                            window_total_area = window_total_area + math.ceil(PolygonHelper.calculate_enclosed_area(window["Coordinates"])/144)
                    for door in doors:
                        if PolygonHelper.is_coordinate_in_polygon(system_window_coordinates, door["Coordinates"][0]):
                            door_total_area = door_total_area + math.ceil(PolygonHelper.calculate_enclosed_area(door["Coordinates"])/144)
                    return window_total_area, door_total_area
    return 0, 0

def insert_spaces_general(general_name, general_floor_area, general_avg_ceiling_height, 
                          general_building_weight=70, general_oa_requirement_1 = 0, 
                          general_oa_units_1 = "CFM/Person", general_oa_requirement_2 = 0, 
                          general_oa_units_2 = "CFM/Person"):
    general_dict = {}
    general_dict["Name"] = general_name
    general_dict["Floor_Area"] = round((general_floor_area/144),1)
    general_dict["Avg_Ceiling_Height"] = float(general_avg_ceiling_height)
    general_dict["Building Weight"] = general_building_weight
    general_dict["OA Req 1"] = general_oa_requirement_1
    general_dict["OA Req 1 Units"] = general_oa_units_1
    general_dict["OA Req 2"] = general_oa_requirement_2
    general_dict["OA Req 2 Units"] = general_oa_units_2
    return general_dict

def insert_spaces_internals(internal_electric_equipment_wattage = 0,
                            internal_electric_equipment_unit = "W/ft²",
                            internal_electric_equipment_schedule = "Sample Schedule",
                            internal_people_occupancy = 0,
                            internal_people_occupancy_unit = "People",
                            internal_people_activity_level = "Office_Work",
                            internal_people_schedule = "Sample Schedule"):
    internals_dict = {}
    internals_dict["Electrical_Equipment"] = {}
    internals_dict["People"] = {}
    internals_dict["Electrical_Equipment"]["Wattage"] = internal_electric_equipment_wattage
    internals_dict["Electrical_Equipment"]["Wattage_Units"] = internal_electric_equipment_unit
    internals_dict["Electrical_Equipment"]["Schedule"] = internal_electric_equipment_schedule
    internals_dict["People"]["Occupancy"] = internal_people_occupancy
    internals_dict["People"]["Occupancy_Unit"] = internal_people_occupancy_unit
    internals_dict["People"]["Activity_Level"] = internal_people_activity_level
    internals_dict["People"]["Schedule"] = internal_people_schedule
    return internals_dict

def insert_walls_windows_doors(wall_exposure = None, 
                               wall_area = None,
                               wall_window = None,
                               wall_door = None,
                               wall_construction = None,
                               window_construction = None,
                               door_construction = None
                               ):
    walls_windows_doors_dict = []

    if wall_exposure is not None:
        for i in range(len(wall_exposure)):
            walls_windows_doors_dict.append({"Exposure":wall_exposure[i],
                                            "Wall_Area": wall_area[i],
                                            "Window": wall_window[i],
                                            "Door": wall_door[i],
                                            "Wall_Assembly": "Default Wall Assembly",
                                            "Window_Assembly": "Sample Window Assembly",
                                            "Door_Assembly": "Sample Door Assembly"
                                            })
    for x in range(8 - len(wall_exposure)):
        walls_windows_doors_dict.append({"Exposure":"not used",
                                            "Wall_Area": 0,
                                            "Window":0,
                                            "Door": 0,
                                            "Wall_Assembly": "(none)",
                                            "Window_Assembly": "(none)",
                                            "Door_Assembly": "(none)"
                                            })
    return walls_windows_doors_dict

def insert_roofs_skylights(roof_exposure = None,
                           roof_area = None,
                           roof_slope = None,
                           skylight = None,
                           roof_assembly = None,
                           skylight_assembly = None):
    roofs_skylights_dict = []

    if roof_exposure is not None:
        for i in range(len(roof_exposure)):
            roofs_skylights_dict.append({"Exposure": roof_exposure[i],
                                         "Roof_Area": roof_area[i],
                                         "Roof_Slope": roof_slope,
                                         "Skylight": skylight,
                                         "roof_assembly": roof_assembly,
                                         "skylight_assembly": skylight_assembly
                                        })

    for x in range(4 - len(roof_exposure)):
        roofs_skylights_dict.append({"Exposure": "not used",
                                    "Roof_Area": 0,
                                    "Roof_Slope": 0,
                                    "Skylight": "(none)",
                                    "roof_assembly": "(none)",
                                    "skylight_assembly": "(none)"
                                    })
    return roofs_skylights_dict

# Infiltration occurs = true: Only When Fan Off
# Infiltration occurs = false: All hours
def insert_infiltration(design_cooling_CFM = 0,
                        design_heating_CFM = 0,
                        energy_analysis_CFM = 0,
                        infiltration_occurs = True):
    infiltration_dict = []
    infiltration_dict.append({"Design_Cooling": design_cooling_CFM,
                              "Design_Heating": design_heating_CFM,
                              "Energy_Analysis": energy_analysis_CFM,
                              "infiltration_occurs": infiltration_occurs
                            })
    return infiltration_dict

def insert_floors(floor_type = None):
    floors_dict = []
    return floors_dict

def insert_spaces_partitions(partition_1_ceiling_wall="Ceiling",
                             partition_1_area=0,
                             partition_1_uvalue=0.5,
                             partition_1_unconditioned_space_max_temp=75.0,
                             partition_1_ambient_at_space_max_temp=95.0,
                             partition_1_unconditioned_space_min_temp=75.0,
                             partition_1_ambient_at_space_min_temp=55.0,
                             partition_2_ceiling_wall="Ceiling",
                             partition_2_area=0,
                             partition_2_uvalue=0.5,
                             partition_2_unconditioned_space_max_temp=75.0,
                             partition_2_ambient_at_space_max_temp=95.0,
                             partition_2_unconditioned_space_min_temp=75.0,
                             partition_2_ambient_at_space_min_temp=55.0):
    partitions_dict = {}
    partitions_dict["Partition_1"] = {}
    partitions_dict["Partition_2"] = {}
    partitions_dict["Partition_1"]["Ceiling_Wall"] = partition_1_ceiling_wall
    partitions_dict["Partition_1"]["Area"] = partition_1_area
    partitions_dict["Partition_1"]["Uvalue"] = partition_1_uvalue
    partitions_dict["Partition_1"]["Unconditioned_Space_Max_Temp"] = partition_1_unconditioned_space_max_temp
    partitions_dict["Partition_1"]["Ambient_At_Space_Max_Temp"] = partition_1_ambient_at_space_max_temp
    partitions_dict["Partition_1"]["Unconditioned_Space_Min_Temp"] = partition_1_unconditioned_space_min_temp
    partitions_dict["Partition_1"]["Ambient_At_Space_Min_Temp"] = partition_1_ambient_at_space_min_temp

    partitions_dict["Partition_2"]["Ceiling_Wall"] = partition_2_ceiling_wall
    partitions_dict["Partition_2"]["Area"] = partition_2_area
    partitions_dict["Partition_2"]["Uvalue"] = partition_2_uvalue
    partitions_dict["Partition_2"]["Unconditioned_Space_Max_Temp"] = partition_2_unconditioned_space_max_temp
    partitions_dict["Partition_2"]["Ambient_At_Space_Max_Temp"] = partition_2_ambient_at_space_max_temp
    partitions_dict["Partition_2"]["Unconditioned_Space_Min_Temp"] = partition_2_unconditioned_space_min_temp
    partitions_dict["Partition_2"]["Ambient_At_Space_Min_Temp"] = partition_2_ambient_at_space_min_temp
    
    return partitions_dict

current_path = os.getcwd()
create_json(f"{current_path}/autocad_output.txt")
process_json_data()

with open(save_path_autoit_json, 'w', encoding="utf-8") as json_file:
    json.dump(final_data, json_file, indent=2, ensure_ascii=False)

os.system("C:/\"Program Files (x86)\"/AutoIt3/AutoIt3.exe ./AutoHAP.au3")