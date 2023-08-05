import os
import json
from pathlib import Path
from zipfile import ZipFile, is_zipfile

class FileManager:
    def __init__(self, filename):
        self.path = Path(filename)

    def read(self, encoding="utf-8"):
        return self.path.read_text(encoding)
        
    def load_json(self, encoding="utf-8"):
        return json.loads(self.path.read_text(encoding))
    
    def write(self, data, encoding="utf-8"):
        return self.path.write_text(data, encoding)
    

class ZipFileManager:
    def __init__(self, filename):
        self.path= Path(filename)

    def compress(self):
        with ZipFile(self.path.with_suffix(".zip"), mode="w") as archive:
            archive.write(self.path)
        
    def decompress(self):
        with ZipFile(self.path.with_suffix(".zip"), mode="r") as archive:
            archive.extract_all()

def check_argument_type(argument):
    if os.path.isdir(argument):
        return "Folder"
    elif os.path.isfile(argument):
        if is_zipfile(argument):
            return "Zip file"
        else:
            return "Regular file"
    else:
        return "Unknown"
    

def build_file_path(base_folder, file_name):
    return os.path.join(base_folder, file_name)
