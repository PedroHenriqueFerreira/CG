from glm import vec2, min, max

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.map import Map

from objects.utils import Utils

class Metrics:
    def __init__(self, app: 'Map'):
        self.app = app
        
        self.min = vec2(float('inf'), float('inf'))
        self.max = vec2(float('-inf'), float('-inf'))
        
        self.delta = vec2(0, 0)
        
        self.aspect = 0.0
        
        self.distance = 0

    def load_box(self, data: dict):
        for feature in data['features']:
            geometry_type = feature['geometry']['type']
            geometry_coords = feature['geometry']['coordinates']

            if geometry_type == 'LineString':                
                coords = [vec2(*coord) for coord in geometry_coords]
            elif geometry_type == 'Polygon':
                coords = [vec2(*coord) for coord in geometry_coords[0]]
            else:
                continue

            self.min = min(self.min, min(coords))
            self.max = max(self.max, max(coords))

        self.delta = self.max - self.min
        
        self.aspect = self.delta.x / self.delta.y

        y = (self.min.y + self.max.y) / 2
        
        left = vec2(self.min.x, y)
        right = vec2(self.max.x, y)
        
        self.distance = Utils.haversine(left, right)
        
    def from_km(self, km: float):
        return (km / self.distance) * self.aspect * 2
        
    def from_pct(self, pct: float):
        return pct * 2

    def from_screen(self, pos: vec2):
        return vec2(2 * pos.x - 1, 1 - 2 * pos.y)

    def normalize(self, pos: vec2):
        return (((pos - self.min) / self.delta) * 2 - 1) * vec2(self.aspect, 1)

    def denormalize(self, pos: vec2):
        return (((pos / vec2(self.aspect, 1)) + 1) / 2) * self.delta + self.min
