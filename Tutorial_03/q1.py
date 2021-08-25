# Sai Krishna I
# 19PD29
from PIL import Image
import numpy as np


def log_transform(image, c=None):
    if c is None:
        c = 255/np.log(256)
    transformed_image = (c * np.log(1+image.astype(int))).astype(np.uint8)
    return transformed_image


def gamma_transform(image, gamma, c=None):
    if c is None:
        c = 255/(255**gamma)
    transformed_image = (c * np.power(image, gamma)).astype(np.uint8)
    return transformed_image


def main():
    name = "cat_bw"
    image = np.array(Image.open("input/{}.jpg".format(name)).convert('L'))
    image_log = log_transform(image, c=43)
    Image.fromarray(image_log).save("output/{}_log.jpg".format(name),
                                    "jpeg")
    image_gamma = gamma_transform(image, 0.5, 30)
    Image.fromarray(image_gamma).save("output/{}_gamma.jpg".format(name),
                                      "jpeg")


if __name__ == '__main__':
    main()
