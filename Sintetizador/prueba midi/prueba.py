import mido

mid = mido.MidiFile()

track = mido.MidiTrack()

mid.tracks.append(track)

track.append(mido.MetaMessage('set_tempo', tempo=500000, time=0))

track.append(mido.Message('program_change', channel=0, program=1, time=0))

track.append(mido.Message('control_change', channel=0, control=4, value=80, time=0))

track.append(mido.Message('note_on', channel=0, note=60, velocity=100, time=0))

track.append(mido.Message('note_on', channel=0, note=62, velocity=100, time=1000))
track.append(mido.Message('note_on', channel=0, note=64, velocity=100, time=1000))
track.append(mido.Message('note_on', channel=0, note=65, velocity=100, time=1000))
track.append(mido.Message('note_on', channel=0, note=67, velocity=100, time=1000))
track.append(mido.Message('note_on', channel=0, note=69, velocity=100, time=1000))
track.append(mido.Message('note_on', channel=0, note=71, velocity=100, time=1000))




mid.save('prueba.mid')