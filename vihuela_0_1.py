import numpy as np
import pyaudio
import wave

br = 64000

def genedo(edo,base,rnge=3):
    nfreqs = []
    for n in range(-edo*rnge,edo*rnge):
        nfreqs.append((2**(1/edo))**n*base)
    return nfreqs

def genji(ingens,base,rnge=3):
    nfreqs = []
    for n in range(-rnge,rnge):
        nfreqs.append(base*2**n)
    for gen in ingens:
        ngenf = []
        for nf in nfreqs:
            for n in range(-2,2):
                ngenf.append(nf*gen**n)
        nfreqs += ngenf
    return sorted(list(set(nfreqs)))

print('\nINITIALIZATION\n')
basefreq = input('What base frequency (e.g. \'440\')? ')
edo_ji = input('Equal temperament or just intonation scale (\'edo\'/\'ji\')? ')
if edo_ji == 'edo':
    tet = input('How many divisions per octave? ')
    scal = genedo(int(tet),int(basefreq))
elif edo_ji == 'ji':
    gensstr = ','+input('What generators (use comma to separate, e.g. \'3/2,4/5\')? ')+','
    gsb = []
    for n, gs in enumerate(gensstr):
        if gs == ',':
            gsb.append(n)
    gens = []
    for n in range(len(gsb)-1):
        gens.append(eval(gensstr[gsb[n]+1:gsb[n+1]]))
    scal = genji(gens,440)
    
print('\nMELODY\n')
print('Write a list of notes for a melody, e.g. -1,-1,3,-1,5,5,4,5')
print('The number for each note represents the number of steps from\nthe base note')
melody = np.array((input()).split(',')).astype('int')

print('\nSAVE\n')
savefile = input('What file name to save to (e.g. \'wavcomp.wav\')? ')

signal = ''

for n in melody:
    for t in range(int(br/4)):
        signal += chr(int(np.sin(np.pi*scal[n+int(len(scal)/2)]*t/br)*127+128))        

p = pyaudio.PyAudio()
stream = p.open(format = p.get_format_from_width(1),
                channels = 1,
                rate = br,
                output = True)     
stream.close()
p.terminate()
        
wf = wave.open(savefile, 'wb')
wf.setnchannels(1)
wf.setsampwidth(p.get_sample_size(pyaudio.paInt8))
wf.setframerate(br)
wf.writeframes(bytes(signal,'utf-8'))
wf.close()

print('Save complete!')