"""

Obtener timbre caracteristico de diferentes instrumentos a partir de la muestra de una nota,
comienzo con un wav de una nota, lo paso a np, analizo en frecuencia, filtro los armonicos, determino asi la adsr

"""

import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq, ifft
from scipy.io import wavfile
from scipy.signal import butter, lfilter
from scipy.signal import savgol_filter

from Additive_Synthesis.waves import generate_wave
from nptowav.numpy_to_wav import write_timeline_to_wav

sample_rate, data = wavfile.read('violin-C4.wav')

samples = data.shape[0]

datafft = fft(data)


fftabs = abs(datafft)

freqs = fftfreq(samples, 1/sample_rate)


positive_freqs = freqs[:int(freqs.size/2)]
positivie_fft = fftabs[:int(freqs.size/2)]


def find_nearest(array, value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return idx - 1
    else:
        return idx


mask = np.copy(datafft)
empty = []


harm = 9
for var in range(2, harm + 2):
    mask2 = np.copy(mask)
    for cont in range(len(freqs)):
        if (freqs[cont] < -(261 * var) - 80) or (-(261 * var) + 80 < freqs[cont] < (261 * var) - 80) or (freqs[cont] > (261 * var) + 80):
            mask2[cont] = 0

    empty.append(mask2)


output = sum(empty)

adsr_violin = ifft(output)

maxi = np.amax(adsr_violin)
normalized = adsr_violin/maxi

plt.plot(normalized.real)
plt.show()

fundamental = generate_wave(261, adsr_violin.real, sample_rate)

for v in range(2, harm + 2):
    sobretono = generate_wave(261 * v, normalized.real, sample_rate)
    fundamental += sobretono

path = '/Users/agustin/Desktop/file_norm.wav'

write_timeline_to_wav(path, fundamental, sample_rate)