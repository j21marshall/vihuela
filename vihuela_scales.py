import numpy as np
from tempfile import NamedTemporaryFile
import subprocess
from pydub import AudioSegment

def play_ffplay(sgmt):
    with NamedTemporaryFile("w+b", suffix=".wav") as f:
        f.close()
        sgmt.export(f.name, "wav")
        subprocess.call(["ffplay", "-nodisp", "-autoexit", "-hide_banner", f.name])
        
def play_note(sample, frac_mult, play=True):
    new_sample_rate = int(frac_mult * sample.frame_rate)
    pitch_sound = sample._spawn(sample.raw_data, overrides={'frame_rate': new_sample_rate})
    ls = pitch_sound
    if play:
        play_ffplay(ls)
    return ls

def play_chord(sample, *fracs, play=True):
    chord = play_note(sample, fracs[0], play=False)
    for fr in fracs[1:]:
        chord = chord.overlay( play_note(sample, fr, play=False) )
    if play:
        play_ffplay(chord)
    return chord

class scale:
    def __init__(self, base_freq=440):
        self.base_freq = base_freq
    
class edo_scale(scale):
    def __init__(self, edo, base_freq=440, return_as_freq=True):
        self.base_freq = base_freq
        self.edo = edo
        scale.__init__(self, base_freq)
        self.return_as_freq = return_as_freq

    def __getitem__(self, note):
        return (2**(1/self.edo))**note * (self.base_freq if self.return_as_freq else 1)

class ji_scale(scale):
    def __init__(self, *gens, base_freq=440, return_as_freq=True):
        self.base_freq = base_freq
        self.gens = list(gens)
        scale.__init__(self, base_freq)
        self.return_as_freq = return_as_freq
        
    def __getitem__(self, gen_inds):
        if len(gen_inds) != len(self.gens):
            raise Exception('Wrong number of indices provided for just intonation scale')
        if self.return_as_freq:
            note_freq = self.base_freq
        else:
            note_freq = 1
        for i in range(len(self.gens)):
            note_freq = note_freq * self.gens[i]**gen_inds[i]
        return note_freq
