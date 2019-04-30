
import cv2 as cv
import numpy as np
import random
import sys
random.seed(110)
def convertData(image_name,colors,output):
	#image_name = output+".png"
	#print image_name
	img = cv.imread(image_name,3)
	
	unique = set( tuple(v) for m2d in img for v in m2d )
	shape = img.shape
	rows = shape[0]
	cols = shape[1]
	img2 = np.ndarray(shape)
	for i in range(rows):
		for j in range(cols):
			color = img[i,j,0]
			if color > 10:
				color = 0
			img2[i,j,0] = colors[color][0]
			img2[i,j,1] = colors[color][1]
			img2[i,j,2] = colors[color][2]
		

	cv.imwrite(output,img2)
r = 0
g = 0
b = 0
colors = []
while(1):
	if (r,g,b) not in colors:
		colors.append((r,g,b))
	r = random.randint(0,255)
	g = random.randint(0,255)
	b = random.randint(0,255)
	if len(colors) == 152:
		break




convertData(sys.argv[1],colors,sys.argv[2])

