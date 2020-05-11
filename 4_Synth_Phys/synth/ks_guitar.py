import numpy as np

class GuitarString:
    def __init__(self, pitch, starting_sample, fs, S):
        """Initialize Guitar String"""
        self.pitch = pitch
        self.starting_sample = starting_sample
        self.fs = fs
        self.S = S
        self.init_wavetable()
        self.curr_sample = 0
        self.prev_value = 0

    def init_wavetable(self):
        """Generate new Wavetable for String"""
        L = self.fs // int(self.pitch)
        self.wavetable = (2 * np.random.randint(0, 2, L) - 1).astype(np.float)

    def get_sample(self):
        """Return next sample from string"""
        sample = 0
        if self.curr_sample >= self.starting_sample:
            curr_sample_mod = self.curr_sample % self.wavetable.size
            stretch = np.random.binomial(1, 1-1/self.S)
            if stretch == 0: # Hago el promedio entre la muestra y la anterior
                self.wavetable[curr_sample_mod] = 0.5 * (self.wavetable[curr_sample_mod] + self.prev_value)
            sample = self.wavetable[curr_sample_mod]
            self.prev_value = sample # Tomo el último valor que ingresé a la nueva señal
            self.curr_sample += 1  # Avanzo el índice circularmente
        else:
            self.curr_sample += 1
            sample = 0
        return sample