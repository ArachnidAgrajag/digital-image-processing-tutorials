# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 08:51:25 2021

@author: 19pd29
"""
from PIL import Image,ImageFilter
import numpy as np


def psnr(im_og, im_noise):
    mat_og= np.array(im_og)
    mat_noise = np.array(im_noise)
    m,n=mat_og.shape
    mse = np.sum(np.square(mat_og-mat_noise))/(m*n)
    psnr = 20 * np.log10(255) - 10 * np.log10(mse)
    return psnr 

def main():
    name = "Lenna"
    image = Image.open("input/{}.png".format(name)).convert('L')
    image.save("output/{}_bw.png".format(name),"PNG")
    noise1 =  (255*np.random.normal(0,1,image.size)).astype(np.uint8)
    noise2 =  (255*np.random.normal(0,1,image.size)).astype(np.uint8)
    Image.fromarray(noise1).save("output/noise.png","PNG")
    image_noisy = Image.fromarray(np.maximum(np.array(image),noise1))
    image_noisy.save("output/image_noise.png","PNG")
    image_guass_filter = image_noisy.filter(ImageFilter.GaussianBlur(radius=3))
    image_mean_filter = image_noisy.filter(
                        ImageFilter.Kernel((3,3),np.ones(9)/9))
    image_median_filter = image_noisy.filter(ImageFilter.MedianFilter(size=3))
    image_guass_filter.save("output/image_guassfilter.png","PNG")
    image_mean_filter.save("output/image_mean_filter.png","PNG")
    image_median_filter.save("output/image_median_filter.png","PNG")
    print("guass psnr = ",psnr(image,image_guass_filter))
    print("mean psnr = ",psnr(image,image_mean_filter))
    print("median psnr = ",psnr(image,image_median_filter))
    
    image_noisy1 = Image.fromarray(np.maximum(np.array(image),noise1))
    image_noisy2 = Image.fromarray(np.maximum(np.array(image),noise2))
    Image.fromarray(np.abs(np.array(image_noisy1,dtype=np.int64)-np.array(image_noisy2,dtype=np.int64)).astype(np.uint8)).save("output/noise_diff.png","PNG")



if __name__=='__main__':
    main()