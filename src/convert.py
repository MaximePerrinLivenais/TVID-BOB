import cv2 as cv
import matplotlib as mpl
import matplotlib.pyplot as plt
import motion
import numpy as np
import os
import shutil
import skimage.color as color
import subprocess

from typing import Optional, Tuple

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
    even_frame, odd_frame = frame[0::2], frame[1::2]
    even_frame = even_frame.repeat(2, axis = 0)
    odd_frame = odd_frame.repeat(2, axis = 0)

    if top_field_first:
        return even_frame, odd_frame
    return odd_frame, even_frame

def video_to_frames(video_path: str, output_path: str, ts_pid: int = None) -> None:
    if os.path.exists(output_path):
        shutil.rmtree(output_path)

    os.mkdir(output_path)
    os.chdir(output_path)
    video_path = os.path.join('..', video_path)

    command = ['./../tools/mpeg2dec/src/mpeg2dec', video_path, '-o', 'pgm']
    if ts_pid is not None:
        command.extend(['-t', ts_pid])

    print(command)
    subprocess.run(command)
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

def deinterlace(frame: np.array, previous_frame: np.array, top_field_first: bool) -> np.array:
    fields = (frame[0::2], frame[1::2], previous_frame[0::2]) if top_field_first \
                else (frame[1::2], frame[0::2], previous_frame[1::2])
    first_field, second_field, previous_field = fields

    first_frame, second_frame = bobbing(frame, top_field_first)

    first_frame_weave = weave_mixing(previous_field, first_field)
    second_frame_weave = weave_mixing(first_field, second_field)

    tile_shape = 16
    motion_estimation = motion.motion_estimation(first_field.mean(axis = 2),
                                                    second_field.mean(axis = 2))
    motion_height, motion_width = motion_estimation.shape
    for j in range(0, motion_height, tile_shape):
        for i in range(0, motion_width, tile_shape):
            y, x = j + tile_shape, i + tile_shape
            tile = motion_estimation[j:y, i:x]

            if tile.mean() < 0.2:
                first_frame[2*j:2*y, i:x] = first_frame_weave[2*j:2*y, i:x]
                second_frame[2*j:2*y, i:x] = second_frame_weave[2*j:2*y, i:x]
    return first_frame_weave, second_frame_weave
