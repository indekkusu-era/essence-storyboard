import random
from .rain import Rain
from utils.objects import Sprite, Move, MoveY, Fade, Scale, Loop, Color
from utils.constants import SB_WIDTH, SB_HEIGHT

random.seed(1547)

class Ascension():
    _bg = 'sb/backgrounds/normal_bg.png'
    _star = "sb/elements/star.png"
    _white = 'sb/white/white.png'
    def __init__(self, start, end):
        self._start = start
        self._end = end
    
    def _black_cover(self):
        white = Sprite(self._white)
        white.add_action(Color(0, self._start, self._end, (0,0,0), (0,0,0)))
        white.add_action(Scale(0, self._start, self._end, 5, 5))
        return white

    def bg(self):
        bg = Sprite(self._bg)
        bg.add_action(Scale(0, self._start, self._end, 1, 1))
        return bg

    def _scroll_up(self, bg: Sprite):
        bg.add_action(MoveY(2, self._start, self._end, 240, 1000))
        return bg

    def render(self):
        all_sprites = []
        black = self._black_cover()
        bg = self.bg()
        stars = Rain(self._star, 20, 0)
        bg = self._scroll_up(bg)
        all_sprites.extend([black, bg])
        all_sprites.extend(stars.render(self._start, self._end))
        return all_sprites
