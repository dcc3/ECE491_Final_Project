import Multispectral
import cv2
import numpy as np
import sys


myImage = cv2.imread(sys.argv[1], 1)




height = myImage.shape[0]
width = myImage.shape[1]




data = Multispectral.Flatten(myImage)	

labels, centers = Multispectral.MultiKMeans(6, data)

resultImage = Multispectral.MarkupRGBImage(myImage, labels)

cv2.imwrite("test_output_set6.jpg", resultImage)

reduced_data = Multispectral.PCAReduction(2,data)

labels1, centers1 = Multispectral.MultiKMeans(6, reduced_data)

reduced_resultImage = Multispectral.MarkupRGBImage(myImage, labels1)

cv2.imwrite("test_output_pca_set6.jpg", reduced_resultImage)