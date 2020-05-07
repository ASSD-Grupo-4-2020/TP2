"""

Genero las envolventes ADSR para cada nota


"""

import numpy as np
from math import ceil

def absolute_adsr(duration, sample_rate, attack_time, decay_time, sustain_level, release_time):
    """
    :param duration:
         duracion del sonido en segundos
    :param sample_rate:
        muestras por segundo
    :param attack_time:
        tiempo de ataque máximo en segundos
    :param decay_time:
        tiempo de decaimiento máximo en segundos
    :param sustain_level:
        volumen en la etapa de sostenido del sonido, 1 es el máximo
    :param release_time:
        tiempo de finalizacion máximo
    :return:
        envolvente en un arreglo numpy n-dimensional
    """

    timepoints = ceil(duration * sample_rate)

    max_tmpts_attack = int(round(attack_time * sample_rate))
    max_tmpts_decay = int(round(decay_time * sample_rate))
    max_tmpts_release = int(round(release_time * sample_rate))

    adr_duration_in_tmpts = (max_tmpts_attack + max_tmpts_decay + max_tmpts_release)
    sustain_duration_in_tmpts = timepoints - adr_duration_in_tmpts

    if max_tmpts_attack > 0:
        step = 1 / max_tmpts_attack
        attack = np.arange(0, 1, step)
    else:
        attack = np.array([])

    if max_tmpts_decay > 0:
        step = (1 - sustain_level) / max_tmpts_decay
        decay = np.arange(1, sustain_level, -step)
    else:
        decay = np.array([])

    if max_tmpts_release > 0:
        step = sustain_level / max_tmpts_release
        release = np.arange(sustain_level, 0, -step)
    else:
        release = np.array([])

    tmpts_with_sustain = (timepoints - len(attack) - len(decay) - len(release))
    sustain = sustain_level * np.ones(tmpts_with_sustain)

    envelope = np.concatenate((attack, decay, sustain, release))

    return envelope
