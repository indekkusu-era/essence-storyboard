from essence.config import mapper_names
from utils.objects import Sprite
from utils.objects.actions import Fade, Move, Scale

class MapperEffect:
    pos = (710, 130)
    def __init__(self, mapper_name):
        self._mapper_name = mapper_name
    
    def render(self, start, end):
        x, y = self.pos
        mapper_sprite = Sprite(f'sb/mappers/{self._mapper_name}.png', align='CentreRight')
        mapper_sprite.add_actions([
            Scale(0, start, end, 0.5, 0.5),
            Move(0, start, start + 100, (x + 20, y), (x, y)),
            Move(0, end - 100, end, (x, y), (x + 20, y)),
            Fade(0, start, start + 100, 0, 1),
            Fade(0, end - 100, end, 1, 0),
        ])
        return [mapper_sprite]

def essence_mappers():
    end = 430572
    offsets = list(mapper_names.keys()) + [end]
    mapper = list(mapper_names.values())
    all_sprites = []
    for i in range(len(mapper)):
        if mapper[i] == "": continue
        all_sprites += MapperEffect(mapper[i]).render(offsets[i], offsets[i+1])
    return all_sprites
