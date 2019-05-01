
from Multispectral import *
import sys
import random

from sklearn.datasets.samples_generator import make_blobs

""" 
This is the main file of the project. From this function kmeans and mean shift will be called a passed the appropriate values.
argv[1]: the path to a folder containing multispectral images. 
argv[2]: ns (non-spatial) or s (spatial)
argv[3]: km (k-means), ms (meanshift), kmp (kmeans using pca), msp ( meanshift using pca)
argv[4]: either the k value for k-means or the bandwidth for mean shift.
argv[5]: if using pca this is the pca value.

output:
	set{}_method_spatial_k/bandwidth(_pca).jpg this is the processed multispectral output.
	set{}_method_spatial_k/bandwidth(_pca)_c.jpg this is the processed RGB output.

Both images are concatenated with the original RGB image. 

"""
def main():

	imageset = sys.argv[1]
	spatial = sys.argv[2]
	method = sys.argv[3]

	elements = imageset.split("/")
	sub = elements[1].split("_")
	
	filename = sub[0]+sub[1]+"_"+method+"_"+spatial
	
	#converting spatial to a value to drop into code
	if spatial == "s":
		spatial = 1
	else:
		spatial = 0
		
	#process data with mean shift
	if method == "ms":

		multispectral = Open(imageset)
		data =Flatten(multispectral,spatial = spatial)

		color_image = MultispectralToBGR(multispectral)
		data_c = Flatten(color_image,spatial = spatial)

		labels, centers ,bandwidth= MultiMeanShift(data,int(sys.argv[4]))
		labels_c, centers_c, bandwidth_c = MultiMeanShift(data_c,int(sys.argv[4]))

		
		filename += "_"+str(int(bandwidth))
		
		output = MarkupRGBImage(color_image,labels,NULL_ARR)
		output_c = MarkupRGBImage(color_image,labels_c,NULL_ARR)

	#process data with k means
	elif method == "km":
		k = int(sys.argv[4])
		filename += "_"+str(k)

		multispectral = Open(imageset)
		color_image = MultispectralToBGR(multispectral)

		data = Flatten(multispectral,spatial=spatial)	
		data_c = Flatten(color_image,spatial=spatial)


		labels, centers = MultiKMeans(k, data)
		labels_c, centers_c = MultiKMeans(k, data_c)

		output = MarkupRGBImage(color_image, labels, NULL_ARR)
		output_c = MarkupRGBImage(color_image, labels_c, NULL_ARR)
	
	#process data with mean shift and PCA
	elif method == "msp":
		
		multispectral = Open(imageset)
		data =Flatten(multispectral,spatial=spatial)

		color_image = MultispectralToBGR(multispectral)	
		data_c =Flatten(color_image,spatial=spatial)
		
		
		pca = int(sys.argv[6])
		data = PCAReduction(pca,data)
		labels, centers ,bandwidth= MultiMeanShift(data,int(sys.argv[4]))
		labels_c, centers_c, bandwidth_c = MultiMeanShift(data_c,int(sys.argv[4]))

		filename += "_"+str(int(bandwidth))+"_"+str(pca)
		
		output = MarkupRGBImage(color_image,labels,NULL_ARR)
		output_c = MarkupRGBImage(color_image,labels_c,NULL_ARR)
	#process data with k-means and PCA
	elif method == "kmp":
		k = int(sys.argv[4])
		pca = int(sys.argv[5])

		multispectral = Open(imageset)
		color_image = MultispectralToBGR(multispectral)

		data = Flatten(multispectral,spatial=spatial)	
		data_c = Flatten(color_image,spatial=spatial)	
		
		data = PCAReduction(pca,data)
		filename += "_"+str(k)+"_"+str(pca)



		labels, centers = MultiKMeans(k, data)
		labels_c, centers_c = MultiKMeans(k, data_c)

		output = MarkupRGBImage(color_image, labels, NULL_ARR)
		output_c = MarkupRGBImage(color_image, labels_c, NULL_ARR)
	
	filename_c = filename + "_c.jpg"
	filename +=".jpg"

	output = np.concatenate((color_image,output),axis=1)
	output_c = np.concatenate((color_image,output_c),axis=1)
	


	cv.imwrite(filename,output)
	cv.imwrite(filename_c,output_c)


if __name__ == "__main__":
	main()
