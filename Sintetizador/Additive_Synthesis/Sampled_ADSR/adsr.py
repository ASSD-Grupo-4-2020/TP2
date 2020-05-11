import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq, ifft
from scipy.io import wavfile

from Additive_Synthesis.Sampled_ADSR.utils import find_nearest, shift2, extend, smooth
from Additive_Synthesis.waves import generate_wave
from nptowav.numpy_to_wav import write_timeline_to_wav


class Instrument:
    violin_sample_rate, violin_data = wavfile.read('Wavs/violin-C4.wav')
    flute_sample_rate, flute_data = wavfile.read('Wavs/flute-G4.wav')
    trumpet_sample_rate, trumpet_data = wavfile.read('Wavs/trumpet-C4.wav')
    piano_sample_rate, piano_data = wavfile.read('Wavs/piano-C4.wav')

    def __init__(self, instrumnet):
        self.instrument = instrumnet

        if self.instrument == 'violin':
            self.sample_rate = Instrument.violin_sample_rate
            self.data = Instrument.violin_data
            self.harmonics_n = 13
            self.fundamental_frequency = 261
            self.cutoff = 80
            self.fudnamental_amp = 1.662e7
            self.partial_amps = [5.45651e6, 3.02029e6, 2.30182e6, 2.29503e6, 1.6187e6, 612246, 1.14481e6, 1.27999e6,
                              141558, 104204, 331075, 789459, 291382]

        elif self.instrument == 'flute':
            self.sample_rate = Instrument.flute_sample_rate
            self.data = Instrument.flute_data
            self.harmonics_n = 6
            self.fundamental_frequency = 392
            self.cutoff = 40
            self.partial_amps = None

        elif self.instrument == 'piano':
            self.sample_rate = Instrument.piano_sample_rate
            self.data = Instrument.piano_data
            self.harmonics_n = 8
            self.fundamental_frequency = 261
            self.cutoff = 40
            self.partial_amps = None

        elif self.instrument == 'trumpet':
            self.sample_rate = Instrument.trumpet_sample_rate
            self.data = Instrument.trumpet_data
            self.harmonics_n = 6
            self.fundamental_frequency = 392
            self.cutoff = 40
            self.partial_amps = None

        else:
            pass

    def get_base_adsr(self, frequency, duration):

        samples = self.data.shape[0]

        time = np.arange(0, samples / self.sample_rate, 1 / self.sample_rate)

        datafft = fft(self.data)

        freqs = fftfreq(samples, 1 / self.sample_rate)

        pos_freqs = freqs[:int(len(freqs) / 2)]

        index_pos_fundamental = find_nearest(pos_freqs, self.fundamental_frequency)
        index_pos_target = find_nearest(pos_freqs, frequency)
        diff = index_pos_target - index_pos_fundamental

        mask = np.copy(datafft)
        empty = []

        self.calculate_partial_shares()

        for var in range(1, self.harmonics_n + 1):
            mask2 = np.copy(mask)
            for cont in range(len(freqs)):
                if (freqs[cont] < -(self.fundamental_frequency * var) - self.cutoff) \
                        or (
                        -(self.fundamental_frequency * var) + self.cutoff < freqs[cont] < (self.fundamental_frequency * var) - self.cutoff) \
                        or (freqs[cont] > (self.fundamental_frequency * var) + self.cutoff):
                    mask2[cont] = 0

            pos_mask2 = mask2[:int(len(freqs) / 2)]
            neg_mask2 = mask2[int(len(freqs) / 2): len(freqs)]

            pos_mask2_shifted = shift2(pos_mask2, diff * var)
            neg_mask2_shifted = shift2(neg_mask2, - (diff * var))

            shifted_mask2 = np.concatenate((pos_mask2_shifted, neg_mask2_shifted))

            empty.append(shifted_mask2)

        output = sum(empty)

        adsr = ifft(output)

        maxi = np.amax(adsr)
        normalized = adsr / maxi

        ##hasta aca standard para cualquier instrumento


        #caso violin (funca buenardo)
        copy = normalized.copy()

        copy[copy < 0] = 0

        suave = smooth(copy.real)

        max_smooth = np.amax(suave)
        suave = suave / max_smooth

        new_time = np.arange(0, len(suave) / self.sample_rate, 1 / self.sample_rate)

        fundamental = generate_wave(frequency, suave, self.sample_rate)

        for v in range(2, self.harmonics_n + 1):
            sobretono = generate_wave(frequency * v, suave, self.sample_rate)
            fundamental += self.partial_amps[v - 2] * sobretono

        out = extend(fundamental, time, duration, self.sample_rate, self.instrument)

        path = '/Users/agustin/Desktop/omegalul4.wav'

        write_timeline_to_wav(path, out, self.sample_rate)

        return out

    def calculate_partial_shares(self):
        for k in range(len(self.partial_amps)):
            self.partial_amps[k] = self.partial_amps[k] / self.fudnamental_amp

instrumneto = Instrument('piano')
instrumneto.get_base_adsr(261, 2)
