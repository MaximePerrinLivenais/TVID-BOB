import cv2 as cv
import matplotlib as mpl
import matplotlib.pyplot as plt
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

def bobbing(frame: np.array, top_field_first: bool = True) -> Tuple[np.array, np.array]:
    even_frame, odd_frame = frame[0::2], frame[1::2]
    even_frame = even_frame.repeat(2, axis = 0)
    odd_frame = odd_frame.repeat(2, axis = 0)

    if top_field_first:
        return even_frame, odd_frame
    return odd_frame, even_frame

def video_to_frames(video_path: str, output_path: str) -> None:
    if os.path.exists(output_path):
        shutil.rmtree(output_path)

    os.mkdir(output_path)
    os.chdir(output_path)
    video_path = os.path.join('..', video_path)
    subprocess.run(['./../tools/mpeg2dec/src/mpeg2dec', video_path, '-o', 'pgm'])
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
