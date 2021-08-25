# Sai Krishna I
# 19PD29
from PIL import Image
import numpy as np
import sys
sys.setrecursionlimit(100000)


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


def crop(image, boundaries):
    image_cropped = image[boundaries['top']:boundaries['bottom'],
                          boundaries['left']:boundaries['right']].copy()
    return image_cropped


def bnd(x, p, q):
    if x < p:
        return p
    elif x > q:
        return q
    else:
        return x


def sel_obj(image, index, img_op, threshold, size):
    """
    if the center pixel has a value greater than the threshold,
    it is copied to the blank image.
    Then the pixels surrounding the center (size x size matrix) which clear
    the threshold are treated as the center pixel and the process continues
    till all pixels that are connected is transfered to the blank image
    """
    (m, n) = image.shape
    stack = []
    stack.append(index)
    while (len(stack) > 0):
        (i, j) = stack.pop()
        for p in range(i-int(size/2), i+int(size/2)+1):
            for q in range(j-int(size/2), j+int(size/2)+1):
                k = bnd(p, 0, m-1)
                l = bnd(q, 0, n-1)
                if image[k][l] > threshold:
                    # print(k, l)
                    img_op[k][l] = image[k][l]
                    image[k][l] = 0
                    stack.append((k, l))


def select_all(img, threshold, size):
    """
    When a pixel greater than the threshold is detected
    a blank image is created and all pixels connected to that pixel are
    transfered to the blank image and removed from the original.
    the process is continued till the original image is empty
    i.e all connected objects are removed
    """
    image = img.copy()
    objects = []
    count = 0
    (m, n) = image.shape
    for i in range(m):
        for j in range(n):
            if image[i][j] > threshold:
                objects.append(np.zeros((m, n)))
                sel_obj(image, (i, j), objects[count], threshold, size)
                count += 1
    return objects


def main():
    image = np.array(Image.open("input/Number-Plate.jpg").convert('L'))
    img_inv = 255 - image
    # list of objects as seperate images, same size as original
    objects = select_all(img_inv, 10, 3)
    i = 0
    for img in objects:
        # image is cropped to the content and saved
        img = crop(img, get_boundary_2d(img))
        img = (255-img).astype(np.uint8)
        Image.fromarray(img).save("output/num_{}.jpg".format(i), "jpeg")
        i += 1


if __name__ == '__main__':
    main()
