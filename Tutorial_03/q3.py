# Sai Krishna I
# 19PD29
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def plot_histogram(image, name):
    # plots the histogram
    h = [np.count_nonzero(image == i) for i in range(256)]
    bins = np.arange(256)
    plt.bar(bins, h, width=1)
    plt.xlabel("Intensity")
    plt.ylabel("Frequency")
    plt.title("Intensity Histogram of {}".format(name))
    plt.savefig("output/hist_{}".format(name))
    plt.close()


def equilize_histogram(image):
    (m, n) = image.shape
    pixels = m*n
    # probabilty
    p = [np.count_nonzero(image == i)/pixels for i in range(256)]
    # transform function
    s = np.rint([255*sum(p[:i]) for i in range(256)]).astype(np.uint8)
    # result
    res = s[image]
    return res


def main():
    name = "X-ray.jpg"
    image = np.array(Image.open("input/{}".format(name)).convert('L'))
    plot_histogram(image, "cat_bw.jpg")
    image_equi = equilize_histogram(image)
    plot_histogram(image_equi, "equi_cat_bw.jpg")
    Image.fromarray(image_equi).save("output/equi_hist_{}".format(name),
                                     "jpeg")


if __name__ == '__main__':
    main()
