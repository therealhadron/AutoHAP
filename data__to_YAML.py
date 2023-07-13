import yaml
import re

data = {}
save_path = "./data.yaml"

def create_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.readlines()
            index = 0
            add_object = False
            room_id = 0
            text_id = 0
            while index < len(content):
                line = content[index].replace('\n','')
                if line == "{":
                    add_object = True
                if add_object:
                    object = re.search(r"<([^>]+)>", line).group(1) if re.search(r"<([^>]+)>", line) else None
                    # Parsing text items
                    if object == "Text_contents":
                        add_object = False
                        text_id = text_id + 1
                        key = (f"Text_{text_id}")
                        text = re.search(r'>\s*(.*)', content[index].replace('\n','')).group(1)
                        text = text.split('\P',-1)
                        data[key] = {"Text":text,
                                     "Coordinates":content[index+2].replace('\n','')
                                    }
                        continue
                    # Parsing layer name items
                    if object == "Layer_name":
                        layer_name = re.search(r'>\s*(.*)', content[index].replace('\n','')).group(1)
                        
                        if layer_name == "Building_Outline":
                            key = "Building_Outline"
                        else:
                            room_id = room_id + 1
                            key = (f"Room_{room_id}")
                        
                        coord_list = []
                        index = index + 1 #Moves the index one ahead to start at the first coordinate
                        while content[index].replace('\n','') != "}":
                            coord_list.append(content[index].replace('\n',''))
                            index = index + 1
                        add_object = False
                        data[key] = coord_list
                index = index + 1
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except IOError:
        print(f"Error reading file '{file_path}'.")
    with open(save_path, 'w') as file:
        file.write(yaml.safe_dump(data))

create_yaml("./Drawing2.txt")