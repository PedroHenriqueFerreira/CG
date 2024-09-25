from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.map import Map

from structures.vector import Vec2, Vec3


utf8_to_ascii: dict[str, str] = {
    'À': 'A', 'à': 'a',
    'Á': 'A', 'á': 'a',
    'Â': 'A', 'â': 'a',
    'Ã': 'A', 'ã': 'a',
    'Ç': 'C', 'ç': 'c',
    'È': 'E', 'è': 'e',
    'É': 'E', 'é': 'e',
    'Ê': 'E', 'ê': 'e',
    'Ì': 'I', 'ì': 'i',
    'Í': 'I', 'í': 'i',
    'Î': 'I', 'î': 'i',
    'Ò': 'O', 'ò': 'o',
    'Ó': 'O', 'ó': 'o',
    'Ô': 'O', 'ô': 'o',
    'Õ': 'O', 'õ': 'o',
    'Ù': 'U', 'ù': 'u',
    'Ú': 'U', 'ú': 'u',
    'Û': 'U', 'û': 'u'
}


class Text:
    def __init__(
        self,
        map: 'Map',
        value: str,
        coords: list[Vec2],
        color: Vec3,
        thickness: int,
        size: float,
        min_size: float,
        max_size: float
    ):
        self.map = map
        self.value = value
        self.coords = coords
        self.color = color
        self.thickness = thickness
        self.size = size
        self.min_size = min_size
        self.max_size = max_size

        self.coords_distance: list[float] = []
        self.coords_rotation: list[float] = []
        self.coords_width = 0

        self.chars_width: list[float] = []

        self.width = 0
        self.height = 0
        self.scale = 0

        self.loaded = False

    def load(self):
        self.value = ''.join(utf8_to_ascii.get(c, c) for c in self.value)

        if abs(Vec2.angle(Vec2(1, 0), self.coords[-1] - self.coords[0])) > 90:
            self.coords = self.coords[::-1]

        self.size = self.map.metrics.from_pct(self.size)
        self.min_size = self.map.metrics.from_km(self.min_size)
        self.max_size = self.map.metrics.from_km(self.max_size)

        for curr, next in zip(self.coords[:-1], self.coords[1:]):
            distance = Vec2.distance(curr, next)
            rotation = Vec2.angle(Vec2(1, 0), next - curr)

            self.coords_distance.append(distance)
            self.coords_rotation.append(rotation)

            self.coords_width += distance

        self.chars_width = [glutStrokeWidth(
            GLUT_STROKE_MONO_ROMAN, ord(c)) for c in self.value]

        self.width = sum(self.chars_width)
        self.height = glutStrokeHeight(GLUT_STROKE_MONO_ROMAN)
        self.scale = self.size / self.height

        self.loaded = True

    def split(self, scale: float, width: float):
        data: list[tuple[str, Vec2, float]] = []

        origin = (self.coords_width - width) / 2

        cum_distance = 0.0
        char_index = 0

        for rotation, distance, curr, next in zip(
            self.coords_rotation,
            self.coords_distance,
            self.coords[:-1],
            self.coords[1:]
        ):
            prev_cum_distance = cum_distance
            cum_distance += distance

            if cum_distance < origin:
                continue

            elif prev_cum_distance < origin:
                expected_distance = origin - prev_cum_distance

                pos = curr + (next - curr) * expected_distance / distance
                rot = rotation

                max_cum_char_width = distance - expected_distance

            elif char_index < len(self.value):
                pos = curr
                rot = rotation

                max_cum_char_width = distance
            else:
                break

            val = ''
            cum_char_width = 0

            for char in self.value[char_index:]:
                index = self.value.index(char)

                char_width = self.chars_width[index] * self.scale / scale
                cum_char_width += char_width

                if cum_char_width > max_cum_char_width:
                    break

                val += char
                char_index += 1

            data.append((pos, rot, val))

        if self.value != ''.join(v for _, _, v in data):
            return []

        return data

    def draw(self):
        if not self.loaded:
            self.load()

        height = self.height * self.scale / self.map.scale

        if height < self.min_size:
            scale = (self.height * self.scale) / self.min_size
        elif height > self.max_size:
            scale = (self.height * self.scale) / self.max_size
        else:
            scale = self.map.scale

        width = self.width * self.scale / scale

        if width > self.coords_width:
            return

        glColor3f(self.color.x, self.color.y, self.color.z)

        for pos, rot, val in self.split(scale, width):
            glPushMatrix()

            glTranslatef(pos.x, pos.y, 0)

            glRotatef(rot, 0, 0, 1)
            glScale(self.scale / scale, self.scale / scale, 1)
            glTranslatef(0, -self.height / 2, 0.005)

            glLineWidth(self.thickness)

            for char in val:
                glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, ord(char))

            glPopMatrix()
