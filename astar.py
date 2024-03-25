from vector import Vector2

def reconstructPath(cameFrom: dict[Vector2, Vector2], current: Vector2):
    total_path = [current]
    
    while current in cameFrom:
        current = cameFrom[current]
        total_path.append(current)
        
    return total_path

def aStar(
    graph: dict[Vector2, list[Vector2]], 
    start: Vector2, 
    goal: Vector2
):
    openSet = { start }
    
    cameFrom = {}
    
    gScore: dict[Vector2, float] = { start: 0 }
    fScore = { start: Vector2.distance(start, goal) }
    
    while len(openSet) > 0:
        current = min(openSet, key=lambda x: fScore[x])
        
        if current == goal:
            return reconstructPath(cameFrom, current), gScore[current]
        
        openSet.remove(current)
        
        for neighbor in graph[current]:
            tentative_gScore = gScore[current] + Vector2.haversine(current, neighbor)
            
            if neighbor not in gScore or tentative_gScore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = tentative_gScore + Vector2.distance(neighbor, goal)
                
                if neighbor not in openSet:
                    openSet.add(neighbor)
        
    return None, 0.0