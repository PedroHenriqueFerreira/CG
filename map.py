import json

from settings import LINE_WIDTH

from vec import Vec2

class Polygon:
    def __init__(
        self,
        name: str | None = None,
        coords: list[list[Vec2]] | None = None,
        type: str | None = None
    ):
        self.name = name
        self.coords = coords

        self.triangles = [self.triangulate(coord) for coord in coords]

        self.type = type

        self.min = self.min()
        self.max = self.max()
        self.centroid = self.centroid()

    def min(self):
        x = min([point.x for coord in self.coords for point in coord])
        y = min([point.y for coord in self.coords for point in coord])

        return Vec2(x, y)

    def max(self):
        x = max([point.x for coord in self.coords for point in coord])
        y = max([point.y for coord in self.coords for point in coord])

        return Vec2(x, y)

    def centroid(self):
        size = sum([len(coord) for coord in self.coords])

        x = sum([point.x for coord in self.coords for point in coord]) / size
        y = sum([point.y for coord in self.coords for point in coord]) / size

        return Vec2(x, y)

    def triangulate(self, polygon: list[Vec2]):
        triangles: list[Vec2] = []

        if self.isClockwise(polygon):
            polygon = polygon[::-1]
        else:
            polygon = polygon[:]

        while len(polygon) >= 3:
            a = self.getEar(polygon)
            if a == []:
                break

            triangles.extend(a)
        return triangles

    def isClockwise(self, polygon: list[Vec2]):
        # initialize sum with last element
        sum = (polygon[0].x - polygon[len(polygon) - 1].x) * (polygon[0].y + polygon[len(polygon) - 1].y)

        # iterate over all other elements (0 to n-1)
        for i in range(len(polygon) - 1):
            sum += (polygon[i + 1].x - polygon[i].x) * (polygon[i + 1].y + polygon[i].y)

        return sum > 0

    def getEar(self, polygon: list[Vec2]):
        size = len(polygon)

        if size < 3:
            return []

        if size == 3:
            tri = [polygon[0], polygon[1], polygon[2]]
            del polygon[:]
            return tri

        for i in range(size):
            tritest = False

            p1 = polygon[(i - 1) % size]
            p2 = polygon[i % size]
            p3 = polygon[(i + 1) % size]

            if self.isConvex(p1, p2, p3):
                for x in polygon:
                    if not (x in (p1, p2, p3)) and self.isInTriangle(p1, p2, p3, x):
                        tritest = True

                if tritest == False:
                    del polygon[i % size]
                    return [p1, p2, p3]
        return []

    def isConvex(self, a: Vec2, b: Vec2, c: Vec2):
        # only convex if traversing anti-clockwise!
        crossp = (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

        if crossp >= 0:
            return True

        return False

    def isInTriangle(self, a: Vec2, b: Vec2, c: Vec2, p: Vec2):
        return (c.x - p.x) * (a.y - p.y) - (a.x - p.x) * (c.y - p.y) >= 0 and \
                (a.x - p.x) * (b.y - p.y) - (b.x - p.x) * (a.y - p.y) >= 0 and \
                (b.x - p.x) * (c.y - p.y) - (c.x - p.x) * (b.y - p.y) >= 0
                
class Line:
    def __init__(self, name: str | None, coords: list[Vec2] | None = None):
        self.name = name
        self.coords = coords

        self.quads = self.fourangulate()

    def fourangulate(self):
        quads: list[list[Vec2]] = []

        for prev, curr in zip(self.coords[:-1], self.coords[1:]):
            delta = (curr - prev).normalize()

            normal = Vec2(-delta.y, delta.x)

            q0 = prev + normal * (LINE_WIDTH / 2)
            q1 = prev - normal * (LINE_WIDTH / 2)
            q2 = curr - normal * (LINE_WIDTH / 2)
            q3 = curr + normal * (LINE_WIDTH / 2)

            quads.append([q0, q1, q2, q3])

        return quads


class Map:
    def __init__(self, file: str):
        self.file = file

        self.polygons: list[Polygon] = []
        self.lines: list[Line] = []

        self.graph: dict[Vec2, list[Vec2]] = {}

        self.min = Vec2(float('inf'), float('inf'))
        self.max = Vec2(float('-inf'), float('-inf'))

        self.load()

    def __repr__(self):
        return f'Map({self.file})'

    def updateBorder(self, coord: Vec2):
        self.min.x = min(self.min.x, coord.x)
        self.max.x = max(self.max.x, coord.x)
        self.min.y = min(self.min.y, coord.y)
        self.max.y = max(self.max.y, coord.y)

    def load(self):
        with open(self.file, 'r') as f:
            data = json.loads(f.read())

        for feature in data['features']:
            type = feature['geometry']['type']
            coords: list[list[float]] = feature['geometry']['coordinates']

            properties = feature['properties']
            name_ = properties.get('name')

            if type == 'Polygon':
                if properties.get('type') == 'boundary':
                    continue

                if properties.get('leisure') == 'park':
                    continue

                coords_ = []

                for coord in coords:
                    coord_ = []

                    for x, y in coord[:-1]:
                        point = Vec2(x, y)

                        coord_.append(point)
                        self.updateBorder(point)

                    coords_.append(coord_)

                type_ = 'building'

                if properties.get('landuse') in (
                    'basin',
                    'salt_pond',
                ) or properties.get('leisure') in (
                    'swimming_pool',
                ) or properties.get('natural') in (
                    'reef',
                    'water',
                ):
                    type_ = 'water'

                if properties.get('landuse') in (
                    'allotments',
                    'flowerbed',
                    'forest',
                    'meadow',
                    'orchard',
                    'plant_nursery',
                    'vineyard',
                    'cemetery',
                    'grass',
                    'recreation_ground',
                    'village_green',
                ) or properties.get('leisure') in (
                    'garden',
                    'pitch',
                ) or properties.get('natural') in (
                    'grassland',
                    'heath',
                    'scrub',
                    'wood',
                    'wetland',
                ):
                    type_ = 'grass'

                if properties.get('natural') in (
                    'beach',
                    'sand'
                ):
                    type_ = 'sand'

                self.polygons.append(Polygon(name_, coords_, type_))

            elif type == 'LineString':
                if properties.get('highway') not in (
                    'motorway',
                    'trunk',
                    'primary',
                    'secondary',
                    'tertiary',
                    'unclassified',
                    'residential',
                    'motorway_link',
                    'trunk_link',
                    'primary_link',
                    'secondary_link',
                    'tertiary_link',
                    'living_street',
                    'service',
                    'pedestrian',
                    'raceway',
                    'road',
                ):
                    continue

                coords_: list[Vec2] = []

                for prev, curr, next in zip([None] + coords[:-1], coords, coords[1:] + [None]):
                    point = Vec2(*curr)

                    coords_.append(point)
                    self.updateBorder(point)

                    if point not in self.graph:
                        self.graph[point] = []

                    if prev is not None:
                        prev_point = Vec2(*prev)

                        if prev_point not in self.graph[point]:
                            self.graph[point].append(prev_point)

                    if next is not None:
                        next_point = Vec2(*next)

                        if next_point not in self.graph[point]:
                            self.graph[point].append(next_point)

                self.lines.append(Line(name_, coords_))

    def aStar(self, start: Vec2, goal: Vec2):
        openSet = {start}

        cameFrom = {}

        gScore: dict[Vec2, float] = {start: 0}
        fScore = {start: Vec2.distance(start, goal)}

        while len(openSet) > 0:
            current = min(openSet, key=lambda x: fScore[x])

            if current == goal:
                total_path = [current]

                while current in cameFrom:
                    current = cameFrom[current]
                    total_path.append(current)

                return total_path, gScore[goal]


            openSet.remove(current)

            for neighbor in self.graph[current]:
                tentative_gScore = gScore[current] + Vec2.haversine(current, neighbor)

                if neighbor not in gScore or tentative_gScore < gScore[neighbor]:
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = tentative_gScore + Vec2.distance(neighbor, goal)

                    if neighbor not in openSet:
                        openSet.add(neighbor)

        return None, 0.0


if __name__ == '__main__':
    location = Map('russas.geojson')
