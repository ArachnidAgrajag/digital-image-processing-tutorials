import cv2 as cv
import glob
import numpy as np

# img_array = []
# for filename in glob.glob('input/pedestrianByFrame/*.png'):
#     img = cv.imread(filename)
#     height, width, layers = img.shape
#     size = (width, height)
#     img_array.append(img)
#
# out = cv.VideoWriter('output/pedestrian2.mp4', cv.VideoWriter_fourcc(*'mp4v'), 24, size)
#
# for i in range(len(img_array)):
#     out.write(img_array[i])
# out.release()
# capture = cv.VideoCapture('output/pedestrian2.mp4')
# width = capture.get(cv.CAP_PROP_FRAME_WIDTH)
# height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
# size = (int(width), int(height))
# print(size)
#
# out = cv.VideoWriter('output/pedestriangray.mp4', cv.VideoWriter_fourcc(*'mp4v'), 24, size)
# frame_i = 0
#
# while(capture.isOpened()):
#     ret, frame = capture.read()
#     if ret == False:
#         break
#     grayframe = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
#     out.write(grayframe)
# out.release()

capt = cv.VideoCapture('output/pedestriangray.mp4')
frame_i = 0
i = 1
fps = int(capt.get(cv.CAP_PROP_FRAME_COUNT))
print(capt)
while(capt.isOpened()):
    ret, frame = capt.read()
    if not ret:
        break
    if i == 1:
        print("yo")
        grayframe1 = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame_1 = grayframe1.copy()
    if i == fps:
        grayframe2 = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame_last = grayframe2.copy()
    i += 1

sh = frame_1.shape
sh = (int(sh[0]), int(sh[1]))
right = frame_1[:, int(sh[1]/2):sh[1]]
left = frame_last[:, 0:int(sh[1]/2)]
back = np.concatenate((left, right), axis=1)
print(back.shape)
cv.imwrite("output/background.png", back)


bcg = cv.imread("output/background.png", 0)
bcg = cv.medianBlur(bcg, 3)
capture = cv.VideoCapture('output/pedestriangray.mp4')
width = capture.get(cv.CAP_PROP_FRAME_WIDTH)
height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
size = (int(width), int(height))
print(size)

out = cv.VideoWriter('output/maskbw2.mp4', cv.VideoWriter_fourcc(*'H264'), 24, size)
frame_i = 0
frame_list = []
bcg0 = np.zeros(bcg.shape)
while(capture.isOpened()):
    ret, frame = capture.read()
    if ret == False:
        break
    gf = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gf = cv.medianBlur(gf, 3)
    frame_list.append(gf)
for i in range(len(frame_list)):
    if (i+1) != len(frame_list):
        sub = frame_list[i+1]-frame_list[i]
        sub = cv.medianBlur(sub, 9)
        out.write(sub)
#    msk=np.where(np.abs(bcg-gf)<=3,255,0).astype(np.uint8)
#    #msk=cv.bitwise_and(bcg,grayframe,mask = None)
#    #msk=grayframe-bcg
#    print(np.count_nonzero(msk>0))
#    print(msk.shape)
#    msk=cv.medianBlur(msk,9)
#    out.write(msk)
out.release()
print("done")
