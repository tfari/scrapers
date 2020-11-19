### oeis_midi_downloader

The [Online Encyclopedia of Integer Sequences](https://oeis.org/), provides midi representation of its stored sequences.
<br/>

This script bulk downloads ranges of them, and allows to determine the desired BPM and sequence length of the midis.

To set the preferred output path for the files, edit the OUTPUT_PATH field in settings.json (./output by default.)

(Settings file gets created first time the script runs.)

**Requirements:**
- requests
- bs4

**Usage:**
```
python oeis_md.py MIN_RANGE MAX_RANGE NUM_THREDS | BPMS SEQ_LENGTH
```
BPMs and SEQ_LENGTH are optional parameters, they default to 100 and 4096 respectively.

**Example:**
```
python oeis_md.py 100 1230 10 100 16
```
Downloads all the sequences between (and including) the ranges of 100 and 1230 distributing work among 10 threads. 
<br/>

The resulting .mid files are produced with a BPM of 100, and the file is limited to 16 steps, representing the first
16 numbers of the sequence.

