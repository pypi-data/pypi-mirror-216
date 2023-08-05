from filemod import writer

def number_detect(letter):
    """Detect the nature of letter is number or not"""

    try:
        int(letter)
        return True
    except:
        return False

def number_string(data):
    """Detect the nature of letter is number or not"""
    try:
        return int(data)
    except:
        return str(data)


def generate_array(data):
    """generate string arrays to real arrays"""
    array_temp = []
    array = []
    for array_elements in data:
        if array_elements in ["["]:
            continue
        elif array_elements in [",", "]"]:
            if number_detect(collab_words_in_list(array_temp).strip()):
                array.append(int(collab_words_in_list(array_temp).strip()))
            else:
                array.append(collab_words_in_list(array_temp).strip())
            array_temp.clear()
        else:
            array_temp.append(array_elements)
    return array


def collab_words_in_list(list):
    """collab word into strings"""
    return ''.join(list)


def allot_values(values : list):
    processed_values=[]
    for elements in values:
        
        if elements[0] == "[":
            processed_values.append(list(generate_array(elements)))
        elif elements=="True":
            processed_values.append(True)
        elif elements=="False":
            processed_values.append(False)
        else:
            processed_values.append(number_string(elements))
    return processed_values


def write_dict_in_file(filename : str ,data:dict)->bool:
    write_file = "{ \n"
    for key , value  in data.items():
        write_file = f"{write_file} {key} : {value}\n"
    write_file = write_file+"\n"+"}"
    return writer(filename, write_file, "w")
