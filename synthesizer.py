###############################################################################
#
#                            Synthesizer in Python
#
#    This is a synthesizer in Python for the piano, organ, acoustic guitar 
#                       and edm musical instruments. 
###############################################################################
# Author of this re-implementation / port: Joao Nuno Carvalho
#
# Date: 2020.02.28 
#
# Description: This project is a re-implementation of a synthesizer in Python.
#              More specifically of the Keith William Horwood Audiosynth - JS
#              Dynamic Audio Synth lib, written in Javascript. There are some
# differences between the two, but the major ones are that my port is not 
# real-time, it generates a wav file. Although, that could be easily changed
# with the use of a lib like PyAudio. 
# I used the Audiosynth in Javascript in a previous WebApp project, 
# the [Perfect Pitch Ear]
# (https://github.com/joaocarvalhoopen/Perfect_pitch_ear___Javascript_WebApp),
# and I liked it, it's a really good library, so I did this project to have
# a deeper understanding of how the Audiosynth synthesizer worked.
#
# Example sounds from this synthesizer
#    [Piano](./sound_piano.wav)
#    [Acoustic Guitar](./sound_acoustic.wav)
#    [Organ](./sound_organ.wav)
#    [Edm](./sound_edm.wav)
#
# The original Lib that I used as the base of my port from Javascript to Python
# I used the Keith William Horwood, Audiosynth - JS Dynamic Audio Synth lib.  
# [Lib Audiosynth - JS Dynamic Audio Synth](https://keithwhor.github.io/audiosynth/) 
# [Example of the lib usage - Musical Keyboard - JS Dynamic Audio Synth](https://keithwhor.com/music/)
#
# Dependencies: This project uses the NumPy library.
#
# License: MIT Open Source license, just like the Audiosynth - JS Dynamic Audio
#          Synth lib. This work is a re-implementation in Python of that lib. 
#
# For more details see the project page.
#
###############################################################################

import numpy as np
import math
import random
import wave

bitsPerSample = 16
channels = 1
sampleRate = 44100
volume = 32768
notesDic = {'C':261.63,
            'C#':277.18,
            'D':293.66,
            'D#':311.13,
            'E':329.63,
            'F':349.23,
            'F#':369.99,
            'G':392.00,
            'G#':415.30,
            'A':440.00,
            'A#':466.16,
            'B':493.88}

def writeArrayToWavFilename(signalArray, sampleFreq, destinationWavFilename):
    # Converts the NumPy contiguous array into frames to be written into the file.
    # From range [-1, 1] to -/+ 2^15 , 16 bits signed
    signalTemp = np.zeros(len(signalArray), np.int16)
    for i in range(0, len(signalTemp)):
        # signalTemp[i] = int( signalArray[i] * (2.0**15) )
        signalTemp[i] = int( signalArray[i] )   # Data already in a float of 16bit unsigned range.

    # Convert float64 into Int16.
    # This means that the sound pressure values are mapped to integer values that can range from -2^15 to (2^15)-1.
    numFrames = signalTemp.tostring()

    # Write file from harddisc.
    wavHandler = wave.open(destinationWavFilename,'wb') # Write only.
    wavHandler.setnframes(len(signalArray))
    wavHandler.setframerate(sampleFreq)
    wavHandler.setnchannels(1)
    wavHandler.setsampwidth(2) # 2 bytes
    wavHandler.writeframes(numFrames)

def modulationFunc_0(i, sampleRate, frequency, x):
    return 1 * math.sin(2 * math.pi * ((i / sampleRate) * frequency) + x)

def modulationFunc_1(i, sampleRate, frequency, x):
    return 1 * math.sin(4 * math.pi * ((i / sampleRate) * frequency) + x)

def modulationFunc_2(i, sampleRate, frequency, x):
    return 1 * math.sin(8 * math.pi * ((i / sampleRate) * frequency) + x)

def modulationFunc_3(i, sampleRate, frequency, x):
    return 1 * math.sin(0.5 * math.pi * ((i / sampleRate) * frequency) + x)

def modulationFunc_4(i, sampleRate, frequency, x):
    return 1 * math.sin(0.25 * math.pi * ((i / sampleRate) * frequency) + x)

def modulationFunc_5(i, sampleRate, frequency, x):
    return 0.5 * math.sin(2 * math.pi * ((i / sampleRate) * frequency) + x)

def modulationFunc_6(i, sampleRate, frequency, x):
    return 0.5 * math.sin(4 * math.pi * ((i / sampleRate) * frequency) + x)

def modulationFunc_7(i, sampleRate, frequency, x):
    return 0.5 * math.sin(8 * math.pi * ((i / sampleRate) * frequency) + x)

def modulationFunc_8(i, sampleRate, frequency, x):
    return 0.5 * math.sin(0.5 * math.pi * ((i / sampleRate) * frequency) + x)

def modulationFunc_9(i, sampleRate, frequency, x):
    return 0.5 * math.sin(0.25 * math.pi * ((i / sampleRate) * frequency) + x)

modulationFunc = [modulationFunc_0,
                  modulationFunc_1,
                  modulationFunc_2,
                  modulationFunc_3,
                  modulationFunc_4,
                  modulationFunc_5,
                  modulationFunc_6,
                  modulationFunc_7,
                  modulationFunc_8,
                  modulationFunc_9]

def generate(sound, note, octave, duration):
    if sound not in soundsList:
        print("Error: Invalid sound " + sound)
        return None
    if note not in notesDic:
        print(note + " is not a valid note.")
        return None
    length = math.ceil(duration * sampleRate)
    time = duration
    data = np.zeros(length)
    if octave < 1:
        octave = 1
    elif octave > 8:
        octave = 8 

    # Initialize the global table for the acoustic instrument.
    acousticInit()

    soundDic  = soundsList[sound]

    frequency = notesDic[note] * math.pow(2, octave - 4)
    attack    = soundDic['attack']()
    dampen    = soundDic['dampen'](sampleRate, frequency, volume)
    waveFunc  = soundDic['wave']

    val = 0
    attackLen = math.floor(sampleRate * attack)
    decayLen = math.floor(sampleRate * time)

    # print("attackLen: " + str(attackLen))
    # print("decayLen: " + str(decayLen))

    lastIndex = 0
    for i  in range(0, attackLen):
        val = volume * (i/(sampleRate*attack)) * waveFunc(i, sampleRate, frequency, volume)
        data[i] = val
        lastIndex = i

    for i in range(lastIndex + 1, decayLen):
        val = volume * math.pow((1-((i-(sampleRate*attack))/(sampleRate*(time-attack)))),dampen) * waveFunc(i, sampleRate, frequency, volume)
        data[i] = val

    return data


soundsList = {}

##############
# Piano sound
##############

def pianoAttack():
    return 0.002

def pianoDampen(sampleRate, frequency, volume):
    return math.pow(0.5*math.log((frequency*volume)/sampleRate),2)
	
def pianoWave(i, sampleRate, frequency, volume):
    base = modulationFunc[0]
    return modulationFunc[1](
			i,
			sampleRate,
			frequency,
			math.pow(base(i, sampleRate, frequency, 0), 2) +
				(0.75 * base(i, sampleRate, frequency, 0.25)) +
				(0.1 * base(i, sampleRate, frequency, 0.5))
		    )

pianoSoundDic = {"name" : "piano",
                 "attack": pianoAttack,
                 "dampen": pianoDampen,
                 "wave"  : pianoWave }

soundsList["piano"] = pianoSoundDic

##############
# Organ sound
##############

def organAttack():
    return 0.03

def organDampen(sampleRate, frequency, volume):
    return 1+(frequency * 0.01)
	
def organWave(i, sampleRate, frequency, volume):
    base = modulationFunc[0]
    return modulationFunc[1](
			i,
			sampleRate,
			frequency,
			base(i, sampleRate, frequency, 0) +
				0.5*base(i, sampleRate, frequency, 0.25) +
				0.25*base(i, sampleRate, frequency, 0.5)
            )

organSoundDic = {"name" : "organ",
                 "attack": organAttack,
                 "dampen": organDampen,
                 "wave"  : organWave }

soundsList["organ"] = organSoundDic

################
# Acoustic sound
################

def acousticAttack():
    return 0.002

def acousticDampen(sampleRate, frequency, volume):
    return 1

valueTable  = []
playVal     = 0
periodCount = 0	

def acousticInit():
    global valueTable
    global playVal
    global periodCount	

    valueTable  = []
    playVal     = 0
    periodCount = 0	

def acousticWave(i, sampleRate, frequency, volume):
    global valueTable
    global playVal
    global periodCount	
 
    period = sampleRate / frequency
    p_hundredth = math.floor((period - math.floor(period)) * 100)
    resetPlay = False
    if(len(valueTable) <= math.ceil(period)):	
        valueTable.append(round(random.random()) * 2 - 1)
        return valueTable[len(valueTable) - 1]
    else:
        valueTmp = 0
        if (playVal >= len(valueTable) -1):
            valueTmp = 0
        else:
            valueTmp = playVal + 1
        valueTable[playVal] = (valueTable[valueTmp] + valueTable[playVal]) * 0.5
        if(playVal >= math.floor(period)):
            if(playVal < math.ceil(period)):
                if((periodCount % 100) >= p_hundredth):
                    # Reset
                    resetPlay = True
                    valueTable[playVal + 1] = (valueTable[0] + valueTable[playVal + 1]) * 0.5
                    periodCount += 1	
            else:
                resetPlay = True	
        _return = valueTable[playVal]
        if(resetPlay):
            playVal = 0
        else:
            playVal += 1
        return _return

acousticSoundDic = {"name"  : "acoustic",
                    "attack": acousticAttack,
                    "dampen": acousticDampen,
                    "wave"  : acousticWave }

soundsList["acoustic"] = acousticSoundDic

##############
# Edm sound
##############

def edmAttack():
    return 0.002

def edmDampen(sampleRate, frequency, volume):
    return 1
	
def edmWave(i, sampleRate, frequency, volume):
    base = modulationFunc[0]
    mod  = modulationFunc[1:]
    return mod[0](
            i,
            sampleRate,
            frequency,
            mod[6]( # 9 Changed from modulation 9 to modulation 6 (they were shifted one pos).
                i,
                sampleRate,
                frequency,
                mod[2](
                    i,
                    sampleRate,
                    frequency,
                    math.pow(base(i, sampleRate, frequency, 0), 3) +
                        math.pow(base(i, sampleRate, frequency, 0.5), 5) +
                        math.pow(base(i, sampleRate, frequency, 1), 7)
                    )
                ) +
            mod[8](
                i,
                sampleRate,
                frequency,
                base(i, sampleRate, frequency, 1.75)
                )
            )

edmSoundDic = {"name" : "edm",
               "attack": edmAttack,
               "dampen": edmDampen,
               "wave"  : edmWave }

soundsList["edm"] = edmSoundDic

##############
# Test 
##############

if __name__ == "__main__":
    p_sounds = ["piano", "organ", "acoustic", "edm"]
    p_octave  = 4
    p_duration = 3.0  # Seconds 

    for p_sound in p_sounds: 
        signal_a = generate(p_sound, "C", p_octave, p_duration)
        signal_b = generate(p_sound, "D", p_octave, p_duration)
        signal_c = generate(p_sound, "E", p_octave, p_duration)
        p_signalArray = np.hstack((signal_a, signal_b, signal_c))
        p_destinationWavFilename = "sound_" + p_sound + ".wav"
        writeArrayToWavFilename(p_signalArray, sampleRate, p_destinationWavFilename)



