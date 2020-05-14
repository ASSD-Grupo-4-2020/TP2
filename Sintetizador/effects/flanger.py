import numpy as np

def gen_delay(data, delay):
    out = data.copy()
    for i in range(len(data)):
        index = int(i - delay)
        if index >= 0 and index < len(data):
            out[i] = data[index]
    return out

def flange(data, lfofreq, depth, M0=1, A=1):
    """ lfofreq: Flanger Speed (samples/sec)
        depth = Degree of Flanging Effect range=[0;1]"""
    out = data.copy()
    for i in range(len(data)):
        delay = M0*(1 + A*np.sin(2*np.pi*lfofreq*i))
        index = int(i - delay)
        if index >= 0 and index < len(data):
            out[i] = data[i] + depth * data[index]
    return out