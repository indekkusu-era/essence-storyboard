import numpy as np
from numpy import linspace
from utils.objects import Sprite, Move, MoveY, Fade, Scale, Loop, Color
from utils.objects.images import get_text_image
from utils.constants import SB_WIDTH, SB_HEIGHT

FINAL_DIALOG = [
"The sky seems to be more beautiful than usual...",
"But, it costs a life to resurrect another life.",
"I guess... that's all",
"It was not for you, for me, or for humanity after all",
"I just have a pleasure doing it."
]

start = 383877; end = 431983; dialog_duration = 5000

black = 'sb/white/white.png'

def display_dialogs(start:int, end:int, dialogs:list[str], dialog_name: str, dialog_duration=5000, font="assets/SourceSerifPro-Black.ttf"):
    intervals = linspace(start, end, len(dialogs)).astype(np.int32)
    pos = (SB_WIDTH // 2, SB_HEIGHT - 40)
    sprites = []
    for dialog, timestamp in zip(dialogs, intervals):
        img = get_text_image(dialog, font, 30)
        sprite = Sprite(f'sb/quotes/{dialog_name}-{timestamp}.png')
        sprite.from_image(img)
        sprite.add_actions([
            Move(0, timestamp, timestamp + 1, pos, pos), 
            Fade(0, timestamp, timestamp + 1000, 0, 1),
            Fade(0, timestamp + dialog_duration - 1000, timestamp + dialog_duration, 1, 0)
        ])
        sprites.append(sprite)
    return sprites

def forever():
    dialogs = display_dialogs(start, end, FINAL_DIALOG, 'forever-dialog')
    return dialogs
