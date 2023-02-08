import py_midicsv as pm

def get_timestamps_and_pitches(midifp: str, bpm=None):
    csv = pm.midi_to_csv(midifp, strict=False)
    ticks = None
    ms_per_beat = None
    timestamps = {}
    pitches = {}
    bpm_lists = {}
    if bpm:
        ms_per_beat = 60000 / bpm
    for event in csv:
        attributes = event.replace("\n", "").split(", ")
        track_num, time, event_type = attributes[:3]
        if event_type == "Header":
            ticks = int(attributes[-1])
            continue
        if event_type == "Tempo" and not bpm:
            microsec_per_beat = int(attributes[-1])
            ms_per_beat = microsec_per_beat / 1000
            bpm_lists[int(time) / ticks] = ms_per_beat
            continue
        if event_type.lower() != "note_on_c":
            continue
        if int(attributes[-1]) == 0:
            continue
        n_beat = int(time) / ticks
        ms = 0
        if not bpm:
            sorted_keys = list(sorted(bpm_lists.keys()))
            for i, bpm_offset in enumerate(sorted_keys):
                if i == 0: continue
                if n_beat > bpm_offset:
                    ms += bpm_lists[sorted_keys[i-1]] * (bpm_offset - sorted_keys[i - 1])
                else:
                    ms += bpm_lists[sorted_keys[i-1]] * (n_beat - sorted_keys[i - 1])
                    break
            if n_beat > max(sorted_keys):
                ms += bpm_lists[sorted_keys[-1]] * (n_beat - sorted_keys[-1])
        else:
            ms = ms_per_beat * n_beat
        if int(track_num) not in timestamps:
            timestamps[int(track_num)] = [ms]
            pitches[int(track_num)] = [int(attributes[-2])]
            continue
        timestamps[int(track_num)].append(ms)
        pitches[int(track_num)].append(int(attributes[-2]))
    return timestamps, pitches

def get_time_signatures(midifp: str, bpm=None):
    csv = pm.midi_to_csv(midifp, strict=False)
    ticks = None
    ms_per_beat = None
    time_signatures = {}
    if bpm:
        ms_per_beat = 60000 / bpm
    for event in csv:
        attributes = event.replace("\n", "").split(", ")
        track_num, time, event_type = attributes[:3]
        if event_type == "Header":
            ticks = int(attributes[-1])
            continue
        if event_type == "Tempo" and not bpm:
            microsec_per_beat = int(attributes[-1])
            ms_per_beat = microsec_per_beat / 1000
            continue
        if event_type != "Time_signature":
            continue
        num, denom = int(attributes[3]), 2 ** int(attributes[4])
        time_signatures[int(int(time) / ticks * ms_per_beat)] = (num, denom)
    return time_signatures

