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


def phi_dpf(im, x, y):
    # this finds the difference between the pixel and its N4
    # neighbours, if the center pixel is darker that its neighbours
    # its value is passed else, its 0.
    # The sum of all 4 values gives the gradient
    image = im.astype(np.float64)
    (n, m) = image.shape
    grad = 0
    grad += min((image[x][y]-image[bnd(x+1, 0, m-1)][y])/255, 0)
    grad += min((image[x][y]-image[bnd(x-1, 0, m-1)][y])/255, 0)
    grad += min((image[x][y]-image[x][bnd(y+1, 0, n-1)])/255, 0)
    grad += min((image[x][y]-image[x][bnd(y-1, 0, n-1)])/255, 0)
    return -grad


def get_pyramid(image, levels):
    # generates a pyramind of images, where the next image
    # is downsampled by a factor of 2
    (n, m) = image.size
    A = []
    A.append(image.resize((int(n*480/m), 480), resample=Image.BICUBIC))
    for l in range(1, levels):
        (na, ma) = A[l-1].size
        A.append(A[l-1].resize((int(na/2), int(ma/2)), resample=Image.BICUBIC))
    return A


def get_gradients(A_pyramid):
    # Applies the dark pass filter on each pixel to get the gradient
    phi_A = []
    i = 0
    for A in A_pyramid:
        res = np.zeros(A.size, dtype='float64')
        A_mat = np.array(A)
        for id, v in np.ndenumerate(A_mat):
            res[id[0]][id[1]] = phi_dpf(A_mat, id[0], id[1])
        i += 1
        phi_A.append(res)
    return phi_A


def upsample_pyramid(phi_A):
    # return the upscaled pyramid
    levels = len(phi_A)
    A = []
    for l in range(0, levels):
        (na, ma) = phi_A[l].shape
        A.append(Image.fromarray(phi_A[l]).resize(
            (int(na * 2**l), int(ma * 2**l)), resample=Image.BICUBIC))
    return A


def get_PHI(image, L=4, eps=0.001):
    # the image is transformed into a sequence of coarse images
    # through subsampling. each image is downsampled by a factor of 2
    # using bicubic interpolation for the next level
    pyramids = get_pyramid(image, L)
    # for each image in the level, a gradient is calculated
    # using the dark pass filter
    gradients = get_gradients(pyramids)
    # the gradients are then upsampled to match
    # the resolution of the first level
    upsampled_gradients = upsample_pyramid(gradients)
    res = np.ones(upsampled_gradients[0].size, dtype=np.float64)
    # next we take the geometric mean of all the gradients.
    # This gives the overall visual importance
    for l in range(L):
        res = res * np.maximum(np.array(
            upsampled_gradients[l]).astype(np.float64), eps)
    res = np.power(res, 1/L)
    return res


def CACHE(image, L=4):
    (n, m) = image.shape
    img_pil = Image.fromarray(image)
    # we calculate the visual importance of each pixels through phi_img
    phi_img = get_PHI(img_pil, L)
    im_resized = np.array(img_pil.resize((int(n*480/m), 480),
                          resample=Image.BICUBIC)).astype(np.float64)
    # for each Intensity,
    # we calculate its relative importance as the probabilty
    p = np.array([np.sum(phi_img*(im_resized == k).astype(np.int64))/np.sum(phi_img)
                  for k in range(256)])
    # using the above p we equilize the histogram
    s = np.rint([255*np.sum(p[:i]) for i in range(256)]).astype(np.uint8)
    res = s[image]
    return res


def main():
    name = "cat_bw.jpg"
    image = np.array(Image.open("input/{}".format(name)).convert('L'))
    image_cache = CACHE(image)
    Image.fromarray(image_cache).save("output/CACHE_{}".format(name),
                                      "jpeg")


if __name__ == '__main__':
    main()
