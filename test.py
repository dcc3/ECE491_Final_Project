import Multispectral
import cv2
import numpy as np
import sys


myImage = cv2.imread(sys.argv[1], 1)


#my_size = 1280 * 1084
#labels = np.random.randint(2, size=my_size)

#data = Multispectral.Flatten(myImage)
#data should be a list of features (3 values for rgb image)

height = myImage.shape[0]
width = myImage.shape[1]

data = np.zeros([width*height,3])

pixel = 0
for i in range(0,width):
	for j in range(0, height): 
		data[pixel][0] = myImage[j][i][0]
		data[pixel][1] = myImage[j][i][1]
		data[pixel][2] = myImage[j][i][2]
		pixel = pixel + 1

		

labels, centers = Multispectral.MultiKMeans(30, data)

resultImage = Multispectral.MarkupRGBImage(myImage, labels)

cv2.imwrite("test_output.jpg", resultImage)