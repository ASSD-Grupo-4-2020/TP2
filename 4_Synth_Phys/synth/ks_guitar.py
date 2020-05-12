import numpy as np

class GuitarString:
    def __init__(self, pitch, starting_sample, fs, A, noise_type):
        """Initialize Guitar String"""
        self.pitch = pitch                      # Frecuencia de la nota
        self.starting_sample = starting_sample  # Delay de la nota (cuándo empezar)
        self.fs = fs                            # Frecuencia de Sampleo
#        self.S = S                              # Stretch Factor
        self.A = A                              # Amplitud
        self.noise_type = noise_type            # Tipo de Ruido Inicial
        self.init_wavetable()
        self.curr_sample = 0
        self.prev_value = 0
        
    def init_wavetable(self):
        """Generate new Wavetable for String"""
        # L = int(np.floor(self.fs / int(self.pitch)-1/2/self.S))
        L = int(np.floor(self.fs / int(self.pitch)-1/2))
        if self.noise_type == "normal":
            self.wavetable = (self.A * np.random.normal(0,1,L)).astype(np.float)
        if self.noise_type == "uniform":
            self.wavetable = (self.A * np.random.uniform(-1, 1, L)).astype(np.float)
        if self.noise_type == "2-level":
            self.wavetable = (self.A * 2 * np.random.randint(0, 2, L) - 1).astype(np.float)

    def get_sample(self):
        """Return next sample from string"""
        sample = 0
        if self.curr_sample >= self.starting_sample:
            curr_sample_mod = self.curr_sample % self.wavetable.size
            # stretch = np.random.binomial(1, 1-1/self.S)
            # if stretch == 0: # Hago el promedio entre la muestra y la anterior
            #     self.wavetable[curr_sample_mod] = 0.5 * (self.wavetable[curr_sample_mod] + self.prev_value)
            self.wavetable[curr_sample_mod] = 0.5 * (self.wavetable[curr_sample_mod] + self.prev_value)
            sample = self.wavetable[curr_sample_mod]
            self.prev_value = sample # Tomo el último valor que ingresé a la nueva señal
            self.curr_sample += 1  # Avanzo el índice circularmente
        else:
            self.curr_sample += 1
            sample = 0
        return sample