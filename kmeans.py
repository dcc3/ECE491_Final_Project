import sklearn
import numpy as np
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt








# reference below

#https://mubaris.com/posts/kmeans-clustering/
#see bottom half for sklearn implementation

#f1 = np.array([4, 5, 6, 7])
#f2 = np.array([1, 2, 3, 4])

f1 = np.random.randint(200, size=100)
f2 = np.random.randint(200, size=100)

X = np.array(list(zip(f1, f2)))
print(X)
exit()

k_clusters = 4
# Set the number of clusters
kmeans = KMeans(n_clusters=k_clusters)

# Fit data to number of clusters
kmeans = kmeans.fit(X)

# Determine labels from fitting
labels = kmeans.predict(X)
print(labels)
exit()



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