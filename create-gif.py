#!/usr/bin/env python3

import os
import argparse
from PIL import Image

def resize_image(image, max_size):
    ratio = max(image.size) / max_size
    new_size = (int(image.size[0] / ratio), int(image.size[1] / ratio))
    return image.resize(new_size, Image.Resampling.LANCZOS)

def create_gif(image_folder, output_gif, duration=500, max_size=None):
    images = []
    for file_name in sorted(os.listdir(image_folder)):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            file_path = os.path.join(image_folder, file_name)
            image = Image.open(file_path).convert('RGB')
            if max_size:
                image = resize_image(image, max_size)
            images.append(image)
    
    if images:
        images[0].save(
            output_gif,
            save_all=True,
            append_images=images[1:],
            duration=duration,
            loop=0
        )
        print(f"Animated GIF saved as {output_gif}")
    else:
        print("No images found in the directory.")

def main():
    parser = argparse.ArgumentParser(description="Create an animated GIF from a directory of images.")
    parser.add_argument('image_folder', type=str, help="Directory containing the images")
    parser.add_argument('output_gif', type=str, help="Output GIF file name")
    parser.add_argument('--duration', type=int, default=500, help="Duration for each frame in milliseconds")
    parser.add_argument('--max_size', type=int, help="Maximum size for the longest axis of the resulting GIF")

    args = parser.parse_args()
    
    create_gif(args.image_folder, args.output_gif, args.duration, args.max_size)

if __name__ == "__main__":
    main()
