import numpy as np

def karplus_strong_drum(wavetable, n_samples, stretch_factor, probability):
    samples = [] 
    # Condiciones Iniciales:
    curr_sample = 0 # Índice para recorrer la tabla de onda
    prev_value = 0  # Valor anterior
    while len(samples) < n_samples: # Recorro hasta que retorno tenga mismo largo
        stretch = np.random.binomial(1, 1/stretch_factor)
        drum_sign = np.random.binomial(1,probability)
        
        if stretch == 1: # Decido si estiro con prob 1/S
            wavetable[curr_sample] = 0.5 * (wavetable[curr_sample] + prev_value)
        if drum_sign == 0: # Decido si invierto el signo con prob b
            wavetable[curr_sample] = -wavetable[curr_sample]
        
        samples.append(wavetable[curr_sample])
        prev_value = samples[-1]    # Tomo el último valor que ingresé a la nueva señal
        curr_sample = (curr_sample+1) % wavetable.size  # Avanzo el índice circularmente
    return np.array(samples)

class DrumString:
    def __init__(self, pitch, fs, A, S, T, b):
        """Initialize Drum String"""
        self.pitch = pitch                      # Frecuencia de la nota
        self.fs = fs                            # Frecuencia de Sampleo
        self.T = T                              # Duración de la nota (samples)
        self.S = 1                              # Stretch Factor
        self.A = A                              # Amplitud
        self.b = b
        self.init_wavetable()
        self.init_samples()
    def init_wavetable(self):  #Se puede usar la constante de Amplitud para el tambor
        self.L = int(np.floor(self.fs / int(self.pitch)-1/2/self.S))
        self.wavetable = np.full(self.L,self.A)
    def init_samples(self):
        """Create sound samples for string"""
        self.samples = karplus_strong_drum(self.wavetable, self.T, self.S, self.b)
        
    def get_samples(self):
        """Return Sound Samples"""
        return self.samples