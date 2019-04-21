
from Multispectral import *
import sys
import random

from sklearn.datasets.samples_generator import make_blobs

""" If using Mean shift, give a 3 argument if you want to use a given bandwidth, otherwise it will be estimated

"""
def main():

	imageset = sys.argv[1]
	method = sys.argv[2]
	spatial = sys.argv[3]

	elements = imageset.split("/")
	sub = elements[1].split("_")
	
	filename = sub[0]+sub[1]+"_"+method+"_"+spatial
	if spatial == "s":
		spatial = 1
	else:
		spatial = 0
		
	
	if method == "ms":
		
		multispectral = Open(imageset)
		data =Flatten(multispectral,spatial)

		color_image = MultispectralToBGR(multispectral)
		data_c = Flatten(color_image,spatial)

		print(len(sys.argv))
		if(len(sys.argv) <= 4):	
			labels, centers, bandwidth = MultiMeanShift(data)
			labels_c, centers_c, bandwidth_c = MultiMeanShift(data_c)
		else:
			labels, centers ,bandwidth= MultiMeanShift(data,int(sys.argv[4]))
			labels_c, centers_c, bandwidth_c = MultiMeanShift(data_c,int(sys.argv[4]))

		filename += "_"+str(bandwidth)
		
		output = MarkupRGBImage(color_image,labels,NULL_ARR)
		output_c = MarkupRGBImage(color_image,labels_c,NULL_ARR)


	elif method == "km":
		k = int(sys.argv[4])
		filename += "_"+str(k)

		multispectral = Open(imageset)
		color_image = MultispectralToBGR(multispectral,spatial)

		data = Flatten(multispectral,spatial)	
		data_c = Flatten(color_image,spatial)


		labels, centers = MultiKMeans(k, data)
		labels_c, centers_c = MultiKMeans(k, data_c)

		output = MarkupRGBImage(color_image, labels, NULL_ARR)
		output_c = MarkupRGBImage(color_image, labels_c, NULL_ARR)
	
	
	elif method == "msp":
		
		multispectral = Open(imageset)
		data =Flatten(multispectral,spatial)

		color_image = MultispectralToBGR(multispectral)

		
		
		
		if(len(sys.argv) <= 5):	
			pca = int(sys.argv[4])
			data = PCAReduction(pca,data)
			labels, centers, bandwidth = MultiMeanShift(data)
		else:
			pca = int(sys.argv[5])
			data = PCAReduction(pca,data)
			labels, centers ,bandwidth= MultiMeanShift(data,int(sys.argv[4]))

		filename += "_"+str(bandwidth)+"_"+str(pca)
		
		output = MarkupRGBImage(color_image,labels,NULL_ARR)
	elif method == "kmp":
		k = int(sys.argv[4])
		pca = int(sys.argv[5])
		data = PCAReduction(pca,data)
		filename += "_"+str(k)+"_"+str(pca)

		multispectral = Open(imageset)
		color_image = MultispectralToBGR(multispectral)

		data = Flatten(multispectral,spatial)	



		labels, centers = MultiKMeans(k, data)

		output = MarkupRGBImage(color_image, labels, NULL_ARR)

	
	filename +=".jpg"
	output = np.concatenate((color_image,output),axis=1)
	
	cv.imwrite(filename,output)


if __name__ == "__main__":
	main()
