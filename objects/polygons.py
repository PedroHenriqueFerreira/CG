from typing import TYPE_CHECKING
from glm import vec2

if TYPE_CHECKING:
    from objects.map import Map

class Polygon:
    def __init__(self, app: 'Map', coords: list[vec2], height: float):
        self.app = app
        
        self.coords = coords
        self.height = height

class Polygons:
    def __init__(self, app: 'Map'):
        self.app = app
        
        self.waters: list[Polygon] = []
        self.grasses: list[Polygon] = []
        self.buildings: list[Polygon] = []
        self.unknowns: list[Polygon] = []
        
    def load_polygon(self, properties: dict, coords: list[vec2]):
        if properties.get('type') in ('boundary', ):
            return

        if (
            properties.get('landuse') in ('forest', 'allotments', 'meadow', 'grass') or 
            properties.get('natural') in ('grassland', 'heath', 'scrub', 'wood', 'wetland') or 
            properties.get('leisure') in ('park',)
        ):
            self.grasses.append(Polygon(self.app, coords, 0.00002))
        
        elif (
            properties.get('leisure') in ('swimming_pool',) or 
            properties.get('natural') in ('water',)
        ):
            self.waters.append(Polygon(self.app, coords, 0.00001))

        elif (
            not properties.get('building')
        ):
            self.unknowns.append(Polygon(self.app, coords, 0.00003))
        
        else:
            height = float(properties.get('height', '3'))
            
            self.buildings.append(Polygon(self.app, coords, self.app.km_to_world(0.001) * height))

        self.polygons.append(Polygon(self, coords, height, color, texture, texture_normal, texture_size))

        return True