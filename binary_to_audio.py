import os
import numpy as np
import wave
import struct
from scipy.io.wavfile import write as write_wav

# Byte to frequency mapping (like MIDI notes 40–100)
def byte_to_freq(byte_val, low=261.63, high=2093.0):  # C4 to C7
    return low + ((high - low) * byte_val / 255)

def generate_tone(freq, duration=0.05, sample_rate=8000):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    waveform = 0.5 * np.sin(2 * np.pi * freq * t)
    return waveform

def binary_to_audio_wave(byte_arr, tone_duration=0.05, sample_rate=8000, max_len=1000):
    samples = []
    for byte in byte_arr[:max_len]:
        freq = byte_to_freq(byte)
        tone = generate_tone(freq, duration=tone_duration, sample_rate=sample_rate)
        samples.append(tone)
    return np.concatenate(samples)

def process_folder_to_musical_audio(input_folder, output_folder, sample_rate=8000, tone_duration=0.05, max_bytes=1000):
    os.makedirs(output_folder, exist_ok=True)

    for fname in os.listdir(input_folder):

        path = os.path.join(input_folder, fname)
        with open(path, 'rb') as f:
            byte_data = f.read()

        byte_arr = np.frombuffer(byte_data, dtype=np.uint8)
        audio = binary_to_audio_wave(byte_arr, tone_duration=tone_duration, sample_rate=sample_rate, max_len=max_bytes)
        audio_int16 = np.int16(audio * 32767)

        out_name = os.path.splitext(fname)[0] + "_tones.wav"
        out_path = os.path.join(output_folder, out_name)

        write_wav(out_path, sample_rate, audio_int16)
        print(f"Saved musical audio: {out_path}")

if __name__ == "__main__":
    process_folder_to_musical_audio(
        input_folder="malware_binaries",
        output_folder="malware_tone_audio",
        sample_rate=8000,
        tone_duration=0.05,  # 50ms per byte
        max_bytes=1000       # keep short for listenability
    )

