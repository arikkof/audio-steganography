Introduction
---
This little project aims to be a first attempt at 'Least Significant Bit' Audio Steganography.
It uses Python and its ```wave``` package to read and write bytes from and to audio files from disk. 

Currently supported media: 
- raw uncompressed audio (tested with .wav)
- plain text (ASCII characters) (tested with .txt)

The repository features an example audio file in the ```audio```folder and a simple text file in the ```text``` folder. Both of these files are currently specified to be used in the scripts.

Usage 
---
```encoder.py``` allows you to specify paths to your audio and text file and the audio-file containing the embedded message, which shall be saved to disk.

```decoder.py``` allows you to specify the path to the audio file, from which the message shall be extracted and the location and name of the file to which the extracted message shall be saved. 
The message is also printed to console but bear in mind that for large amounts of data the console's output might not suffice to display the whole message.

