from PIL import Image, GifImagePlugin
import matplotlib.pyplot as plt
import os

directory = "../data/supplemental/"
extension = ".gif"
# offsets = [10]
# T = [1, 1.5, 2, 2.25, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7, 8, 9, 10]
# for offset in offsets:
# 	for t in T:

name = "Movie 3"
modified_gif = directory + name + extension
image_frames = directory + name + "/"
image = Image.open(modified_gif)
os.mkdir(image_frames)
print(name)
for frame in range(image.n_frames):
    frame_name = '{:03}'.format(frame)+".png"
    image.seek(frame)
    image.save(image_frames + frame_name)
