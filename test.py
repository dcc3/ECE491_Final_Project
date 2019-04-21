import Multispectral
import cv2
import numpy as np
import sys


myImage = cv2.imread(sys.argv[1], 1)




height = myImage.shape[0]
width = myImage.shape[1]



# Kmeans full rgb
data = Multispectral.Flatten(myImage)	

labels, centers = Multispectral.MultiKMeans(6, data)

resultImage = Multispectral.MarkupRGBImage(myImage, labels)

cv2.imwrite("kmeans_set1_rgb_full.jpg", resultImage)


# Kmeans rgb PCA = 2
reduced_data = Multispectral.PCAReduction(2,data)

labels1, centers1 = Multispectral.MultiKMeans(6, reduced_data)

reduced_resultImage = Multispectral.MarkupRGBImage(myImage, labels1)

cv2.imwrite("kmeans_set1_rgb_pca2.jpg", reduced_resultImage)


# Kmeans rgb PCA = 1
reduced_data2 = Multispectral.PCAReduction(1,data)

labels2, centers2 = Multispectral.MultiKMeans(6, reduced_data2)

reduced_resultImage2 = Multispectral.MarkupRGBImage(myImage, labels2)

cv2.imwrite("kmeans_set1_rgb_pca1.jpg", reduced_resultImage2)