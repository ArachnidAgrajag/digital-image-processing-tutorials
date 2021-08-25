# Sai Krishna I
# 19PD29
from PIL import Image
import numpy as np
from glob import glob
from datetime import datetime


def invert_bw(x: int) -> int: return 255-x  # grayscale pixel range 0-255


def is_grayscale(mat: np.ndarray) -> bool:
    """
    Checks if a image is grayscale.
    Returns true if its grayscale false otherwise
    """
    if len(mat.shape) == 3:
        # if RGB channels have the same value the image is grayscale
        # seperating the RGB channels
        mat_r = mat[:, :, 0]
        mat_g = mat[:, :, 1]
        mat_b = mat[:, :, 2]
        # checking if they are eqaul
        c1 = (mat_r == mat_b).all()
        c2 = False
        if(c1):
            c2 = (mat_r == mat_g).all()
        return c1 and c2
    else:
        # if the array is 2d the image is grayscale
        return True


# scan for image files in the input folder
images = glob("input/*.jpg") + glob("input/*.jpeg")
# if images are found proceed
if len(images) != 0:
    for img_file in images:
        # Open the image
        image = Image.open(img_file)
        mat = np.array(image)
        # check if image is grayscale
        if(is_grayscale(mat)):
            # if eqaul rgb's select one channel to make the image grayscale
            if len(mat.shape) == 3:
                mat_bw = mat[:, :, 0]
            else:
                mat_bw = mat
            # invert the grayscale image by subtracting each pixel from 255
            mat_bw_inv = invert_bw(mat_bw)

            # generate the output filename with timestamp
            f0 = img_file.replace(
                'input/', 'output/out_inv'+datetime.now()
                .strftime("_%m-%d-%Y_%H-%M-%S_"))
            # save the Image
            Image.fromarray(mat_bw_inv).save(f0, "jpeg")
        else:
            # seperate the RGB channels
            mat_r = mat[:, :, 0]
            mat_g = mat[:, :, 1]
            mat_b = mat[:, :, 2]

            # create a new array with
            # the red value is replaced by blue
            # the green value is replaced by red
            # the blue value is replaced by green
            mat_rgb_swap = np.stack((mat_b, mat_r, mat_g), axis=2)

            # generate a grayscale image from the average of rgb values
            # average rgb value
            mat_avg = (np.average((mat_r, mat_g, mat_b), axis=0))
            # convert to unsigned 8bit integer
            mat_bw_avg = np.rint(mat_avg).astype(np.uint8)
            # generate the output filename with timestamp
            f1 = img_file.replace(
                'input/', 'output/out_swap'+datetime.now()
                .strftime("_%m-%d-%Y_%H-%M-%S_"))
            f2 = img_file.replace(
                'input/', 'output/out_bw'+datetime.now()
                .strftime("_%m-%d-%Y_%H-%M-%S_"))
            # save the images
            Image.fromarray(mat_rgb_swap).save(f1, "jpeg")
            Image.fromarray(mat_bw_avg).save(f2, "jpeg")
