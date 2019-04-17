import numpy as np
import sys
import cv2 as cv
import os

np.set_printoptions(threshold=sys.maxsize)

""" Merge will take a python list of opencv images and stack them all into one 'image'
	imgs: Python list of opencv images
	returns:
			output: (height x width x number of input images) numpy array
"""
def Merge(imgs):
	
	output = np.zeros((imgs[0].shape[0],imgs[0].shape[1],len(imgs)),np.uint8)
	
	for i in range(len(imgs)):
		tmp = imgs[i].copy()

		output[:,:,i] = tmp

	return output


""" Open takes a directory from the user and traverses and opens all bmp images in the file as grey scale images
	and generates a list to be passed to merge. The return is a (height x width x number of input images) numpy array
	directory: directory housing multispectral images
	returns:
			img_merge: numpy array of merge images (height x width x inputs)
"""
def Open(directory):
	image_list = []
	for dirname,subdir,filelist in os.walk(sys.argv[1]):
		for fname in sorted(filelist):
			if '.bmp' in fname:
				img_tmp = cv.imread(dirname+fname,0)
				image_list.append(img_tmp)
				
	img_merge = Merge(image_list)
	print(img_merge.shape)
	return img_merge

def MultispectralToBGR(image):
	blue = np.zeros((image.shape[0],image.shape[1]),np.uint8)
	green = np.zeros((image.shape[0],image.shape[1]),np.uint8)
	red = np.zeros((image.shape[0],image.shape[1]),np.uint8)

	blue = np.mean(image[:,:,3:8],2)
	green = np.mean(image[:,:,10:15],2)
	red = np.mean(image[:,:,20:26],2)

	output = Merge((blue,green,red))
	return output


image = Open(sys.argv[1])

output = MultispectralToBGR(image)

cv.imshow("test",output)
cv.waitKey(0)







