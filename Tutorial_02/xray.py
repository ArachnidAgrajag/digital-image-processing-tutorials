# Sai Krishna I
# 19PD29
from PIL import Image
import numpy as np


def get_boundary_1d(image_inv):
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
    v1, v2 = get_boundary_1d(image)
    h1, h2 = get_boundary_1d(np.transpose(image))
    return {'top': v1, 'left': h1, 'bottom': v2, 'right': h2}


def generate_rect_mask(size_orig, position, size):
    # generates a mask with the given size and position
    mask = np.zeros(size_orig)
    mask[position[0]:position[0]+size[0],
         position[1]:position[1]+size[1]].fill(255)
    return mask.astype(np.uint8)


def crop_with_mask(image, mask):
    return np.minimum(image, mask).astype(np.uint8)


def crop(image, boundaries):
    image_cropped = image[boundaries['top']:boundaries['bottom'],
                          boundaries['left']:boundaries['right']].copy()
    return image_cropped


def main():
    image = np.array(Image.open("input/X-ray.jpg").convert('L'))
    (m, n) = image.shape
    # the top right corner of the cropped image
    # relative to the original image
    # for a 100x200 image (0.2,0.3) will be (20, 60)
    postition_perct = (0.4, 0.2)
    position = (int(postition_perct[0]*m), int(postition_perct[1]*n))
    # the size of the cropped image
    # relative to the original image
    # for a 100x200 image (0.7,0.5) will be 70x100
    size_perct = (1, 0.5)
    size = (int(size_perct[0]*m), int(size_perct[1]*n))
    mask = generate_rect_mask(image.shape, position, size)
    image_masked = crop_with_mask(image, mask)
    Image.fromarray(image_masked).save("output/xray_masked.jpg", "jpeg")
    boundaries = get_boundary_2d(image_masked)
    image_cropped = crop(image, boundaries)
    Image.fromarray(image_cropped).save("output/xray_cropped.jpg", "jpeg")


if __name__ == '__main__':
    main()
