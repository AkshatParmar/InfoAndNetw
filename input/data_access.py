import json
from os import path

class JsonDataAccess():
    def __init__(self, filename):
        self.filename = filename
        if not path.exists(filename):
            with open(self.filename, 'w') as f:
                empty_dict = {}
                json.dump(empty_dict, f)
    
    def insert(self, dict_data, key):
        with open(self.filename, 'r') as f:
            data = json.load(f)
        
        if key in data.keys():
            return False
        
        data[key] = dict_data
        with open(self.filename,'w') as f: 
            json.dump(data, f)

        return True

    def update(self, dict_data, key):
        with open(self.filename, 'r') as f:
            data = json.load(f)
        
        if key not in data.keys():
            return False
        
        data[key] = dict_data
        with open(self.filename,'w') as f: 
            json.dump(data, f)

        return True
    
    def delete(self, key):
        with open(self.filename, 'r') as f:
            data = json.load(f)
        
        if key not in data.keys():
            return False
        
        data.pop(key)

        with open(self.filename,'w') as f: 
            json.dump(data, f)

        return True
    
    def search(self, key):
        with open(self.filename, 'r') as f:
            data = json.load(f)

        if key not in data.keys():
            return None
        
        return data[key]
