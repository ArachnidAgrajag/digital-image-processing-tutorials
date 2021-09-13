# Sai Krishna I
# 19PD29
from PIL import Image
import numpy as np


def bnd(x, p=0, q=255):
    if x < p:
        return p
    elif x > q:
        return q
    else:
        return x

def calc(img, ftr, image_op, m, n, x, y, i, j):
    # performs the operation on the given pixel
    # for the top right pixel the bottom left part of the filter is used
    # centers always line up
    # p and q are the neighbouring pixels
    v=0
    for p in range(i-int(x/2),  i+int(x/2)+1):
        for q in range(j-int(y/2),  j+int(y/2)+1):
            v += ftr[p+int(x/2)-i][q+int(y/2)-j]*img[bnd(p, 0, m-1)][bnd(q, 0, n-1)]
    return v


def apply_filter(image, filter, stride=1):
    (m, n) = image.shape
    image_op = np.zeros((m, n))
    (x, y) = filter.shape
    # i and j is the center pixel
    for i in range(0, m, stride):
        for j in range(0, n, stride):
            image_op[i][j]= calc(image, filter, image_op, m, n, x, y, i, j)
    return image_op.astype(np.uint8)


def guassian_filter(m, n, k, sig):
    guassian = np.zeros(m, n)
    for (s, t), val in np.nditer(guassian):
        guassian[s][t] = k * np.exp(-(s**2 + t**2)/(2*sig**2))
    return guassian


def main():
    name = "cat_bw"
    image = np.array(Image.open("input/{}.jpg".format(name)).convert('L'))
    # # list of filters
    f = {}
    # f[1] = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    f[2] = np.zeros((3, 3))
    f[2].fill(1)
    f[2] = f[2]/9
    # f[3] = np.array([[0, 0, 0], [1, 0, 0], [0, 0, 0]])
    # f[4] = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    # f[5] = (2*f[1]) - f[2]
    guassian = np.array([[0.3679, 0.6065, 0.3679],
                         [0.6065, 1, 0.6065],
                         [0.3679, 0.6065, 0.3679]])
    guassian = guassian/4.8976
    # for i, filter in f.items():
    #     # for each filter, stride is varied from 1 to 5
    #     for s in range(1, 6):
    #         img_name = "output_f/{}_f{}_s{}.jpg".format(name, i, s)
    #         print("Processing " + img_name)
    #         img_f = apply_filter(image, filter, s)
    #         print("Writing " + img_name)
    #         Image.fromarray(img_f).save(img_name, "jpeg")
    #         print("Done")
    img_name = "output/{}_guass.jpg".format(name)
    img_f = apply_filter(image, guassian, 1)
    Image.fromarray(img_f).save(img_name, "jpeg")
    img_name = "output/{}_box.jpg".format(name)
    img_f = apply_filter(image, f[2], 1)
    Image.fromarray(img_f).save(img_name, "jpeg")
    print("All done!")


if __name__ == '__main__':
    main()
