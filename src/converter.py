import cv2 as cv
import numpy as np
import os
import skimage.color as color

def open_pgm_in_rgb_ppm(path: os.path) -> np.array:
    image = cv.imread(path, cv.IMREAD_GRAYSCALE)
    height, width = image.shape

    luminance_end = height * 2 // 3
    luminance = image[:luminance_end]

    u_chrominance_end = width // 2
    u_chrominance = image[luminance_end:, :u_chrominance_end]
    v_chrominance = image[luminance_end:, u_chrominance_end:]

    u_chrominance = u_chrominance.repeat(2, axis = 0).repeat(2, axis = 1)
    v_chrominance = v_chrominance.repeat(2, axis = 0).repeat(2, axis = 1)

    yuv_image = np.stack((luminance, u_chrominance, v_chrominance), axis = -1).astype(np.float32)
    yuv_image[:, :, 1:] -= 127.5

    rgb_image = np.clip(color.yuv2rgb(yuv_image), 0., 255.).astype(np.uint8)

    return rgb_image

def bobbing(frames: np.array) -> np.array:
    pass
