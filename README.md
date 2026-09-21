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

Both scripts take the same options and run in one of two modes:

| Option | Mode | Meaning |
| --- | --- | --- |
| `-i`, `--input FILE` | single file | binary file to convert |
| `-o`, `--output FILE` | single file | file to write (parent folders are created) |
| `-I`, `--input-dir DIR` | folder | convert every file in this folder (subfolders are skipped) |
| `-O`, `--output-dir DIR` | folder | folder to save the converted files into (created if missing) |

`--input` and `--output` must be given together, as must `--input-dir` and
`--output-dir`, and the two modes can't be combined. With no options, folder
mode runs on the defaults: `malware_binaries/` in, `malware_images/` or
`malware_tone_audio/` out.

### Binary to image

```bash
# one file
python binary_to_image.py -i malware_binaries/ls -o out/ls.png

# every file in a folder
python binary_to_image.py -I malware_binaries -O out/images
```

Each file's bytes are laid out as pixel rows (width 256, zero-padded), then
resized to 224x224 and saved as a grayscale PNG. In folder mode each output is
named after its input with a `.png` extension.

### Binary to audio

```bash
# one file
python binary_to_audio.py -i malware_binaries/ls -o out/ls.wav

# every file in a folder
python binary_to_audio.py -I malware_binaries -O out/audio
```

Each byte is mapped to a tone between C4 (261.63 Hz) and C7 (2093 Hz), played
for 50 ms. Only the first 1000 bytes of each file are used, and the result is
saved as a WAV. In folder mode each output is named `<input name>_tones.wav`.

Other parameters (image width, tone duration, sample rate, max bytes) are still
set in the code.

## Sample data

`malware_binaries/ls` is a copy of the standard `ls` binary, included as a
harmless example along with its generated outputs.
