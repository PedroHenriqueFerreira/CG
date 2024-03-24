from priority_queue import PriorityQueue
from vector import Vector2
from map import Map
import math

class Node:
    def __init__(self, coords: Vector2, extremities, from_coord=None, path_cost=0) -> None:
        self.coords = coords
        self.from_coord = from_coord #no, não cordenada, para facilita pegar o caminho
        if from_coord != None:
            self.path_cost = from_coord.path_cost + self.Haversine(from_coord)
        else:
            self.path_cost = path_cost

    def getmembers(self):
        return f"{type(self.coords)}: {self.coords}\n{type(self.from_coord)}: {self.from_coord}\n{type(self.path_cost)}: {self.path_cost}"

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.coords == other.coords #checar se vector tem implementação de comparaçao
        return False

    def haversine(self, from_coord):
        lat1, lon1, lat2, lon2 = map(math.radians, [from_coord.coords.x, from_coord.coords.y, self.coords.x, self.coords.y])

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        r = 6371
        distance = r * c

        return distance
    
    def way(self):
        aux = self
        way_coords = []
        while aux.from_coord is not None:
            way_coords.append(aux.from_coord)
            aux = aux.from_coord
        return list(reversed(way_coords))


def getExtremities(location, coord):
    for line in location.lines:
        for point in line.coords:
            if math.isclose(distance(coord.coords, point), 0):
                return [line.coords[0], line.coords[-1]]

def Extend(location, coord):
    neighborhood = []
    ref = []
    for line in location.lines:
        for point in line.coords:
            if math.isclose(distance(coord.coords, point), 0):
                if ref:
                    neighborhood.append            

def distance(A:Vector2, B:Vector2):
    return ((B.x - A.x)**2 + (B.y - A.y)**2)**0.5

def Astar(location: Map, origin_coords, dest_coords):
    f = lambda n: n.path_cost + distance(n.coords, dest_coords)
    origin = Node(origin_coords)
    frontier = PriorityQueue(f)
    frontier.append(origin)
    explored = set()
    while frontier:
        coord = frontier.pop()
        if coord.coords == dest_coords:
            return coord
        explored.add(coord.coords)
        print(Extend(location, coord))
        for to_coord in Extend(location, coord):
            if to_coord.coords not in explored and coord not in frontier:
                frontier.append(to_coord)
            elif coord in frontier:
                if f(to_coord) < frontier[to_coord]:
                    del frontier[to_coord]
                    frontier.append(to_coord)
    return None

if __name__=="__main__":
    location = Map("russas.geojson")
    origin = Vector2(-37.9701597, -4.9385131)
    dest = Vector2(-37.9749484, -4.9436688)
    r = Astar(location, origin, dest)