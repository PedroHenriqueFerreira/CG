from json import loads
from vec import Vec2

class Map:
    def __init__(self, filepath: str):
        self.filepath = filepath

        self.min = Vec2(float('inf'), float('inf'))
        self.max = Vec2(float('-inf'), float('-inf'))
    
        self.load()
    
    def load(self):
        with open(self.filepath, 'r') as f:
            data = loads(f.read())
        
        types = set()
            
        for feature in data['features']:
            types.add(feature['geometry']['type'])
            
        print(types)
            
if __name__ == '__main__':
    location = Map('russas.geojson')
    
          