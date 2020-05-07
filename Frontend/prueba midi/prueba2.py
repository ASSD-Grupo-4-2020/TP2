from midi2audio import FluidSynth

fs = FluidSynth()
fs.midi_to_audio('dancing_queen.mid', 'output.wav')