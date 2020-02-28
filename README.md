# Synthesizer in Python

This is a synthesizer in Python for the piano, organ, acoustic guitar and edm musical instruments. 

## Description
This project is a re-implementation of a synthesizer in Python. More specifically of the Keith William Horwood Audiosynth - JS Dynamic Audio Synth lib, written in Javascript. There are some differences between the two, but the major ones are that my port is not real-time, it generates a wav file. Although, that could be easily changed with the use of a lib like PyAudio. <br> 
I used the Audiosynth library in a previous WebApp project, the [Perfect Pitch Ear](https://github.com/joaocarvalhoopen/Perfect_pitch_ear___Javascript_WebApp), and I liked it. It's a really good library, so I did this project to have a deeper understanding of how the Audiosynth synthesizer worked.

## Example sounds from this synthesizer
* [Piano](./sound_piano.wav)
* [Acoustic Guitar](./sound_acoustic.wav)
* [Organ](./sound_organ.wav)
* [Edm](./sound_edm.wav)

## The original Lib that I used as the base of my port from Javascript to Python
I used the Keith William Horwood, Audiosynth - JS Dynamic Audio Synth lib. <br> 
[Lib Audiosynth - JS Dynamic Audio Synth](https://keithwhor.github.io/audiosynth/) <br>
[Example of the lib usage - Musical Keyboard - JS Dynamic Audio Synth](https://keithwhor.com/music/)

## Dependencies
* This project uses the NumPy library.

## How to use it?

```python
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
```

## License
MIT Open Source license, just like the Audiosynth - JS Dynamic Audio Synth lib. <br>
This work is a re-implementation in Python of that lib. 

## Have fun!
Best regards, <br>
Joao Nuno Carvalho <br>

