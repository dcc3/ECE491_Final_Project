
import numpy as np
import sys
import cv2 as cv
import os
import random
import sklearn
from sklearn.cluster import KMeans
from sklearn import decomposition
from sklearn.cluster import MeanShift,estimate_bandwidth

np.set_printoptions(threshold=sys.maxsize)

NULL_ARR = [[0]]


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


def Flatten(multispectral,spatial=0):
	s = multispectral.shape
	if spatial == 0:
		test = np.zeros((s[0]*s[1],s[2]))
	
	elif spatial ==1:
		test = np.zeros((s[0]*s[1],s[2]+2))

	print("--- Flattening ---")
	for r in range(multispectral.shape[0]):
		for c in range(multispectral.shape[1]):
			if spatial == 0:
				test[r*s[1] + c,:] = multispectral[r,c,:]
			elif spatial == 1:
				test[r*s[1] + c,:s[2]] = multispectral[r,c,:]
				test[r*s[1] + c,s[2]] = (float(r)/float(multispectral.shape[0]))*255.0
				test[r*s[1] + c,s[2]+1] = (float(c)/float(multispectral.shape[1]))*255.0
	

	return test
	
""" 
Description: 	Wraps SKLearn library's KMeans function for use in our project 
Inputs: 		k_clusters - # of clusters to predict
				data - list of features
Outputs:		labels - list of lables associated with pixels
				centroids - list of cluster center coordinates
"""
def MultiKMeans(k_clusters, data):
	
	# Set the number of clusters
	kmeans = KMeans(n_clusters=k_clusters)

	print("Kmeans: Fitting data...")
	# Fit data to number of clusters
	kmeans = kmeans.fit(data)

	print("Kmeans: Predicting labels...")
	# Determine labels from fitting
	labels = kmeans.predict(data)
		
	print("Kmeans: Calculating cluster centers...")
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
def MarkupRGBImage(rgbImg, labels, centers):

	height = rgbImg.shape[0]
	width = rgbImg.shape[1]
	
	# holds result
	segmentedImage = np.zeros([height,width,3],np.uint8)
	
	# Create a list of random colors based on number of labels
	label_list = len(np.unique(labels))
	
	
	blue = []
	green = []
	red = []
	"""
	colors = []
	# assign random color for each label
	if len(centers[0]) < 3:
		while(len(blue) < label_list):
			
			b = random.randint(0,255)
			g = random.randint(0,255)
			r = random.randint(0,255)
			if b not in blue and g not in green and r not in red:
				blue.append(b)
				green.append(g)
				red.append(r)
	else:
		for c in centers:
			print(c)
			blue.append(c[0])
			green.append(c[1])
			red.append(c[2])
	"""
	fin = open("colors.txt",'r')

	for line in fin:
		tmp = line.strip('\n').split(" ")
		blue.append(int(tmp[0]))
		green.append(int(tmp[1]))
		red.append(int(tmp[2]))



	pixel = 0
	print("Psuedo coloring cluster labels into RGB output...")
	for i in range(0,height):
		for j in range(0, width): 
			#if (image[j,i] != 0): # ignore black
						
			lab = int(labels[pixel])			
			
			segmentedImage[i,j,0] = blue[lab]
			segmentedImage[i,j,1] = green[lab]
			segmentedImage[i,j,2] = red[lab]

			pixel = pixel + 1
	print(segmentedImage.shape)
	return segmentedImage

""" 
Description: 	Wraps SKLearn library's PCA function for use in our project 
Inputs: 		target_features - how many features to reduce to
				data - list of features
Outputs:		reduced_data - PCA reduced data set
"""	
def PCAReduction(number_target_features, data):

	print("Using PCA to reduce used features for segmentation to: " + str(number_target_features))
	pca = decomposition.PCA(n_components=number_target_features) #3
	pca.fit(data)
	reduced_data = pca.transform(data)

	return reduced_data
	
def MultiMeanShift(data,bandwidth=-1):
	
		rand_indices = np.random.randint(0,data.shape[0],int(data.shape[0]*.6))
		test_train = data[rand_indices]
		if bandwidth == -1:
			print("--- Estimating Bandwidth ---")
			bandwidth = estimate_bandwidth(data,quantile=.3,n_samples=int(test_train.shape[0]*.05))
			print("Estimated Bandwidth:",bandwidth)
		
		print("--- Fitting Dataset ---")
		clusters = MeanShift(bandwidth=bandwidth,bin_seeding=True,n_jobs=4)
		labels = clusters.fit(test_train)
		labels = clusters.predict(data)
		print(np.unique(labels))
		centers = clusters.cluster_centers_

		return labels,centers,bandwidth






