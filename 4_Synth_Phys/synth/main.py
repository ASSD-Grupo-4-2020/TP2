import numpy as np
import scipy as sp

def make_wavetable(n_samples, amps, phases, freqs):
    #Generate Wavetable
    t = np.linspace(0, 1, num=n_samples)
    wavetable = np.zeros_like(t)
    for amp, phase, freq in zip(amps,phases,freqs):
        wavetable += amp+ np.sin(np.sin(2*np.pi*2*freq*t + phase))
    return wavetable