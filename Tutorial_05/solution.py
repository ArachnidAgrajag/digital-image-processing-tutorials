# 19pd29
# SaiKrishna

import glob
import numpy as np
from PIL import Image, ImageFilter


def extract_background(frames_rgb):
    """
    the person in moving from left to right with a constant background
    so we can get the right half from the first frame and left half from the
    last frame and combine it to get the background
    """
    m, n, d = frames_rgb[0].shape
    right = frames_rgb[0][:, int(n/2):n]
    left = frames_rgb[-1][:, 0:int(n/2)]
    back = np.concatenate((left, right), axis=1)
    return back


def to_grayscale(frame):
    return np.mean(frame, axis=2).astype(np.uint8)


def invert_gray(frame):
    return (255 - frame).astype(np.uint8)


def save_frames(frames, path):
    filepath = path+"{}.png"
    i = 0
    for frame in frames:
        Image.fromarray(frame.astype(np.uint8)).save(filepath.format(i), "PNG")
        i += 1


def main():
    frames_rgb = []
    filenames = glob.glob('input/pedestrianByFrame/*.png')
    filenames.sort()
    for filename in filenames:
        img = np.array(Image.open(filename))
        frames_rgb.append(img)
    back = extract_background(frames_rgb)
    back_gray = to_grayscale(back)
    frames_gray = list(map(to_grayscale, frames_rgb))
    # back_inv = invert_gray(back_gray)
    frames_black_bg = list(map(lambda frame: 255 * (np.abs(
        frame - back_gray) >= 10).astype(np.uint8), frames_gray))

    frames_median_filter = list(map(lambda x: np.array(Image.fromarray(
        x).filter(ImageFilter.MedianFilter(size=3))), frames_black_bg))
    save_frames(frames_median_filter, 'output/frames_filter/median')
    frames_guass_filter = list(map(lambda x: np.array(Image.fromarray(
        x).filter(ImageFilter.GaussianBlur(radius=3))),
        frames_median_filter))
    save_frames(frames_guass_filter, 'output/frames_filter/median_guass')
    frames_mask = list(map(lambda x: 255 * (x >= 240), frames_guass_filter))
    save_frames(frames_mask, 'output/frames_mask/mask')
    new_bg = np.array(Image.open('input/meadow.png'))
    final_frames = []
    for i in range(len(frames_rgb)):
        frame_pers_r = frames_rgb[i][:, :, 0] * (frames_mask[i]/255)
        frame_pers_g = frames_rgb[i][:, :, 1] * (frames_mask[i]/255)
        frame_pers_b = frames_rgb[i][:, :, 2] * (frames_mask[i]/255)
        frame_bg_r = new_bg[:, :, 0] * ((255-frames_mask[i])/255)
        frame_bg_g = new_bg[:, :, 1] * ((255-frames_mask[i])/255)
        frame_bg_b = new_bg[:, :, 2] * ((255-frames_mask[i])/255)
        replaced_bg_r = frame_pers_r + frame_bg_r
        replaced_bg_g = frame_pers_g + frame_bg_g
        replaced_bg_b = frame_pers_b + frame_bg_b
        new_frame = np.dstack([replaced_bg_r, replaced_bg_g,
                              replaced_bg_b])
        final_frames.append(new_frame)
    save_frames(final_frames, 'output/replaced_background/final_frame')


if __name__ == '__main__':
    main()
