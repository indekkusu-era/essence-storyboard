speedcore_melody_timestamps = [271725, 272044, 272363, 272576, 272788, 273107, 273427, 273533, 273639, 273746, 274065, 274384, 274597, 274809, 275128, 275448, 275554, 275660, 275767, 276086, 276405, 276618, 276830, 277149, 277469, 277575, 277681, 277788, 277894, 278000, 278107, 278213, 278426, 278532, 278639, 278745, 278958, 279064, 279170, 279277, 279383, 279490, 279596, 279702, 279809, 280128, 280447, 280660, 280872, 281191, 281511, 281617, 281723, 281830, 282149, 282468, 282787, 282893, 283212, 283532, 283638, 283744, 283851, 284170, 284489, 284702, 284914, 285233, 285553, 285659, 285765, 285978, 286084, 286191, 286297, 286510, 286616, 286723, 286829, 286935, 287254, 287574, 287680, 287786, 287895]

figma_star_positions = [
    (-2298, 78),
    (-1951, -108),
    (-1572, 103),
    (-2638, -72.7),
    (-1927, 36),
    (-1729, -226),
    (-2986, -265),
    (-2237.1, -304),
    (-2727, 33),
    (-2382, -12.19),
    (-2314.27, -104.37),
    (-2224.34, -68.83),
    (-2158.29, -181)
]

bg_pos = (-3222, -371)
bg_size = (1920, 1080)

constellation_positions = []

for (x, y) in figma_star_positions:
    bgx, bgy = bg_pos
    bgw, bgh = bg_size
    constellation_positions.append(((x - bgx) / bgw * 640, (y - bgy) / bgh * 480 + 100))

essence_constellation_order = [
    11,
    10,
    9,
    8,
    7,
    13,
    12,
    6,
    5,
    1,
    2,
    3,
    4,
]

essence_constellation_edges_pred = [
    [9],
    [4],
    [4],
    [8],
    [11],
    [4],
    [8],
    [12],
    [9],
    [],
    [9],
    [10],
    [11]
]

constellation_initial_timestamps = 310860
constellation_endpoint_timestamps = 311936

constellation_vertices_timestamps = {}

for pos, order in zip(constellation_positions, essence_constellation_order):
    constellation_vertices_timestamps[pos] = constellation_initial_timestamps + (constellation_endpoint_timestamps - constellation_initial_timestamps) * ((order - 1) / len(essence_constellation_order))
