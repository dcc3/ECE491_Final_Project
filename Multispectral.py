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
""" NEED TO WRITE COMMENT: this gives you a bgr image from multispectral"""
def MultispectralToBGR(image):
	blue = np.zeros((image.shape[0],image.shape[1]),np.uint8)
	green = np.zeros((image.shape[0],image.shape[1]),np.uint8)
	red = np.zeros((image.shape[0],image.shape[1]),np.uint8)

	blue = np.mean(image[:,:,3:8],2)
	green = np.mean(image[:,:,10:15],2)
	red = np.mean(image[:,:,20:26],2)

	output = Merge((blue,green,red))
	return output


def Flatten(multispectral):
	s = multispectral.shape
	test = np.zeros((s[0]*s[1],s[2]))
	print("--- Flattening ---")
	for r in range(multispectral.shape[0]):
		for c in range(multispectral.shape[1]):
			test[r*s[1] + c,:] = multispectral[r,c,:]
	return test
	
""" 
Description: 	Wraps SKLearn library's KMeans function for use in our project 
Inputs: 		k_clusters - # of clusters to predict
				data - list of features
Outputs:		labels - list of lables associated with pixels
				centroids - list of cluster center coordinates
"""
def KMeans(k_clusters, data):
	
	# Set the number of clusters
	kmeans = KMeans(n_clusters=k_clusters)

	# Fit data to number of clusters
	kmeans = kmeans.fit(data)

	# Determine labels from fitting
	labels = kmeans.predict(data)
		
	# Coordinates of clusters
	centroids = kmeans.cluster_centers_
	
	
	return labels, centroids

""" 
Description: 	Takes RGB version of image and colors segements by label class 
				with a randomly generated color
Inputs: 		rgbImg - rgb version of multispectral image
				labels - list of lables associated with pixels
Outputs:		segmentedImage - rgb image marked up with segments
"""
def MarkupRGBImage(rgbImg, labels):
	
	# Create a list of random colors based on number of labels
	label_list = len(np.unique(labels))
	blue = [0]*label_list
	green = [0]*label_list
	red = [0]*label_list
		
	# assign random color for each label
	for lab in range(0,label_list):
		blue[lab] = random.randint(0,255)
		green[lab] = random.randint(0,255)
		red[lab] = random.randint(0,255)
	
	# Color component pixels
	for i in range(0,width):
		for j in range(0, height): 
			#if (image[j,i] != 0): # ignore black
			lab = int(image[j,i])
			color_image[j,i,0] = blue[lab]
			color_image[j,i,1] = green[lab]
			color_image[j,i,2] = red[lab]
	
	return segmentedImage
	
#image = Open(sys.argv[1])

#output = MultispectralToBGR(image)

#cv.imwrite(sys.argv[2],output)

#cv.imshow("test",output)
#cv.waitKey(0)







