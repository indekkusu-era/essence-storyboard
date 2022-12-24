import os
from utils.objects import Sprite, Move, Fade, Scale
from utils.objects.images import get_text_image

class Speech:
    def __init__(self, text_sections: list[str], timestamps: list[tuple], end: int):
        self._text_sections = text_sections
        self._timestamps = timestamps
        self._end = end
    
    def render(self, position: tuple, font: str, scale: float):
        # generate characters
        script = "".join(self._text_sections)
        character_set = list(set("".join(self._text_sections)))
        char_size = {}
        for char in character_set:
            if char == "\n": continue
            char_number = ord(char)
            file_name = f'sb/characters/{char_number}.png'
            im = get_text_image(char_number, font, 40)
            char_size[char_number] = (im.width, im.height)
            if os.path.isfile(file_name):
                continue
            im.save(file_name)
        # predetermine the characters positions
        positions = []

        lines = script.split("\n")
        midpoint_section = len(lines) // 2 + 1
        