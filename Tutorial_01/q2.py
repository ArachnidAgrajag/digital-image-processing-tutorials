# Sai Krishna I
# 19PD29
from PIL import Image
import numpy as np

# Open both images and convert to array
img1 = np.array(Image.open("input/image1.jpg"))
img2 = np.array(Image.open("input/image2.jpg"))
# proceed if the images have the same resolution
if img1.shape == img2.shape:
    # split both images into RBG channel
    img1_r = img1[:, :, 0]
    img1_g = img1[:, :, 1]
    img1_b = img1[:, :, 2]
    img2_r = img2[:, :, 0]
    img2_g = img2[:, :, 1]
    img2_b = img2[:, :, 2]
    # find the difference between the images
    diff_r = np.abs(img2_r-img1_r)
    diff_g = np.abs(img2_g-img1_g)
    diff_b = np.abs(img2_b-img1_b)
    # save the images
    Image.fromarray(diff_r).save("output/r_diff.jpg", "jpeg")
    Image.fromarray(diff_g).save("output/g_diff.jpg", "jpeg")
    Image.fromarray(diff_b).save("output/b_diff.jpg", "jpeg")
else:
    print("Images must have same resolution")
