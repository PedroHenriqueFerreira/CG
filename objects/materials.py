from glm import vec3

from settings import *

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.map import Map

class Materials:
    def __init__(self, app: 'Map'):
        self.grass = Material(
            GRASS_AMBIENT_MATERIAL, 
            GRASS_DIFFUSE_MATERIAL, 
            GRASS_SPECULAR_MATERIAL, 
            GRASS_SHININESS_MATERIAL
        )
        
        self.water = Material(
            WATER_AMBIENT_MATERIAL, 
            WATER_DIFFUSE_MATERIAL, 
            WATER_SPECULAR_MATERIAL, 
            WATER_SHININESS_MATERIAL
        )
        
        self.building = Material(
            BUILDING_AMBIENT_MATERIAL, 
            BUILDING_DIFFUSE_MATERIAL, 
            BUILDING_SPECULAR_MATERIAL, 
            BUILDING_SHININESS_MATERIAL
        )
        
        self.unknown = Material(
            UNKNOWN_AMBIENT_MATERIAL, 
            UNKNOWN_DIFFUSE_MATERIAL, 
            UNKNOWN_SPECULAR_MATERIAL, 
            UNKNOWN_SHININESS_MATERIAL
        )
        
        self.road = Material(
            ROAD_AMBIENT_MATERIAL, 
            ROAD_DIFFUSE_MATERIAL, 
            ROAD_SPECULAR_MATERIAL, 
            ROAD_SHININESS_MATERIAL
        )
        
        self.path = Material(
            PATH_AMBIENT_MATERIAL,
            PATH_DIFFUSE_MATERIAL,
            PATH_SPECULAR_MATERIAL,
            PATH_SHININESS_MATERIAL
        )
        
        self.ground = Material(
            GROUND_AMBIENT_MATERIAL,
            GROUND_DIFFUSE_MATERIAL,
            GROUND_SPECULAR_MATERIAL,
            GROUND_SHININESS_MATERIAL
        )
        
class Material:
    def __init__(self, ambient: vec3, diffuse: vec3, specular: vec3, shininess: float):
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess