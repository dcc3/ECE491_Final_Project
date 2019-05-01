""" This script was written at the 11th hour and is what stream of consciousness programming would look like
argv[1]: label image
argv[2]: folder with images to process
argv[3]: number of objects in image
argv[4]: points of interest



"""

import cv2 as cv
import numpy as np
import sys
from math import sqrt
import time
import os
import csv

#this value is to make processing faster by only checking the top colors in color.txt
poi = int(sys.argv[4])

""" I use this function to return points from the ground truth that should all be in one class.
	image is the ground truth image, label is the color to look for.
"""
def Where(image,label):
	
	rows = image.shape[0]
	cols = image.shape[1]
	points = []
	for r in range(rows):
		for c in range(cols):
			tmp = (image[r,c,0],image[r,c,1],image[r,c,2])
			if tmp == label:
				points.append((r,c))
	return points
# Euclidean distance because you never know when you need to use it. 
def distance(p1,p2):
	return sqrt(((p1[0]-p2[0])**2) + ((p1[1]-p2[1])**2) +((p1[2]-p2[2])**2))


start = time.time()
label = cv.imread(sys.argv[1],1)
# uses the list of colors from the labels and the colors that were used in psuedo coloring to make this work. 
fin = open("colors_l.txt","r")
fin2 = open("colors.txt",'r')
key_labels = []
keys = []
key_count = {}
key_assign = {}
pca_val = ""


for line in fin:
	tmp = line.strip('\n').split(" ")
	key_labels.append((int(tmp[0]),int(tmp[1]),int(tmp[2])))
	key_assign[(int(tmp[0]),int(tmp[1]),int(tmp[2]))] = (0,0,0)
	

for _,line in zip(range(poi),fin2):
	tmp = line.strip('\n').split(" ")
	keys.append((int(tmp[0]),int(tmp[1]),int(tmp[2])))
	key_count[(int(tmp[0]),int(tmp[1]),int(tmp[2]))] = 0



spatial_multi = {}
spatial_rgb = {}
non_multi = {}
non_rgb = {}
output1 = ''
output2 = ''

for dirname,subdir,filelist in os.walk(sys.argv[2]):
	for fname in sorted(filelist):
		print(dirname+fname)
		hold = fname.strip('\n').strip('.jpg').split("_")
		output1 = hold[0]
		output2 = hold[1]
		method = hold[1]+hold[2]
		seg_size = hold[3]

		if hold[1] == 'kmp' or hold[1] == 'msp':
			pca_val = hold[4]
		
		test_image = cv.imread(dirname+fname,1)
		shape = test_image.shape
		test_image = test_image[:,(int(shape[1]/2)):shape[1]]#,:]
		shape = test_image.shape
		for val in key_assign.keys():
			key_assign[val] = (0,0,0)

		accuracy = 0
		for i in range(int(sys.argv[3])):
			#print(i)
			for val in key_count.keys():
				key_count[val] = 0
			labels = Where(label,key_labels[i])
			for points in labels:
					x = points[0]
					y = points[1]
					color = (test_image[x,y,0],test_image[x,y,1],test_image[x,y,2])
					dist = 1000000
					for k in keys:
						dist_t = distance(color,k)
						if dist_t < dist:
							master_k = k
							dist = dist_t
					
					key_count[master_k] +=1
					
			max_key = max(key_count, key=key_count.get)
			check = 0
			for val in key_assign.keys():
				if key_assign[val] == max_key:
					check = 1
					break

			if check == 0:
				key_assign[key_labels[i]] = max_key
				accuracy += key_count[max_key]

		

		accuracy = (accuracy/(shape[0]*shape[1]))*100
		if method == 'kmps' and hold[-1] != 'c':
			spatial_multi[pca_val] = accuracy
		elif method == 'kmps' and hold[-1] == 'c':
			spatial_rgb[pca_val] = accuracy
		elif method == 'kmpns' and hold[-1] != 'c':
			non_multi[pca_val] = accuracy
		elif method == 'kmpns' and hold[-1] == 'c':
			non_rgb[pca_val] = accuracy
		elif method == 'msps' and hold[-1] != 'c':
			spatial_multi[pca_val] = accuracy
		elif method == 'msps' and hold[-1] == 'c':
			spatial_rgb[pca_val] = accuracy
		elif method == 'mspns' and hold[-1] != 'c':
			non_multi[pca_val] = accuracy
		elif method == 'mspns' and hold[-1] == 'c':
			non_rgb[pca_val] = accuracy
		elif method == 'kms' and hold[-1] != 'c':
			spatial_multi[seg_size] = accuracy
		elif method == 'kms' and hold[-1] == 'c':
			spatial_rgb[seg_size] = accuracy
		elif method == 'kmns' and hold[-1] != 'c':
			non_multi[seg_size] = accuracy
		elif method == 'kmns' and hold[-1] == 'c':
			non_rgb[seg_size] = accuracy
		elif method == 'mss' and hold[-1] != 'c':
			spatial_multi[seg_size] = accuracy
		elif method == 'mss' and hold[-1] == 'c':
			spatial_rgb[seg_size] = accuracy
		elif method == 'msns' and hold[-1] != 'c':
			non_multi[seg_size] = accuracy
		elif method == 'msns' and hold[-1] == 'c':
			non_rgb[seg_size] = accuracy
		"""
		if method == 'kms' and hold[-1] != 'c':
			spatial_multi[seg_size] = accuracy
		elif method == 'kms' and hold[-1] == 'c':
			spatial_rgb[seg_size] = accuracy
		if method == 'kmns' and hold[-1] != 'c':
			non_multi[seg_size] = accuracy
		if method == 'kmns' and hold[-1] == 'c':
			non_rgb[seg_size] = accuracy
		"""


if pca_val == "":
	filename = output1+"_"+output2+'_spatial.csv'
else:
	filename = output1+"_"+output2+"_"+"pca"+'_spatial.csv'

with open(filename, mode='w') as f:
	fout = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	for k in sorted(spatial_multi.keys()):
		fout.writerow([k,spatial_multi[k]])
	

if pca_val == "":
	filename = output1+"_"+output2+'_rgb_spatial.csv'
else:
	filename = output1+"_"+output2+"_"+"pca"+'_rgb_spatial.csv'

with open(filename, mode='w') as f:
	fout = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	for k in sorted(spatial_rgb.keys()):
		fout.writerow([k,spatial_rgb[k]])

if pca_val == "":
	filename = output1+"_"+output2+'_non.csv'
else:
	filename = output1+"_"+output2+"_"+"pca"+'_non.csv'
with open(filename, mode='w') as f:
	fout = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	for k in sorted(non_multi.keys()):
		fout.writerow([k,non_multi[k]])

if pca_val == "":
	filename = output1+"_"+output2+'_rgb_non.csv'
else:
	filename = output1+"_"+output2+"_"+"pca"+'_rgb_non.csv'
#print(non_rgb)
with open(filename, mode='w') as f:
	fout = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	for k in sorted(non_rgb.keys()):
		fout.writerow([k,non_rgb[k]])




#cv.imshow("test",test_image)
#cv.waitKey(0)
print(key_assign)
end = time.time()

print(end-start)

"""
color = (test_image[x,y,0],test_image[x,y,1],test_image[x,y,2])
if color not in colors:
	dist = 10000
	for tmp in colors:
		dist_t = distance(color,tmp)
		
		if dist_t < dist:
			dist = dist_t

	if dist >100:
		print(color)
		colors.append(color)
"""
