import numpy as np
import os
import sys

import converter
import display

arg = sys.argv[1]

def get_images_from_dir(dir_path: str) -> np.array:
    image_list = []

    for image_name in os.listdir(dir_path):
        image_path = os.path.join(dir_path, image_name)

        image_list.append(converter.open_pgm_in_rgb_ppm(image_path))

    return np.array(image_list)

def display_images_from_dir(dir_path: str) -> None:
    image_list = get_images_from_dir(dir_path)

    for image in image_list:
        display.display_image(image)

def play_video_from_dir(dir_path: str, output_path: str, fps: int = 30) -> None:
    image_list = get_images_from_dir(dir_path)

    display.play_frames_as_video(image_list, output_path, fps = fps)

play_video_from_dir(arg, 'test.mpg', 3)
