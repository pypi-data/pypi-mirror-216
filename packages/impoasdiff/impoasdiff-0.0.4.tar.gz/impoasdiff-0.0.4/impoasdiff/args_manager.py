import os
from zipfile import is_zipfile

def get_argument_type(argument):
    if os.path.isdir(argument):
        return "Folder"
    elif os.path.isfile(argument):
        if is_zipfile(argument):
            return "Zip file"
        else:
            return "Regular file"
    else:
        return "Unknown"
    

def is_valid_args(arg1, arg2):
    if get_argument_type(arg1) != get_argument_type(arg2):
        return False
    elif get_argument_type(arg1) =="Unknown":
        return False
    return True
    

    