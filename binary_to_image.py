import argparse
import os
import math
import numpy as np
from PIL import Image

from cli_helpers import add_io_arguments, make_parent_dir, resolve_io

def binary_to_image(binary_path, width=256):
    # Read the binary file as bytes
    with open(binary_path, 'rb') as f:
        byte_data = f.read()

    # Convert bytes to uint8 array
    byte_arr = np.frombuffer(byte_data, dtype=np.uint8)

    # Calculate required height
    length = len(byte_arr)
    height = math.ceil(length / width)

    # Pad byte array to match target shape
    padded_len = height * width
    padded_byte_arr = np.pad(byte_arr, (0, padded_len - length), 'constant', constant_values=0)

    # Reshape to 2D image
    image = padded_byte_arr.reshape((height, width))

    return image

def binary_to_rgb_image(binary_path, width=256):
    with open(binary_path, 'rb') as f:
        byte_data = f.read()

    byte_arr = np.frombuffer(byte_data, dtype=np.uint8)

    # Ensure total length is divisible by 3
    padded_len = int(np.ceil(len(byte_arr) / 3)) * 3
    byte_arr = np.pad(byte_arr, (0, padded_len - len(byte_arr)), 'constant', constant_values=0)

    rgb_arr = byte_arr.reshape(-1, 3)

    # Calculate image dimensions
    height = int(np.ceil(len(rgb_arr) / width))
    padded_rgb = np.pad(rgb_arr, ((0, height * width - len(rgb_arr)), (0, 0)), 'constant', constant_values=0)

    image = padded_rgb.reshape((height, width, 3))
    return image


def process_file(input_path, output_path, width=256):
    make_parent_dir(output_path)
    image = binary_to_image(input_path, width=width)

    # Convert to grayscale image
    img = Image.fromarray(image.astype(np.uint8))

    # Optional: Resize to standard CNN input size (e.g., 224x224)
    img = img.resize((224, 224))

    img.save(output_path)
    print(f"Saved: {output_path}")


def process_folder(input_folder, output_folder, width=256):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in sorted(os.listdir(input_folder)):
        binary_path = os.path.join(input_folder, filename)
        if not os.path.isfile(binary_path):
            continue
        output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".png")
        process_file(binary_path, output_path, width=width)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert binary files into grayscale PNG images.")
    add_io_arguments(parser)
    args = parser.parse_args()

    mode, input_path, output_path = resolve_io(parser, args, "malware_binaries", "malware_images")
    if mode == "file":
        process_file(input_path, output_path)
    else:
        process_folder(input_path, output_path)

