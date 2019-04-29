import cv2 as cv
import numpy as np
import sys
from math import sqrt

label = cv.imread(sys.argv[1],0)
test_image = cv.imread(sys.argv[2],1)
shape = test_image.shape
print(shape)
test_image = test_image[:,(int(shape[1]/2)):shape[1]]#,:]
shape = test_image.shape
print(shape)
for i in range(4):
	for j in range(4):
		print(test_image[i,j,0],test_image[i,j,1],test_image[i,j,2])


cv.imshow("test",test_image)
cv.waitKey(0)
exit()

label1 = np.where(label==1)

c = []
for i in range(len(label1[0])):

	c.append((label1[0][i],label1[1][i]))
colors = []
colors.append((0,0,0))
for points in c:
	x = points[0]
	y = points[1]
	color = (test_image[x,y,0],test_image[x,y,1],test_image[x,y,2])
	if color not in colors:
		dist = 10000
		for tmp in colors:
			dist_t = sqrt(((color[0]-tmp[0])**2) + ((color[1]-tmp[1])**2) +((color[2]-tmp[2])**2))
			
			if dist_t < dist:
				dist = dist_t

		if dist >100:
			print(color)
			colors.append(color)
