'''
json_txt/MainFile.py - version 1.4.6

[ ]extract_keys()-> fixed bugs
'''

import contextlib
from filemod import reader
from pytn.compiler import compiles
from pytn.SupportFuncs import *


def extract_keys(filename)->list:
    """
    extract keys from file
    1)this takes list or some times even file works. 
    2)finds for each specific line where '/n' is present(this means new line)
    3)and append every thing before ':' and append it in a list
    """
    txt_file_data=list(reader(filename))
    temp = []
    keys = []
    for index , element in enumerate(txt_file_data) :
        if element== "\n":
            for value_index in range(index, len(txt_file_data)):
                if txt_file_data[value_index] == ":":
                    keys.append(collab_words_in_list(temp))
                    temp.clear()
                    break
                elif txt_file_data[value_index] not in [":","}", "{"]:
                    temp.append(txt_file_data[value_index])

    keys=list(map(str.strip, keys)) 
    res = []
    [res.append(x) for x in keys if x not in res]          
    return res



def extract_values(filename:str)->list:
    """extract values from file"""

    temp : list = []
    values : list= []
    txt_file_data: list =list(reader(filename))
    for index ,element in enumerate(txt_file_data):
        if element == ":":
            for index in range(index, len(txt_file_data)):
                if txt_file_data[index] == "\n":
                    values.append(collab_words_in_list(temp).strip())
                    temp.clear()
                    break
                elif txt_file_data[index] not in [":","'",'"',"}", '\r']:
                    temp.append(txt_file_data[index])             
    return allot_values(values)

def extract_data(filename : str)->dict:
    """create a dictonary"""

    keys = extract_keys(filename)
    values = extract_values(filename)
    res = []
    [res.append(x) for x in keys if x not in res]
    keys=res
    return {keys[index]: values[index] for index in range(len(keys))}


def load_txt(data):
    """compiling the text file"""

    with contextlib.suppress(FileNotFoundError):
        return list(compiles(data))


def edit_data(filename: str, key: str, value: str):
    """
    edit value  from the file
    """
    
    data = extract_data(filename)

    data[key]=value

    return write_dict_in_file(filename,data)


def add_data(filename:str, newkeys:str, newvalues:str):
    """append data into txt file"""

    data : dict= extract_data(filename)
    data[newkeys]=newvalues
    # filling up template

    return write_dict_in_file(filename,data)

def remove_data(filename:str,key:str):
    '''
    remove keys from file
    '''

    data = extract_data(filename)

    data.pop(key)

    return write_dict_in_file(filename,data)