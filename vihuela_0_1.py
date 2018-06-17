import numpy as np
import pyaudio
import wave

br = 64000

def genwave(afs,lenwav):
    outsig = np.zeros(lenwav)
    for ampfreq in afs:
        outsig += ampfreq[0]*np.sin((np.arange(lenwav))/((br/ampfreq[1])/np.pi))
        #outsig += ampfreq[0]*np.sin(np.pi*scal[n+int(len(scal)/2)]*t/br)
    return outsig

def envwave(inwav):
    fadein = int(len(inwav)/10)
    fadeout = int(len(inwav)/5)
    for n in range(fadein):
        inwav[n] = n/fadein*inwav[n]
    for n in range(fadeout):
        inwav[-n] = n/fadeout*inwav[-n]
    return inwav

def instr1(infreq):
    a1 = [(2/3,infreq)]
    rems = 1/3
    for n in range(2,7):
        a1.append((rems/3,infreq*n))
        a1.append((rems/3,infreq/n))
        rems = rems/3
    return a1

def instr2(infreq):
    a1 = [(1/3,infreq)]
    a1.append((1/9,infreq+.0003))
    a1.append((1/9,infreq-.0003))
    rems = 1/2
    for n in range(2,10):
        a1.append((rems/n**2,infreq*n))
    a1.append((1/8,infreq/2))
    return a1

def null_instr(infreq):
    return [(1,infreq)]

def chor1(afs,offset=.003):
    afso = []
    for ampfreq in afs:
        afso.append((ampfreq[0]/3,ampfreq[1]))
        afso.append((ampfreq[0]/3,ampfreq[1]*(1+offset)))
        afso.append((ampfreq[0]/3,ampfreq[1]*(1-offset)))
    return afso

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
    abc = envwave(genwave(chor1((instr2(scal[n+int(len(scal)/2)]))),int(br/4)))
    for k in abc:
        signal +=  chr(int(k*127+128))

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