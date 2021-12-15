import numpy as np
import skimage.registration as registration

def motion_estimation(first_image, second_image):
    v, u = registration.optical_flow_ilk(second_image, first_image)
    return np.sqrt(np.power(u, 2) + np.power(v, 2))
