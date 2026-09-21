import os
import math
import numpy as np
from PIL import Image

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


def process_folder(input_folder, output_folder, width=256):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename:  # adjust as needed
            binary_path = os.path.join(input_folder, filename)
            image = binary_to_rgb_image(binary_path, width=width)

            # Convert to grayscale image
            img = Image.fromarray(image.astype(np.uint8), mode='L')

            # Optional: Resize to standard CNN input size (e.g., 224x224)
            img = img.resize((224, 224))

            output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".png")
            img.save(output_path)
            print(f"Saved: {output_path}")

if __name__ == "__main__":
    input_folder = "malware_binaries"
    output_folder = "malware_images"
    process_folder(input_folder, output_folder)

