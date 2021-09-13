# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 08:39:52 2021

@author: 19pd29
"""
import numpy as np
from PIL import Image, ImageFilter


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
    return image_op


def zero_crossing(image):
    m,n=image.shape
    image_op = np.zeros((m,n),dtype=np.int64)
    j=0
    for row in image:
        for i in range(1,len(row)-1):
            if row[i]<0:
                if (row[i-1]<0 and row[i+1]>=0) or (row[i-1]>=0 and row[i+1]<0):
                    print('zero')
                    image_op[j][i]=255
        j+=1
    return image_op 
    

def main():
    name = "181079.jpg"
    image = Image.open("input/{}".format(name)).convert('L')
    laplace_4 = np.array([0,1,0,
                          1,-4,1, 
                          0,1,0])
    laplace_8 = np.array([1,1,1,
                          1,-8,1,
                          1,1,1])
    sobel_h = np.array([-1,-2,-1,
                       0,0,0,
                       1,2,1])
    sobel_v = np.array([-1,0,1,
                         2,0,2,
                        -1,0,1])
    
    im_l4 = image.filter(ImageFilter.Kernel((3,3),laplace_4,1,0))
    im_l8 = image.filter(ImageFilter.Kernel((3,3),laplace_8,1,0))
    im_sh = image.filter(ImageFilter.Kernel((3,3),sobel_h,1,0))
    im_sv = image.filter(ImageFilter.Kernel((3,3),sobel_v,1,0))
    
    im_l4.save("output/l4_{}".format(name),"jpeg")
    im_l8.save("output/l8_{}".format(name),"jpeg")
    im_sh.save("output/sh_{}".format(name),"jpeg")
    im_sv.save("output/sv_{}".format(name),"jpeg")
    
    '''   
    im_l40 = zero_crossing(np.array(im_l4))
    im_l80 = zero_crossing(np.array(im_l8))
    im_sh0 = zero_crossing(np.array(im_sh))
    im_sv0 = zero_crossing(np.array(im_sv))
    
    Image.fromarray(im_l40.astype(np.uint8)).save("output/l40_{}".format(name),"jpeg")
    Image.fromarray(im_l80.astype(np.uint8)).save("output/l80_{}".format(name),"jpeg")
    Image.fromarray(im_sh0.astype(np.uint8)).save("output/sh0_{}".format(name),"jpeg")
    Image.fromarray(im_sv0.astype(np.uint8)).save("output/sv0_{}".format(name),"jpeg")
    '''
    
if __name__ == '__main__':
    main()
    