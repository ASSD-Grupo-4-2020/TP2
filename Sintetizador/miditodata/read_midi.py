"""
Leo archivos midi y los interpreto

"""

from mido import MidiFile

def midi_to_freq(midi_note):
    midiA4 = 69
    f = 2**((midi_note-midiA4)/12) * 440
    return round(f,2)

def find_note_off(note, track):
    time = 0
    for msg in track:
        if msg.is_meta == 0:
            print(msg)
            time += msg.time
            if msg.type == 'note_off' and msg.note == note:
                break
            print(time)
    return time



class my_note:
    def __init__(self, fs, pitch, t_i, t_f, A):
        """Initialize Note Object"""
        self.fs = fs
        self.pitch = pitch
        self.t_i = t_i
        self.t_f = t_f
        self.A = A

    def get_len(self):
        return self.t_f - self.t_i

class my_track:
    def __init__(self):
        self.notes = []

    def add_note(self, new_note):
        self.notes.append(new_note)
    

def track_parse(track):
    fs = 44100
    notes = []
    t_i = 0
    msg_num = 0
    for msg in track:
        if msg.is_meta == 0:
            if msg.type == 'note_on':
                print('\n' + str(msg))
                t_i += msg.time
                A = msg.velocity
                t_f = t_i + find_note_off(msg.note, track[msg_num:len(track)+1])
                pitch = midi_to_freq(msg.note)
                new_note = my_note(fs,pitch, t_i, t_f, A)
                notes.append(new_note)
                print('Pitch: {} \tt_i: {}   \tt_f: {}'.format(pitch, t_i, t_f))
                msg_num += 1
    return notes