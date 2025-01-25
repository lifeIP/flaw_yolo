SERVICE_FILE_NAME:str = "service_data/"

LIST_OF_VALUES = [
    "crop_left", 
    "crop_right",
    "crop_up",
    "crop_down",
    "confidence_threshold"
]

def get_service_data_from_file(prop):
    if prop not in LIST_OF_VALUES: 
        print("not in LIST_OF_VALUES")
        return None

    try:
        line = list()
        with open(SERVICE_FILE_NAME + prop, "r") as f:
            line = f.readline()
        return str(line).rstrip("\n")
    except:
        pass
    return None


def set_service_data_into_file(prop, value: str = ""):
    
    value = str(value)

    if prop not in LIST_OF_VALUES: 
        print("not in LIST_OF_VALUES")
        return
    
    value_2 = get_service_data_from_file(prop)
    if value == value_2: return

    if len(value) == 0:
        return

    try:
        line = list()
        with open(SERVICE_FILE_NAME + prop, "r") as f:
            line = f.readline()

        line = value + "\n"
        
        with open(SERVICE_FILE_NAME + prop, "w") as f:
            f.writelines(line)
    except:
        pass



