import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import os
import subprocess

from typing import Optional

import convert

def open_grayscale(path: str) -> np.array:
    return cv.imread(path, cv.IMREAD_GRAYSCALE)

def get_frame_paths_from_dir(dir_path: str) -> list[str]:
    path_list = []

    for frame_name in os.listdir(dir_path):
        path_list.append(os.path.join(dir_path, frame_name))

    return path_list

def get_images_from_dir(dir_path: str, deinterlacing: bool, bob: bool,
                            top_field_first: bool) -> np.array:
    path_list = get_frame_paths_from_dir(dir_path)

    image_list = []
    previous_image = convert.pgm_to_rgb_ppm(open_grayscale(path_list[0]))
    for path in path_list:
        image = convert.pgm_to_rgb_ppm(open_grayscale(path))

        if deinterlacing and bob:
            first_image, second_image = convert.bobbing(image, top_field_first)
            image_list.append(first_image)
            image_list.append(second_image)
        elif deinterlacing:
            first_image, second_image = convert.deinterlace(image, previous_image, top_field_first)
            image_list.append(first_image)
            image_list.append(second_image)
            previous_image = image
        else:
            image_list.append(image)

    return np.array(image_list)

def display_image(image: np.array) -> None:
    plt.imshow(image)
    plt.show()

def display_images_from_dir(dir_path: str, deinterlacing: bool, bob: bool,
                            top_field_first: bool) -> None:
    image_array = get_images_from_dir(dir_path, deinterlacing, bob, top_field_first)

    for image in image_array:
        display_image(image)

def create_video_from_dir(dir_path: str, output_path: str, deinterlacing: bool,
                            bob: bool, fps: int, top_field_first: bool) -> None:
    image_array = get_images_from_dir(dir_path, deinterlacing, bob, top_field_first)


    convert.images_to_video(image_array, output_path, fps)

def play_video(video_path):
    subprocess.run(['vlc', video_path])
