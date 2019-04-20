import sklearn
import cv2
import numpy as np
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt


class MultispectralKMeans:
	
	def __init__(self):
		pass
	
	# Wraps SKLearn library's KMeans function for use in our project
	def calculateLabels(self, k_clusters, data):
	
		# Set the number of clusters
		kmeans = KMeans(n_clusters=k_clusters)

		# Fit data to number of clusters
		kmeans = kmeans.fit(data)

		# Determine labels from fitting
		labels = kmeans.predict(data)
		
		# Coordinates of clusters
		centroids = kmeans.cluster_centers_
	
	
		return labels, centroids


	def markupImage(self, rgbImg, labels):
	
		# Set to upper limit of 50 labels
		label_list = len(np.unique(labels))
		blue = [0]*label_list
		green = [0]*label_list
		red = [0]*label_list
		
		# assign random color for each label
		for lab in range(0,label_list):
			blue[lab] = random.randint(0,255)
			green[lab] = random.randint(0,255)
			red[lab] = random.randint(0,255)
	
		# Color component pixels
		for i in range(0,width):
			for j in range(0, height): 
				#if (image[j,i] != 0): # ignore black
				lab = int(image[j,i])
				color_image[j,i,0] = blue[lab]
				color_image[j,i,1] = green[lab]
				color_image[j,i,2] = red[lab]
	
		return segmentedImage


# reference below

#https://mubaris.com/posts/kmeans-clustering/
#see bottom half for sklearn implementation

#f1 = np.array([4, 5, 6, 7])
#f2 = np.array([1, 2, 3, 4])

f1 = np.random.randint(200, size=100)
f2 = np.random.randint(200, size=100)

X = np.array(list(zip(f1, f2)))

k_clusters = 4
# Set the number of clusters
kmeans = KMeans(n_clusters=k_clusters)

# Fit data to number of clusters
kmeans = kmeans.fit(X)

# Determine labels from fitting
labels = kmeans.predict(X)



# Get centroids
centroids = kmeans.cluster_centers_
print(centroids)
c_x = []
c_y = []
for c in centroids:
	c_x.append(c[0])
	c_y.append(c[1])
	

i = 0
for p in range(0, len(X)):
	a = X[i]
	if labels[p] == 0:
		plt.scatter(a[0], a[1], c='red', s= 7)
	if labels[p] == 1:
		plt.scatter(a[0], a[1], c='blue', s= 7)
	if labels[p] == 2:
		plt.scatter(a[0], a[1], c='green', s= 7)
	if labels[p] == 3:
		plt.scatter(a[0], a[1], c='yellow', s= 7)
	i = i +1
		
#plt.scatter(f1, f2, c='black', s=7)
plt.scatter(c_x, c_y, c='black', marker='*', s=50)

plt.savefig('foo.pdf')















exit()
# Eventually make kmeans into a class to call
class kmeans():

	def __init__(self):
	
		pass


	def cluster(self, ):
	
	
		return x