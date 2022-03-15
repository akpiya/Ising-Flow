import os
import glob

directory = "../data/image_frames/"
prefix = "vec_piv_FFT_"
suffix = "_med_thrhld_repl.vec"
offsets = [2]
T = [2.25]

def find_files(temp):
	counter = len(glob.glob1(temp, "*repl.vec"))
	return counter

def standardize(t, offset, valid):
	name = "UnbluredGifOffset="+str(offset)+"_T="+("%.2f" % t)
	files = find_files(directory + name + "/")
	if valid:
		for i in range(files):
			filename = directory + name + "/" + prefix + "{:03d}".format(i) + suffix
			# if deletion:	
			#	  with open(filename,"r") as textobj:
			#		  a = list(textobj)    #puts all lines in a list

			#	  del a[0]	  #delete regarding element

			#	  #rewrite the textfile from list contents/elements:
			#	  with open(filename,"w") as textobj:
			#		  for n in a:
			#			  textobj.write(n)

			with open(filename,"r") as f:
				contents = f.readlines()
			contents.insert(0,"x\ty\tu\tv\tmask\tsig2noise\n")
			with open(filename,"w") as f:
				contents = "".join(contents)
				f.write(contents)

def delete_top(t, offset, valid):
	name = "GifOffset="+str(offset)+"_T="+("%.2f" % t)
	files = find_files(directory + name + "/")
	if valid:
		for i in range(files):
			filename = directory + name + "/" + prefix + "{:03d}".format(i) + suffix
			with open(filename,"r") as textobj:
				a = list(textobj)	 #puts all lines in a list

			del a[0]	#delete regarding element

			#rewrite the textfile from list contents/elements:
			with open(filename,"w") as textobj:
				for n in a:
					textobj.write(n)

if __name__ == "__main__":
	
	for offset in offsets:
		for t in T:
			standardize(t, offset, True)
			delete_top(t, offset, False)

