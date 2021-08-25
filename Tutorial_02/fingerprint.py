# Sai Krishna I
# 19PD29
from PIL import Image
import numpy as np


def get_boundary_1d(image_inv):
    """
    checks if all the elements in a row are 0, from the top and bottom
    when the first non-zero row is encountered the position is saved
    This gives the boundary in one axis
    """
    top = 0
    top_done = False
    bottom = image_inv.shape[0]-1
    bottom_done = False
    for row_i in range(image_inv.shape[0]):
        if all(image_inv[row_i] == 0) and not top_done:
            top = top+1
        else:
            top_done = True
        if all(image_inv[image_inv.shape[0]-1-row_i] == 0) and not bottom_done:
            bottom = bottom-1
        else:
            bottom_done = True
        if top_done and bottom_done:
            return (top, bottom)


def get_boundary_2d(image):
    # get boundary in vertical direction
    v1, v2 = get_boundary_1d(image)
    # get boundary in horizontal direction
    # passing the transpose of the image,
    # to the function that gives top and bottom boundaries
    h1, h2 = get_boundary_1d(np.transpose(image))
    return {'top': v1, 'left': h1, 'bottom': v2, 'right': h2}


def crop(image, boundaries):
    # crops and returns a new image
    image_cropped = image[boundaries['top']:boundaries['bottom'],
                          boundaries['left']:boundaries['right']].copy()
    return image_cropped


def main():
    image = np.array(Image.open("input/fingerprint.jpg"))[:, :, 0]
    image_inv = 255-image
    boundaries = get_boundary_2d(image_inv)
    image_cropped = crop(image, boundaries)
    Image.fromarray(image_cropped).save("output/fingerprint_cropped.jpg",
                                        "jpeg")


if __name__ == '__main__':
    main()
