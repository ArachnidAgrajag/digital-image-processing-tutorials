# Sai Krishna I
# 19PD29
from PIL import Image
import numpy as np


def rmshe(image, r=0, x_0=0, x_l=255):
    # returns the image as is if the recursion depth is reached
    if r < 0:
        return image
    x_m = np.rint(np.mean(image))  # mean
    X_L = np.where(image <= x_m, image, -1)  # intensities less than mean
    X_U = np.where(image > x_m, image, -1)  # intensities greater than mean
    size_l = np.count_nonzero(X_L >= 0)  # number of pixels in X_L
    size_l = 1 if size_l == 0 else size_l  # to avoid div by 0 error
    size_u = np.count_nonzero(X_U >= 0)  # number of pixels in X_L
    size_u = 1 if size_u == 0 else size_u  # to avoid div by 0 error
    # intensity probabilties for sub-images
    p_l = [np.count_nonzero(X_L == i)/size_l for i in range(256)]
    p_u = [np.count_nonzero(X_U == i)/size_u for i in range(256)]
    # cummulative probabilty
    c_l = [sum(p_l[:i]) for i in range(256)]
    c_u = [sum(p_u[:i]) for i in range(256)]
    # transform function
    s_l = np.rint([x_0+(x_m-x_0)*c_l[i] for i in range(256)]).astype(np.uint8)
    s_u = np.rint([x_m+1+(x_l-x_m)*c_u[i]
                   for i in range(256)]).astype(np.uint8)
    # histogram equilized sub-images
    res_l = np.where(X_L >= 0, s_l[X_L], X_L)
    res_u = np.where(X_U >= 0, s_u[X_U], X_U)
    # Returns union of all the sub-images after recursion depth is reached
    return np.maximum(rmshe(res_l, r-1, x_0, x_m),
                      rmshe(res_u, r-1, x_m+1, x_l))


def main():
    name = "X-ray.jpg"
    image = np.array(Image.open("input/{}".format(name)).convert('L'))
    # for i in range(5):
    #     image_res = rmshe(image.astype(np.int64), i).astype(np.uint8)
    #     Image.fromarray(image_res).save("output/RMSHE_{}_{}".format(i, name),
    #                                     "jpeg")
    i = 4
    image_res = rmshe(image.astype(np.int64), i).astype(np.uint8)
    Image.fromarray(image_res).save("output/RMSHE_{}_{}".format(i, name),
                                    "jpeg")


if __name__ == '__main__':
    main()
