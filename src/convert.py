import cv2 as cv
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
import skimage.color as color
import subprocess

from typing import Optional, Tuple
from matplotlib import animation

def pgm_to_rgb_ppm(frame: np.array) -> np.array:
    height, width = frame.shape

    luminance_end = height * 2 // 3
    luminance = frame[:luminance_end]

    u_chrominance_end = width // 2
    u_chrominance = frame[luminance_end:, :u_chrominance_end]
    v_chrominance = frame[luminance_end:, u_chrominance_end:]

    u_chrominance = u_chrominance.repeat(2, axis = 0).repeat(2, axis = 1)
    v_chrominance = v_chrominance.repeat(2, axis = 0).repeat(2, axis = 1)

    yuv_frame = np.stack((luminance, u_chrominance, v_chrominance), axis = -1).astype(np.float32)
    yuv_frame[:, :, 1:] -= 127.5

    rgb_frame = np.clip(color.yuv2rgb(yuv_frame), 0., 255.).astype(np.uint8)

    return rgb_frame

def weave_mixing(first_field: np.array, second_field: np.array) -> np.array:
    frame = np.stack([first_field, second_field], axis = 2)
    frame = frame.swapaxes(1, 2)

    height, width, channels = first_field.shape
    return frame.reshape(2 * height, width, channels)

def bobbing(frame: np.array, top_field_first: bool) -> Tuple[np.array, np.array]:
    top_field, bottom_field = frame[0::2], frame[1::2]

    top_field = top_field.repeat(2, axis = 0)
    bottom_field = bottom_field.repeat(2, axis = 0)

    _, field_width, field_channels = frame.shape
    padding_row = np.zeros((1, field_width, field_channels), dtype = np.uint8)

    #top_field = np.concatenate((top_field, padding_row), axis = 0)
    #bottom_field = np.concatenate((padding_row, bottom_field), axis = 0)

    if top_field_first:
        return top_field, bottom_field
    return bottom_field, top_field

def video_to_frames(video_path: str, output_path: str, ts_pid: int = None) -> None:
    if os.path.exists(output_path):
        shutil.rmtree(output_path)

    os.mkdir(output_path)
    os.chdir(output_path)
    video_path = os.path.join('..', video_path)

    command = ['./../src/tools/mpeg2dec/src/mpeg2dec', video_path, '-o', 'pgm']
    if ts_pid is not None:
        command.extend(['-t', ts_pid])

    with open('../frames.meta', 'w') as outfile:
        subprocess.run(command, stdout = outfile)
    os.chdir('..')

def images_to_video(frame_array: np.array, output_path: str, fps: int) -> None:
    _, height, width, _ = frame_array.shape
    dpi = (height / 19) * (width / 33)
    figure, axes = plt.subplots(figsize = (width / dpi, height / dpi))

    figure.subplots_adjust(left = 0,
                            bottom = 0,
                            right = 1,
                            top = 1,
                            wspace = None,
                            hspace = None,
                        )

    mpl_writer = mpl.animation.writers['ffmpeg']
    metadata = { 'title': None, 'artist': __name__, 'comment': None, }
    mpl_writer = mpl_writer(fps = fps,
                            metadata = { k: v for k, v in metadata.items() if v is not None },
                            )

    iterator = iter(frame_array)
    with mpl_writer.saving(figure, output_path, dpi):
        plot = axes.imshow(next(iterator), interpolation = 'nearest')
        mpl_writer.grab_frame()

        for frame in iterator:
            plot.set_data(frame)
            mpl_writer.grab_frame()

def deinterlace(prev_field, field, next_field, threshold: float, top_field):

    bob_field = field.repeat(2, axis = 0)
    weave_field = weave_mixing(field, prev_field) if top_field \
                    else weave_mixing(prev_field, field)

    threshold = 40.0 if threshold is None else threshold

    field_height, field_width, _ = field.shape
    tile_shape = 16
    num_pixels = tile_shape * tile_shape
    for j in range(0, field_height, tile_shape):
        for i in range(0, field_width, tile_shape):
            y, x = j + tile_shape, i + tile_shape

            prev_tile = prev_field[j:y, i:x]
            next_tile = next_field[j:y, i:x]

            EBMA = np.sum((next_tile - prev_tile) ** 2)

            if EBMA / num_pixels < threshold:
                bob_field[2*j:2*y, i:x] = weave_field[2*j:2*y, i:x]

    return bob_field
