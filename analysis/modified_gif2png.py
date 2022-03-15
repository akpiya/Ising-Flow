from PIL import Image, GifImagePlugin
import matplotlib.pyplot as plt
import os

directory = "../data/"
extension = ".gif"
offsets = [2]
T = [2.25]
for offset in offsets:
	for t in T:

		name = "GifOffset=" + str(offset) + "_T=" + ("%.2f" % t) 
		modified_gif = directory + "modified_gifs/" + name + extension
		image_frames = directory + "image_frames/" + name + "/"
		image = Image.open(modified_gif)
		os.mkdir(image_frames)
		print(name)
		for frame in range(image.n_frames):
			frame_name = '{:03}'.format(frame)+".png"
			image.seek(frame)
			image.save(image_frames + frame_name)
