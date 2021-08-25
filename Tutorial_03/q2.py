# Sai Krishna I
# 19PD29
from PIL import Image
import numpy as np


def contrast_strech(image):
    # streching contrast linearly
    pmin = np.min(image)
    pmax = np.max(image)
    res = 255/(pmax-pmin) * (image-pmin)
    return res.astype(np.uint8)


def intensity_slice_bw(image, int_min, int_max):
    # intensity slicing with two colors only
    res = np.where(np.logical_and(image <= int_max,
                                  image >= int_min), 255, 0).astype(np.uint8)
    return res.astype(np.uint8)


def intensity_slice(image, int_min, int_max):
    # intensity slice where the values in our interest
    # are increased to a constant intensity
    res = np.where(np.logical_and(image <= int_max,
                                  image >= int_min), 222, image)
    return res.astype(np.uint8)


def bitplane_slice(image, bitplane):
    # bitplane slicing
    res = np.bitwise_and(image, bitplane)
    return res.astype(np.uint8)


def main():
    name = "cat_bw.jpg"
    image = np.array(Image.open("input/{}".format(name)).convert('L'))
    im_contrast = contrast_strech(image)
    Image.fromarray(im_contrast).save("output/cont_strech_{}".format(name),
                                      "jpeg")
    im_int_slice1 = intensity_slice_bw(image, 60, 150)
    Image.fromarray(im_int_slice1).save("output/int_slic_bw_{}".format(name),
                                        "jpeg")
    im_int_slice = intensity_slice(image, 60, 150)
    Image.fromarray(im_int_slice).save("output/int_slice_{}".format(name),
                                       "jpeg")
    for i in range(8):
        image_contrast = bitplane_slice(image, 2**i)
        Image.fromarray(image_contrast).save("output/bit{}{}".format(i, name),
                                             "jpeg")
    image_contrast = bitplane_slice(image, 240)
    Image.fromarray(image_contrast).save("output/bit{}{}".format("4-7", name),
                                         "jpeg")


if __name__ == '__main__':
    main()
