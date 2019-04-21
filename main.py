
from sklearn.cluster import MeanShift,estimate_bandwidth
from Multispectral import *
import sys
import random

from sklearn.datasets.samples_generator import make_blobs


def main():

	multispectral = Open(sys.argv[1])
	test =Flatten(multispectral)

	img = MultispectralToBGR(multispectral)

	#img = cv.imread(sys.argv[1],1)
	#img = cv.resize(img,(int(img.shape[1]/4),int(img.shape[0]/4)))

	#test = Flatten(img,spatial=1)
	
	rand_indices = np.random.randint(0,test.shape[0],int(test.shape[0]*.4))
	test_train = test[rand_indices]

	print("--- Estimating Bandwidth ---")
	bandwidth = estimate_bandwidth(test_train,quantile=.3,n_samples=100)
	print(bandwidth)

	print("--- Fitting Dataset ---")
	clusters = MeanShift(bandwidth=bandwidth,min_bin_freq=3,n_jobs=-1)
	clusters.fit(test_train)
	
	

	#print( clusters.cluster_centers_)

	labels = clusters.predict(test)
	
	output = MarkupRGBImage(img,labels)
	
	cv.imshow("test",output)
	cv.waitKey(0)


	#print(len(np.unique(labels)))


if __name__ == "__main__":
	main()
