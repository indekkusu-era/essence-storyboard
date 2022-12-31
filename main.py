import numpy as np

np.random.seed(1547)

from utils.sb import StoryBoard
from essence.effects.rain import Rain
from utils.objects import Scale

def wons(start, end):
    snow = Rain('sb/elements/sq.jpg',150,-4*np.pi/3)
    list_objects = snow.render(start,end)
    for i in range(len(list_objects)):
        list_objects[i].add_action(Scale(0, start, end, 4.5, 4.5))
    return list_objects

def main():
    s = wons(62944, 92712)
    sb = StoryBoard().from_osb('poly.osb')
    sb.Objects['background'] += s
    sb.osb('takehirotei vs. HowToPlayLN - Essence (who will upload this idk).osb')

if __name__ == "__main__":
    main()
