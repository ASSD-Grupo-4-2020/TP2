"""
Leo archivos midi y los interpreto

"""

import mido
import numpy as np

from Additive_Synthesis.instrument_utils import find_nearest
from nptowav.numpy_to_wav import write_timeline_to_wav
from physical_synthesis.ks_guitar import GuitarString
from Additive_Synthesis.Instruments import Instrument


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


def convert(real_note):
    if real_note in range(24, 36):
        return real_note + 36
    elif real_note in range(36, 48):
        return real_note + 24
    elif real_note in range(48, 60):
        return real_note + 12
    elif real_note in range(72, 84):
        return real_note - 12
    elif real_note in range(84, 96):
        return real_note - 24
    elif real_note in range(96, 108):
        return real_note - 36
    elif real_note in range(108, 120):
        return real_note - 48
    elif real_note in range(120, 128):
        return real_note - 60
    else:
        return  real_note

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
                pitch = midi_to_freq(convert(msg.note))
                new_note = Mynote(fs, pitch, t_i, t_f, A)
                notes.append(new_note)
                #print('Pitch: {} \tt_i: {}   \tt_f: {}'.format(pitch, t_i, t_f))
                msg_num += 1
    return notes


mid = mido.MidiFile('tester.mid', clip=True)

note_list = track_parse(mid.tracks[1])


largo = mid.length
#print(largo)
tempo_usable = 461538

ins_note = Instrument('flute')
sample_rate = ins_note.sample_rate
print(sample_rate)

time = np.arange(0, largo, 1 / sample_rate)
y = np.zeros(len(time))



for note in note_list:
    length = note.get_len_seconds(mid.ticks_per_beat, tempo_usable)
    #print(length)
    pitch = note.pitch

    #busco que indice es el mas cercano al tiempo inicial de mi nota
    index = find_nearest(time, note.get_initial_time_seconds(mid.ticks_per_beat, tempo_usable))
    #print('Tiempo incial: ' + str(note.get_initial_time_seconds(mid.ticks_per_beat, tempo_usable)))
    #print(index)
    #sintetizo nota

    nota_musical = ins_note.get_sound(pitch, length)


    #guitarnote = GuitarString(pitch, sample_rate, 1, length * sample_rate, 'normal')
    #sample = guitarnote.get_samples()
    #Ahora debo sumar en el arreglo y, desde index hasta el final de mi nota

    for idx in range(index, len(nota_musical)):
        y[idx] += nota_musical[idx]


print(len(y) / sample_rate)
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

###### Pruebas de Victor ########

fs = 44100
freqs = [98, 123, 147, 196, 294, 392, 392, 294, 196, 147, 123, 98]

unit_delay = fs//3

# Son los tiempos iniciales de cada nota
delays = [unit_delay * _ for _ in range(len(freqs))]

notes=[]
for freq, delay in zip(freqs, delays):
    new_note = Mynote(fs, freq, delay, delay+2*fs, 1) # 2*fs hace que cada una dure 2 seg
    notes.append(new_note)

for note in notes:
    # Sintetizo nota
    guitarnote = GuitarString(note.pitch, note.fs, note.A, note.get_len(), '2-level')
    note.add_sound(guitarnote.get_samples()) # Le asocio a cada objeto nota su respectivo sonido

# Combino los sonidos   
# Básicamente, recorre cada objeto MyNota, se fija si a un tiempo 't' le corresponde tocar (devuelve 0 o x(t)) y suma todo lo que encuentre para el momento 't'. Así continúa con toda la secuencia.
# Este nuevo arreglo deberías poder insertarlo al pyaudio. Es sólo el y(n) final con todas las notas juntas.
guitar_sound = [sum(note.get_sample(t) for note in notes) for t in range(fs*6)]

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                frames_per_buffer=1024,
                output=True,
                output_device_index=1
                )


stream.write(guitar_sound.astype(np.float32).tostring())
stream.close()