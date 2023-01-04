import numpy as np

np.random.seed(1547)

from utils.sb import StoryBoard
from utils.objects import Scale

from essence.effects.rain import Rain
from essence.effects.stars import StarZoom
from essence.effects.orb_rotation import OrbRotation
from essence.effects.final_dialog import forever

def wons(start, end):
    snow = Rain('sb/elements/sq.jpg',150,-4*np.pi/3)
    list_objects = snow.render(start,end)
    for i in range(len(list_objects)):
        list_objects[i].add_action(Scale(0, start, end, 4.5, 4.5))
    return list_objects

def main():
    s = wons(62944, 92712)
    zoomin = StarZoom(500)
    forever_render = forever()
    orb_rot = OrbRotation(50)
    sb = StoryBoard().from_osb('poly.osb')
    sb.Objects['background'] += s
    sb.Objects['background'] += forever_render
    sb.Objects['background'] += zoomin.render(287893, 301512)
    sb.Objects['background'] += orb_rot.render(301512, 310860, 0.0008, 0.002, 0.003)
    sb.osb('takehirotei vs. HowToPlayLN - Essence (who will upload this idk).osb')

if __name__ == "__main__":
    main()
