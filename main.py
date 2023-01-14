import numpy as np

np.random.seed(1547)

from utils.sb import StoryBoard
from utils.objects import Scale

from essence.effects.rain import Rain
from essence.effects.stars import StarZoom
from essence.effects.orb_rotation import OrbRotation
from essence.effects.bubble import Bubble
from essence.effects.final_dialog import forever
from essence.effects.ascension import Ascendance
from essence.effects.uncertainty import Uncertainty

def wons(start, end):
    snow = Rain('sb/elements/sq.jpg',150,-4*np.pi/3)
    list_objects = snow.render(start,end)
    for i in range(len(list_objects)):
        list_objects[i].add_action(Scale(0, start, end, 4.5, 4.5))
    return list_objects

def render(full_sb=True):
    if full_sb:
        sb = StoryBoard().from_osb('poly.osb')
    else:
        sb = StoryBoard()
    wons_2023 = wons(62944, 92712)
    star_zoom = StarZoom(500)
    forever_render = forever()
    orb_rot = OrbRotation(50)
    bbl = Bubble(50)
    ascendance = Ascendance()
    uncertainty = Uncertainty('assets/essence_xi_midi.mid')
    sb.Objects['background'] += wons_2023
    sb.Objects['background'] += forever_render
    sb.Objects['background'] += star_zoom.render(287893, 301512)
    sb.Objects['background'] += orb_rot.render(301512, 310860, 0.0008, 0.002, 0.003)
    sb.Objects['background'] += bbl.render(180304, 198248, 280 * 16)
    sb.Objects['background'] += ascendance.render(217316, 225267, 230721)
    sb.Objects['background'] += uncertainty.render(109652)
    return sb

def main():
    sb = render(full_sb=True)
    sb.osb('takehirotei vs. HowToPlayLN - Essence (who will upload this idk).osb')

if __name__ == "__main__":
    main()
