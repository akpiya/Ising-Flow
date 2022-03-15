from PIL import Image, ImageFilter, ImageSequence
import matplotlib.pyplot as plt

directory = "../data/"
offsets = [2]
T = [2.25]
for offset in offsets:
    for t in T:
        name = "GifOffset=" + str(offset) + "_T=" + ("%.2f" % t) + ".gif"
        raw_gif = directory + "raw_gifs/" + name
        modified_gif = directory + "modified_gifs/" + name
        ret_images = []
        print(name)
        with Image.open(raw_gif) as im:
            index = 0
            for frame in ImageSequence.Iterator(im):
                ret_images.append(frame.convert(mode="RGB").filter(ImageFilter.GaussianBlur(radius = 4)))
                index += 1
            
        ret_images[0].save(modified_gif, save_all=True, append_images = ret_images[1:], duration = 60, loop = 0)