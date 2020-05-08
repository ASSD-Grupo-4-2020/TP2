"""
Test con nota Do

"""

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

sonido = synthesize(timbre, frecuencia, 1, 10, sample_rate)

path = '/Users/agustin/Desktop/file.wav'

write_timeline_to_wav(path, sonido, sample_rate)



