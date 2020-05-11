"""

Obtener timbre caracteristico de diferentes instrumentos a partir de la muestra de una nota,
comienzo con un wav de una nota, lo paso a np, analizo en frecuencia, filtro los armonicos, determino asi la adsr

"""

from math import ceil
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq, ifft
from scipy.signal import argrelextrema
from scipy.io import wavfile
from scipy import signal



from Additive_Synthesis.Sampled_ADSR.utils import find_nearest, shift2, extend, smooth
from Additive_Synthesis.waves import generate_wave
from nptowav.numpy_to_wav import write_timeline_to_wav
from scipy.interpolate import interp1d
from Additive_Synthesis.adsr_envelopes import relative_adsr

def base_adsr(form, frequency, duration):
    if form == 'violin':

        sample_rate, data = wavfile.read('Wavs/violin-C4.wav')
        harmonics_n = 13
        fundamental_frequency = 261
        corte = 80

        samples = data.shape[0]

        time = np.arange(0, samples / sample_rate, 1 / sample_rate)

        datafft = fft(data)

        freqs = fftfreq(samples, 1 / sample_rate)

        pos_freqs = freqs[:int(len(freqs) / 2)]

        index_pos_fundamental = find_nearest(pos_freqs, fundamental_frequency)
        index_pos_target = find_nearest(pos_freqs, frequency)
        diff = index_pos_target - index_pos_fundamental

        mask = np.copy(datafft)
        empty = []

        partial_amplitudes = [5.45651e6, 3.02029e6, 2.30182e6, 2.29503e6, 1.6187e6, 612246, 1.14481e6, 1.27999e6, 141558, 104204, 331075, 789459, 291382]

        maximun = 1.662e7

        for k in range(len(partial_amplitudes)):
            partial_amplitudes[k] = partial_amplitudes[k] / maximun

        for var in range(1, harmonics_n + 1):
            mask2 = np.copy(mask)
            for cont in range(len(freqs)):
                if (freqs[cont] < -(fundamental_frequency * var) - corte) \
                        or (-(fundamental_frequency * var) + corte < freqs[cont] < (fundamental_frequency * var) - corte) \
                        or (freqs[cont] > (fundamental_frequency * var) + corte):

                    mask2[cont] = 0

            pos_mask2 = mask2[:int(len(freqs) / 2)]
            neg_mask2 = mask2[int(len(freqs) / 2): len(freqs)]

            pos_mask2_shifted = shift2(pos_mask2, diff * var)
            neg_mask2_shifted = shift2(neg_mask2, - (diff * var))

            shifted_mask2 = np.concatenate((pos_mask2_shifted, neg_mask2_shifted))

            empty.append(shifted_mask2)

        output = sum(empty)


        adsr_violin = ifft(output)

        maxi = np.amax(adsr_violin)
        normalized = adsr_violin / maxi

        copy = normalized.copy()

        copy[copy < 0] = 0

        suave = smooth(copy.real)

        max_smooth = np.amax(suave)
        suave = suave / max_smooth

        new_time = np.arange(0, len(suave) / sample_rate, 1 / sample_rate)

        fundamental = generate_wave(frequency, suave, sample_rate)

        for v in range(2, harmonics_n + 1):
            sobretono = generate_wave(frequency * v, suave, sample_rate)
            fundamental += partial_amplitudes[v - 2] * sobretono

        out = extend(fundamental, time, duration, sample_rate, form)

        path = '/Users/agustin/Desktop/omegalulsuave.wav'

        write_timeline_to_wav(path, out, sample_rate)

        return fundamental

    elif form == 'flute':
        pass


    elif form == 'piano':
        sample_rate, data = wavfile.read('Wavs/piano-C4.wav')
        harmonics_n = 13
        fundamental_frequency = 261
        corte = 40

        samples = data.shape[0]

        time = np.arange(0, samples / sample_rate, 1 / sample_rate)

        datafft = fft(data)

        freqs = fftfreq(samples, 1 / sample_rate)

        plt.plot(freqs, datafft)
        plt.show()

        pos_freqs = freqs[:int(len(freqs) / 2)]

        index_pos_fundamental = find_nearest(pos_freqs, fundamental_frequency)
        index_pos_target = find_nearest(pos_freqs, frequency)
        diff = index_pos_target - index_pos_fundamental

        mask = np.copy(datafft)
        empty = []


        partial_amplitudes = [927700, 415458, 407031, 49717, 554565, 131549, 196502, 176397, 29992, 12682, 32329, 11866, 71958]

        maximun = 4.4781e6

        for j in range(len(partial_amplitudes)):
            partial_amplitudes[j] = partial_amplitudes[j] / maximun


        for var in range(0, harmonics_n + 2):
            mask2 = np.copy(mask)
            for cont in range(len(freqs)):
                if (freqs[cont] < -(fundamental_frequency * var) - corte) \
                        or (
                        -(fundamental_frequency * var) + corte < freqs[cont] < (fundamental_frequency * var) - corte) \
                        or (freqs[cont] > (fundamental_frequency * var) + corte):
                    mask2[cont] = 0

            pos_mask2 = mask2[:int(len(freqs) / 2)]
            neg_mask2 = mask2[int(len(freqs) / 2): len(freqs)]

            pos_mask2_shifted = shift2(pos_mask2, diff * var)
            neg_mask2_shifted = shift2(neg_mask2, - (diff * var))

            shifted_mask2 = np.concatenate((pos_mask2_shifted, neg_mask2_shifted))

            empty.append(shifted_mask2)

        output = sum(empty)

        adsr_violin = ifft(output)

        plt.plot(time, adsr_violin)
        plt.show()

        maxi = np.amax(adsr_violin)
        normalized = data / maxi

        copy = normalized.copy()

        copy[copy < 0] = 0

        suave = smooth(copy.real)
        for i in range(0, 250):
            suave = smooth(suave)

        max_smooth = np.amax(suave)
        suave = suave / max_smooth

        new_time = np.arange(0, len(suave) / sample_rate, 1 / sample_rate)

        plt.plot(time, copy)
        plt.show()

        plt.plot(new_time, suave)
        plt.show()

        plt.plot(fftfreq(len(suave), 1 / sample_rate), fft(suave))
        plt.show()

        fundamental = generate_wave(frequency, suave, sample_rate)

        for v in range(2, harmonics_n + 1):
            sobretono = generate_wave(frequency * v, suave, sample_rate)
            fundamental += partial_amplitudes[v - 2] * sobretono


        max_fund = np.amax(fundamental)

        fundamental = fundamental / max_fund

        plt.plot(new_time, fundamental)
        plt.show()

        plt.plot(fftfreq(len(fundamental), 1 / sample_rate), fft(fundamental))
        plt.show()

        out = extend(fundamental, time, duration, sample_rate, form)

        out_time = np.arange(0, len(out) / sample_rate, 1 / sample_rate)


        path = '/Users/agustin/Desktop/suenabien.wav'

        write_timeline_to_wav(path, fundamental, sample_rate)

        return fundamental

    elif form == 'trumpet':
        pass


base_adsr('violin', 261, 3)


