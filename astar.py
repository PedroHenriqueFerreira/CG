from math import sin, cos, asin, sqrt

from vector import Vector2

def heuristic(start: Vector2, goal: Vector2):
    start = start.radians()
    goal = goal.radians()
    
    delta = goal - start
    
    a = sin(delta.x / 2) ** 2 + cos(start.x) * cos(goal.x) * sin(delta.y / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371

    return r * c

def reconstructPath(cameFrom: dict[Vector2, Vector2], current: Vector2):
    total_path = [current]
    
    while current in cameFrom:
        current = cameFrom[current]
        total_path.append(current)
        
    return total_path

def aStar(graph: dict[Vector2, list[Vector2]], start: Vector2, goal: Vector2):
    openSet = { start }
    
    cameFrom = {}
    
    gScore = { start: 0 }
    fScore = { start: heuristic(start, goal) }
    
    while len(openSet) > 0:
        current = min(openSet, key=lambda x: fScore[x])
        
        if current == goal:
            return reconstructPath(cameFrom, current)
        
        openSet.remove(current)
        
        for neighbor in graph[current]:
            tentative_gScore = gScore[current] + Vector2.distance(current, neighbor)
            
            if neighbor not in gScore or tentative_gScore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = tentative_gScore + heuristic(neighbor, goal)
                
                if neighbor not in openSet:
                    openSet.add(neighbor)
        
    return None