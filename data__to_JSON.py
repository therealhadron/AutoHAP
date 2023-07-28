import re
import json
import main

save_path = "./data.json"
final_data = {}
final_data["Spaces"] = []
save_path_final = "./final.json"

def create_json(file_path):
    data = {}
    try:
        with open(file_path, 'r') as file:
            content = file.readlines()
            index = 0
            add_object = False
            text_id = 0
            room_list = []
            text_list = []
            while index < len(content):
                line = content[index].replace('\n','')
                if line == "{":
                    add_object = True
                if add_object:
                    object = re.search(r"<([^>]+)>", line).group(1) if re.search(r"<([^>]+)>", line) else None

                    # Parsing layer name items
                    if object == "Layer_name":
                        layer_name = re.search(r'>\s*(.*)', content[index]).group(1)

                        # W.I.P. just skipping for now
                        if layer_name == "System_Window_Line":
                            add_object = False
                            continue

                        if layer_name == "Building_Outline":
                            key = "Building_Outline"
                            coord_list = []
                            index = index + 2 #Moves the index one ahead to start at the first coordinate
                            while content[index].replace('\n','') != "}":
                                coord_list.append(eval(content[index]))
                                index = index + 1
                            add_object = False
                            data[key] = {"Coordinates": coord_list}
                        
                        if layer_name == "Room_Outline":
                            coord_list = []
                            index = index + 2 #Moves the index one ahead to start at the first coordinate
                            while content[index].replace('\n','') != "}":
                                coord_list.append(eval(content[index]))
                                index = index + 1
                            add_object = False
                            room_list.append({"Coordinates": coord_list})
                        
                        if layer_name == "Text":
                            add_object = False
                            text_id = text_id + 1
                            key = (f"Text_{text_id}")
                            text = re.search(r'>\s*(.*)', content[index+1]).group(1)
                            text = text.split('\P',-1)
                            text_contents = {}
                            for line in text:
                                text_key = line.split(':',-1)[0]
                                text_value = line.split(':',-1)[1]
                                text_contents[text_key] = text_value
                            text_list.append({"Text":text_contents,
                                        "Coordinates":eval(content[index+3])
                                        })
                index = index + 1
            data["Rooms"] = room_list
            data["Texts"] = text_list
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except IOError:
        print(f"Error reading file '{file_path}'.")
    with open(save_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def process_json_data():
    global final_data
    num_of_rooms = 0

    with open(save_path, 'r') as json_file:
        json_data = json.load(json_file)
    room_data = {}
    rooms = json_data["Rooms"]
    texts = json_data["Texts"]
    building_outline = json_data["Building_Outline"]["Coordinates"]

    for text in texts:
        text_coordinates = text["Coordinates"]
        for room in rooms:
            room_vertex = room["Coordinates"]
            if main.is_coordinate_in_polygon(room_vertex, text_coordinates):
                text_name = text["Text"]["Name"]
                text_ceiling_height = text["Text"]["height"]
                num_of_rooms = num_of_rooms + 1
                spaces_floor_area = main.calculate_enclosed_area(room_vertex)

                for i, room_coordinate in enumerate(room_vertex):
                    if i < len(room_vertex) - 1:
                        room_coordinate_1 = room_coordinate
                        room_coordinate_2 = room_vertex[i + 1]
                        room_wall_length = main.calculate_side_length(room_coordinate_1,room_coordinate_2)
                        for j, building_coordinate in enumerate(building_outline):
                            if j < len(building_outline) - 1:
                                is_room_wall_in_building_outline = main.is_point_on_line(room_coordinate_1, room_coordinate_2, building_coordinate) and \
                                                                    main.is_point_on_line(room_coordinate_1, room_coordinate_2, building_outline[j + 1])
                                is_building_outline_in_room_wall = main.is_point_on_line(building_coordinate, building_outline[j + 1], room_coordinate_1) and \
                                                                    main.is_point_on_line(building_coordinate, building_outline[j + 1], room_coordinate_2)
                                if is_room_wall_in_building_outline or is_building_outline_in_room_wall:
                                    print(text_name, room_wall_length)
                                    print(main.wall_direction(room_vertex))
                
                room_data["General"] = insert_spaces_general(text_name, spaces_floor_area, text_ceiling_height)
                room_data["Internals"] = insert_spaces_internals()
                room_data["Walls_Windows_Doors"] = insert_walls_windows_doors()
                room_data["Partitions"] = insert_spaces_partitions()
                final_data["Spaces"].append(room_data)
                room_data = {}

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
                            internal_electric_equipment_unit = "W/ft^2",
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

    if wall_exposure is None:
        for x in range(8):
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
    roofs_skylights_dict = {}
    return roofs_skylights_dict

def insert_infiltration(design_cooling_CFM = 0,
                        design_heating_CFM = 0,
                        energy_analysis_CFM = 0):
    infiltration_dict = {}
    return infiltration_dict

def insert_floors():
    floors_dict = {}
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

create_json("./Drawing2.txt")
process_json_data()

with open("./final_data.json", 'w') as json_file:
    json.dump(final_data, json_file, indent=2)