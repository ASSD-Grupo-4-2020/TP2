"""
Test con nota Do

"""
import numpy as np

from Additive_Synthesis.adsr_envelopes import absolute_adsr, relative_adsr
from Additive_Synthesis.timbre import Overtone, Timbre
from Additive_Synthesis.synthesis import synthesize
from nptowav.numpy_to_wav import write_timeline_to_wav

frecuencia = 261
sample_rate = 11025


sobretono1 = Overtone(2, 0.278, relative_adsr)
sobretono2 = Overtone(3, 0.1045, relative_adsr)
sobretono3 = Overtone(4, 0.087, relative_adsr)
sobretono4 = Overtone(4, 0.076, relative_adsr)

lista_sobretonos = [sobretono1, sobretono2, sobretono3, sobretono4]

timbre = Timbre(relative_adsr, lista_sobretonos)

sonido = synthesize(timbre, frecuencia, 1, 2, sample_rate)


path = '/Users/agustin/Desktop/niu.wav'


write_timeline_to_wav(path, sonido, sample_rate)