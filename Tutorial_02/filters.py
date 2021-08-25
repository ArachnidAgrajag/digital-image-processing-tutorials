# Sai Krishna I
# 19PD29
from PIL import Image
import numpy as np


def bnd(x, p, q):
    if x < p:
        return p
    elif x > q:
        return q
    else:
        return x


def calc(img, ftr, image_op, m, n, x, y, i, j, p, q):
    # performs the operation on the given pixel
    # for the top right pixel the bottom left part of the filter is used
    # centers always line up
    v = ftr[p+int(x/2)-i][q+int(y/2)-j]*img[bnd(p, 0, m-1)][bnd(q, 0, n-1)]
    image_op[bnd(p, 0, m-1)][bnd(q, 0, n-1)] += v
    image_op[bnd(p, 0, m-1)][bnd(q, 0, n-1)] /= 2


def apply_filter(image, filter, stride):
    (m, n) = image.shape
    image_op = np.zeros((m, n))
    (x, y) = filter.shape
    # i and j is the center pixel
    for i in range(0, m, stride):
        for j in range(0, n, stride):
            # p and q are the neighbouring pixels
            for p in range(i-int(x/2),  i+int(x/2)+1):
                for q in range(j-int(y/2),  j+int(y/2)+1):
                    calc(image, filter, image_op, m, n, x, y, i, j, p, q)
    return image_op.astype(np.uint8)


def main():
    name = "cat_bw"
    image = np.array(Image.open("input/{}.jpg".format(name)).convert('L'))
    # list of filters
    f = {}
    f[1] = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    f[2] = np.zeros((3, 3))
    f[2].fill(1)
    f[2] = f[2]/9
    f[3] = np.array([[0, 0, 0], [1, 0, 0], [0, 0, 0]])
    f[4] = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    f[5] = (2*f[1]) - f[2]
    for i, filter in f.items():
        # for each filter, stride is varied from 1 to 5
        for s in range(1, 6):
            img_name = "output/{}_f{}_s{}.jpg".format(name, i, s)
            print("Processing " + img_name)
            img_f = apply_filter(image, filter, s)
            print("Writing " + img_name)
            Image.fromarray(img_f).save(img_name, "jpeg")
            print("Done")
    print("All done!")


if __name__ == '__main__':
    main()
