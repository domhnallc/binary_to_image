# binary_to_image

Convert binary files (e.g. malware samples) into images and audio, for use in
visual/audio analysis or as input to CNN-based classifiers.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

Both scripts read every file in `malware_binaries/` and write results to a
sibling output folder. Run them from the repo root.

### Binary to image

```bash
python binary_to_image.py
```

Each file's bytes are laid out as pixel rows (width 256, zero-padded), then
resized to 224x224 and saved as a grayscale PNG in `malware_images/`.

### Binary to audio

```bash
python binary_to_audio.py
```

Each byte is mapped to a tone between C4 (261.63 Hz) and C7 (2093 Hz), played
for 50 ms. Only the first 1000 bytes of each file are used, and the result is
saved as a WAV in `malware_tone_audio/`.

Parameters (image width, tone duration, sample rate, max bytes) are set at the
bottom of each script.

## Sample data

`malware_binaries/ls` is a copy of the standard `ls` binary, included as a
harmless example along with its generated outputs.
