"""
Utilidades de MidiReader

"""
from physical_synthesis.ks_guitar import GuitarString
from Additive_Synthesis.Instruments import Instrument




def midi_to_freq(midi_note):
    midiA4 = 69
    f = 2**((midi_note-midiA4)/12) * 440
    return round(f, 2)


def find_note_off(note, track):
    current_time_in_ticks = 0
    for msg in track:
        if msg.is_meta == 0:
            current_time_in_ticks += msg.time
            if msg.type == 'note_off' and msg.note == note:
                break
    return current_time_in_ticks


#Covierte a la 4ta octava, todo mejorar repeticiond e codigo.
def convert_4oct(real_note):
    if round(real_note) in range(24, 36):
        return real_note + 36
    elif round(real_note) in range(36, 48):
        return real_note + 24
    elif round(real_note) in range(48, 60):
        return real_note + 12
    elif round(real_note) in range(72, 84):
        return real_note - 12
    elif round(real_note) in range(84, 96):
        return real_note - 24
    elif round(real_note) in range(96, 108):
        return real_note - 36
    elif round(real_note) in range(108, 120):
        return real_note - 48
    elif round(real_note) in range(120, 128):
        return real_note - 60
    else:
        return real_note

def synthesize(sample_rate, frequency, length, form, instrument, noise):
    if form == 'additive':
        instrumento = Instrument(instrument)
        return instrumento.get_sound(frequency, length)
    elif form == 'physical':
        if instrument == 'guitar':
            guitarnote = GuitarString(frequency, sample_rate, 1, length * sample_rate, noise)
            return guitarnote.get_samples()
        else:
            pass

