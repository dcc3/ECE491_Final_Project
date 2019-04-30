import cv2 as cv
import numpy as np
import sys
from math import sqrt
import time

poi = 20

square = 21

def distance(p1,p2):
	#print(p1)
	#print(p2)
	
	return sqrt(((p1[0]-p2[0])**2) + ((p1[1]-p2[1])**2) +((p1[2]-p2[2])**2))

def avg_area(point,image,square):
	
	
	avg_b = 0
	avg_g = 0
	avg_r = 0
	shape = image.shape
	bound = int(square/2)
	if (point[0] - bound) < 0 or  (point[1] - bound) < 0 or (point[0] + bound) > shape[0] or (point[1] + bound) > shape[1] :
		return (0,0,0)
	
	
	for i in range(-bound,bound):
		for j in range(-bound,bound):
			i_t = i + point[0]
			j_t = point[1]+j
			avg_b += image[i_t,j_t,0]
			avg_g += image[i_t,j_t,1]
			avg_r += image[i_t,j_t,2]

	s = square**2
	return avg_b/s,avg_g/s,avg_r/s

start = time.time()
label = cv.imread(sys.argv[1],0)
test_image = cv.imread(sys.argv[2],1)

fin = open("../colors.txt","r")
keys = []

for line in fin:
	tmp = line.strip('\n').split(" ")
	keys.append((int(tmp[0]),int(tmp[1]),int(tmp[2])))

keys = keys[:poi]

shape = test_image.shape
#print(shape)
test_image = test_image[:,(int(shape[1]/2)):shape[1]]#,:]
shape = test_image.shape


label1 = np.where(label==7)
print(len(label1[0]))
label1 = np.where(label==8)
print(len(label1[0]))
label1 = np.where(label==9)
print(len(label1[0]))
label1 = np.where(label==6)
print(len(label1[0]))
label1 = np.where(label==5)
print(len(label1[0]))
label1 = np.where(label==4)
print(len(label1[0]))
label1 = np.where(label==3)
print(len(label1[0]))
label1 = np.where(label==2)
print(len(label1[0]))
label1 = np.where(label==1)
print(len(label1[0]))
exit()
c = []
for i in range(len(label1[0])):

	c.append((label1[0][i],label1[1][i]))
colors = []
colors.append((0,0,0))
for x in range(shape[0]):
	for y in range(shape[1]):
		#x = points[0]
		#y = points[1]
		color = (test_image[x,y,0],test_image[x,y,1],test_image[x,y,2])#avg_area(points,test_image,square)
		#print("Color:",color)
		dist = 1000000
		for k in keys:
			dist_t = distance(color,k)
			if dist_t < dist:
				master_k = k
				dist = dist_t
				#if k not in colors:
				#	colors.append(k)
				#	print(color)
		test_image[x,y,0] = master_k[0]
		test_image[x,y,1] = master_k[1]
		test_image[x,y,2] = master_k[2]
		if master_k not in colors:
			colors.append(master_k)
		
			print("Matched Point:",master_k)




#cv.imshow("test",test_image)
#cv.waitKey(0)

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
