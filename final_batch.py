
from Multispectral import *
import sys
import random

from sklearn.datasets.samples_generator import make_blobs

""" If using Mean shift, give a 3 argument if you want to use a given bandwidth, otherwise it will be estimated

"""
def main():

	if len(sys.argv) < 7:
		print("USAGE: python3 final_batch.py {ns/s} {km,ms,kmp,msp} {min range} {max} {step} o:{pca}")




	imageset = sys.argv[1]
	spatial = sys.argv[2]
	method = sys.argv[3]

	min_val = int(sys.argv[4])
	max_val = int(sys.argv[5])
	step_val = int(sys.argv[6])
	constant = int(sys.argv[7])
	
	elements = imageset.split("/")
	sub = elements[1].split("_")
	
	filename_o = sub[0]+sub[1]+"_"+method+"_"+spatial
	if spatial == "s":
		spatial = 1
	else:
		spatial = 0
		
	for val in range(min_val,max_val+step_val,step_val):
		filename = filename_o
		if method == "ms":
			
			multispectral = Open(imageset)
			data =Flatten(multispectral,spatial = spatial)

			color_image = MultispectralToBGR(multispectral)
			data_c = Flatten(color_image,spatial = spatial)

			labels, centers ,bandwidth= MultiMeanShift(data,val)
			labels_c, centers_c, bandwidth_c = MultiMeanShift(data_c,val)

			
			filename += "_"+str(int(bandwidth))
			print("------- {} -------".format(filename))
			output = MarkupRGBImage(color_image,labels,NULL_ARR)
			output_c = MarkupRGBImage(color_image,labels_c,NULL_ARR)


		elif method == "km":
			#k = int(sys.argv[4])
			filename += "_"+str(val)

			multispectral = Open(imageset)
			color_image = MultispectralToBGR(multispectral)

			data = Flatten(multispectral,spatial=spatial)	
			data_c = Flatten(color_image,spatial=spatial)


			labels, centers = MultiKMeans(val, data)
			labels_c, centers_c = MultiKMeans(val, data_c)

			output = MarkupRGBImage(color_image, labels, NULL_ARR)
			output_c = MarkupRGBImage(color_image, labels_c, NULL_ARR)
		
		
		elif method == "msp":
			
			multispectral = Open(imageset)
			data =Flatten(multispectral,spatial=spatial)

			color_image = MultispectralToBGR(multispectral)	
			data_c =Flatten(color_image,spatial=spatial)
			
			
			pca = val
			data = PCAReduction(pca,data)
			labels, centers ,bandwidth= MultiMeanShift(data,constant)
			labels_c, centers_c, bandwidth_c = MultiMeanShift(data_c,constant)

			filename += "_"+str(int(bandwidth))+"_"+str(pca)
			
			output = MarkupRGBImage(color_image,labels,NULL_ARR)
			output_c = MarkupRGBImage(color_image,labels_c,NULL_ARR)
		elif method == "kmp":
			k = constant
			pca = val

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
		elif method == "test":
			k = int(sys.argv[4])

			multispectral = Open(imageset)
			color_image = MultispectralToBGR(multispectral)

			data = Flatten(multispectral,spatial=spatial)	
			#data_c = Flatten(color_image,spatial=spatial)


			#labels, centers = MultiKMeans(k, data)
			labels, centers, bandwidth = MultiMeanShift(data,k)
			#labels_c, centers_c = MultiKMeans(k, data_c)

			output = MarkupRGBImage(color_image, labels, NULL_ARR)
			#output_c = MarkupRGBImage(color_image, labels_c, NULL_ARR)
			cv.imshow("test",output)
			cv.waitKey(0)
			exit()
	
		filename_c = filename + "_c.jpg"
		filename +=".jpg"

		output = np.concatenate((color_image,output),axis=1)
		output_c = np.concatenate((color_image,output_c),axis=1)
		


		cv.imwrite(filename,output)
		cv.imwrite(filename_c,output_c)


if __name__ == "__main__":
	main()
