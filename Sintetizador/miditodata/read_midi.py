"""
Leo archivos midi y los interpreto

"""

import mido
import numpy as np

from Additive_Synthesis.instrument_utils import find_nearest
from physical_synthesis.ks_guitar import GuitarString


def midi_to_freq(midi_note):
    midiA4 = 69
    f = 2**((midi_note-midiA4)/12) * 440
    return round(f,2)


def find_note_off(note, track):
    time = 0
    for msg in track:
        if msg.is_meta == 0:
            #print(msg)
            time += msg.time
            if msg.type == 'note_off' and msg.note == note:
                break
            #print(time)
    return time


class Mynote:
    def __init__(self, fs, pitch, t_i, t_f, A):
        """Initialize Note Object"""
        self.fs = fs
        self.pitch = pitch
        self.t_i = t_i
        self.t_f = t_f
        self.A = A
        self.sound = None

    def get_len(self):
        return self.t_f - self.t_i

    def get_len_seconds(self, ticks_per_beat, tempo):
        return mido.tick2second(self.get_len(), ticks_per_beat, tempo)

    def get_initial_time_seconds(self, ticks_per_beat, tempo):
        return mido.tick2second(self.t_i, ticks_per_beat, tempo)

    def add_sound(self, sound): #Sound should be the array of sample values in time
        """Attaches the sound for this note as an array of samples"""
        self.sound = sound

    def get_sample(self, time):
        """Returns the sample at a given time. If it isn't the time for the note to play it will return an empty value"""

        if time < self.t_i or time > self.t_f:
            sample = 0
        else:
            sample = self.sound[time-self.t_i]

        return sample


class MyTrack:
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
                #print('\n' + str(msg))
                t_i += msg.time
                A = msg.velocity
                t_f = t_i + find_note_off(msg.note, track[msg_num:len(track)+1])
                pitch = midi_to_freq(msg.note)
                new_note = Mynote(fs, pitch, t_i, t_f, A)
                notes.append(new_note)
                #print('Pitch: {} \tt_i: {}   \tt_f: {}'.format(pitch, t_i, t_f))
                msg_num += 1
    return notes


mid = mido.MidiFile('tester.mid', clip=True)

note_list = track_parse(mid.tracks[1])


largo = mid.length
print(largo)
tempo_usable = 461538
sample_rate = 11025

time = np.arange(0, largo, 1 / 11025)
y = np.zeros(len(time))



for note in note_list:
    length = note.get_len_seconds(mid.ticks_per_beat, tempo_usable)
    print(length)
    pitch = note.pitch

    #busco que indice es el mas cercano al tiempo inicial de mi nota
    index = find_nearest(time, note.get_initial_time_seconds(mid.ticks_per_beat, tempo_usable))
    print(index)
    #sintetizo nota

    guitarnote = GuitarString(pitch, 1 / sample_rate, 1, length * sample_rate, '2-level')
    sample = guitarnote.get_samples()
    #Ahora debo sumar en el arreglo y, desde index hasta el final de mi nota

    for idx in range(index, len(sample)):
        y[idx] += sample[idx]


import pyaudio
p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=sample_rate,
                frames_per_buffer=1024,
                output=True,
                output_device_index=1
                )


stream.write(y.astype(np.float32).tostring())
stream.close()
