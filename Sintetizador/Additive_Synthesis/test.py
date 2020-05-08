"""
Test con nota Do

"""
import numpy as np

from Additive_Synthesis.adsr_envelopes import absolute_adsr
from Additive_Synthesis.timbre import Overtone, Timbre
from Additive_Synthesis.synthesis import synthesize
from nptowav.numpy_to_wav import write_timeline_to_wav

frecuencia = 261.63
sample_rate = 44100

#sobretono1 = Overtone(2, 0.2, absolute_adsr)
#sobretono2 = Overtone(3, 0.1, absolute_adsr)
#sobretono3 = Overtone(4, 0.05, absolute_adsr)

#lista_sobretonos = [sobretono1, sobretono2, sobretono3]

timbre = Timbre(absolute_adsr, [])

sonido = synthesize(timbre, frecuencia, 1, 4, sample_rate)
sonido2 = synthesize(timbre, frecuencia + 1, 1, 5, sample_rate)

data = np.concatenate((sonido, sonido2))

path = '/Users/agustin/Desktop/file.wav'

write_timeline_to_wav(path, data, sample_rate)



