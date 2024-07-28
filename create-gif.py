#!/usr/bin/env python3

import os
import re
import argparse
from PIL import Image, ImageOps
from moviepy.editor import ImageSequenceClip
import numpy as np
from natsort import natsorted

def resize_and_pad_image(image, target_size):
    """
    Resize an image while maintaining aspect ratio and pad it to the target size.
    """
    image.thumbnail(target_size, Image.Resampling.LANCZOS)
    delta_w = target_size[0] - image.size[0]
    delta_h = target_size[1] - image.size[1]
    padding = (delta_w // 2, delta_h // 2, delta_w - (delta_w // 2), delta_h - (delta_h // 2))
    return ImageOps.expand(image, padding)

def create_gif(image_folder, output_gif, duration=500, max_size=None, regex_pattern=None, loop=False, skip=0):
    images = []
    pattern = re.compile(regex_pattern) if regex_pattern else None

    file_names = natsorted(os.listdir(image_folder))

    for file_name in file_names[skip:]:
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            if pattern and not pattern.match(file_name):
                continue
            file_path = os.path.join(image_folder, file_name)
            image = Image.open(file_path).convert('RGB')
            if max_size:
                target_size = (max_size, max_size)
                image = resize_and_pad_image(image, target_size)
            images.append(image)
    
    if images:
        first_image_size = images[0].size

        save_kwargs = {
            'save_all': True,
            'append_images': images[1:],
            'duration': duration,
        }
        
        if loop:
            save_kwargs['loop'] = 0  # Infinite loop if --loop flag is provided

        # Debug print statements
        print(f"Saving GIF with the following parameters:")
        print(f"output_gif: {output_gif}")
        print(f"save_all: {save_kwargs['save_all']}")
        print(f"append_images: {[f'Image {i}' for i in range(1, len(images))]}")
        print(f"duration: {save_kwargs['duration']}")
        print(f"loop: {save_kwargs.get('loop', 'Not set')}")

        images[0].save(output_gif, **save_kwargs)
        print(f"Animated GIF saved as {output_gif}")
    else:
        print("No images found in the directory matching the criteria.")
    
    return images

def create_mp4(images, output_mp4, duration):
    frame_duration = duration / 1000.0  # Convert milliseconds to seconds
    numpy_images = [np.array(image) for image in images]  # Convert PIL images to NumPy arrays
    clip = ImageSequenceClip(numpy_images, fps=1/frame_duration)
    clip.write_videofile(output_mp4, codec='libx264')
    print(f"MP4 video saved as {output_mp4}")

def main():
    parser = argparse.ArgumentParser(description="Create an animated GIF and a video (MP4) from a directory of images.")
    parser.add_argument('image_folder', type=str, help="Directory containing the images")
    parser.add_argument('output_gif', type=str, help="Output GIF file name")
    parser.add_argument('--output_mp4', type=str, help="Output MP4 file name", default=None)
    parser.add_argument('--duration', type=int, default=500, help="Duration for each frame in milliseconds")
    parser.add_argument('--max_size', type=int, help="Maximum size for the longest axis of the resulting GIF")
    parser.add_argument('--regex', type=str, help="Regular expression to filter image files")
    parser.add_argument('--loop', action='store_true', help="Specify this flag to make the GIF loop")
    parser.add_argument('--skip', type=int, default=0, help="Number of initial images to skip")

    args = parser.parse_args()
    
    images = create_gif(args.image_folder, args.output_gif, args.duration, args.max_size, args.regex, args.loop, args.skip)

    if args.output_mp4:
        create_mp4(images, args.output_mp4, args.duration)

if __name__ == "__main__":
    main()
