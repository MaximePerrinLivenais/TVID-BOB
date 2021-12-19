import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import os
import subprocess
import sys

from typing import Optional, List

import convert

def open_grayscale(path: str) -> np.array:
    return cv.imread(path, cv.IMREAD_GRAYSCALE)

def get_frame_paths_from_dir(dir_path: str) -> List[str]:
    path_list = []

    numerical_sort = lambda key: int(key.split('.')[0])
    for frame_name in sorted(os.listdir(dir_path), key = numerical_sort):
        print(frame_name)
        path_list.append(os.path.join(dir_path, frame_name))

    return path_list

def get_images_from_dir(dir_path: str) ->np.array:
    path_list = get_frame_paths_from_dir(dir_path)

    image_list = []
    for path in path_list:
        image = convert.pgm_to_rgb_ppm(open_grayscale(path))

        image_list.append(image)

    return np.array(image_list)

def get_images_from_dir_bob(dir_path: str, frames_meta) -> np.array:
    path_list = get_frame_paths_from_dir(dir_path)

    image_list = []
    meta_index, progressive_sequence = 0, 0
    for path in path_list:
        image = convert.pgm_to_rgb_ppm(open_grayscale(path))

        while frames_meta[meta_index][0]:
            progressive_sequence = frames_meta[meta_index]
            meta_index += 1
        meta = frames_meta[meta_index]
        meta_index += 1

        if meta[1]:
            image_list.append(image)
        else:
            first_image, second_image = convert.bobbing(image, meta[2])
            image_list.append(first_image)
            image_list.append(second_image)

            if meta[3]:
                image_list.append(first_image)
    return np.array(image_list)

def get_images_from_dir_X(dir_path: str, threshold:float, frames_meta) -> np.array:
    path_list = get_frame_paths_from_dir(dir_path)

    image = convert.pgm_to_rgb_ppm(open_grayscale(path_list[0]))
    first_image, second_image = convert.bobbing(image, frames_meta[0][2])
    image_list = [first_image, second_image]
    prev_bf = image[1::2]
    next_image = convert.pgm_to_rgb_ppm(open_grayscale(path_list[1]))

    meta_index, progressive_sequence = 0, 0
    for index in range(2, len(path_list) - 1):
        image = next_image
        next_image = convert.pgm_to_rgb_ppm(open_grayscale(path_list[index]))

        while frames_meta[meta_index][0]:
            progressive_sequence = frames_meta[meta_index]
            meta_index += 1
        meta = frames_meta[meta_index]
        meta_index += 1

        if meta[1]:
            image_list.append(image)
        else:
            tf, bf = image[0::2], image[1::2]
            next_tf = next_image[0::2]

            top_field = convert.deinterlace(prev_bf, tf, bf, threshold, True)
            bottom_field = convert.deinterlace(tf, bf, next_tf, threshold, False)

            first_image, second_image = (top_field, bottom_field) if meta[2] \
                                        else (bottom_field, top_field)

            image_list.append(first_image)
            image_list.append(second_image)

            if meta[3]:
                image_list.append(first_image)

        prev_bf = image[1::2]

    return np.array(image_list)

def display_image(image: np.array) -> None:
    plt.imshow(image)
    plt.show()

def display_images_from_dir(dir_path: str, deinterlacing: bool, bob: bool,
                            threshold:float, frames_meta) -> None:
    if not deinterlacing:
        image_array = get_images_from_dir(dir_path)
    elif bob:
        image_array = get_images_from_dir_bob(dir_path, frames_meta)
    else:
        image_array = get_images_from_dir_X(dir_path, threshold, frames_meta)

    for image in image_array:
        display_image(image)

def create_video_from_dir(dir_path: str, output_path: str, deinterlacing: bool,
                            bob: bool, fps: int, threshold: float, frames_meta) -> None:
    if not deinterlacing:
        image_array = get_images_from_dir(dir_path)
    elif bob:
        image_array = get_images_from_dir_bob(dir_path, frames_meta)
    else:
        image_array = get_images_from_dir_X(dir_path, threshold, frames_meta)

    if fps is None:
        for meta in frames_meta:
            if meta[0] and fps is None:
                fps = meta[3]
            elif meta[0] and fps != meta[3]:
                sys.exit('All sequences does not have the same ips cadence\n')

    convert.images_to_video(image_array, output_path, fps)

def play_video(video_path):
    subprocess.run(['vlc', video_path])
