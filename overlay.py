import cv2 as cv
import sys

image = cv.imread(sys.argv[1])
shape = image.shape

overlay = image[:,(int(shape[1]/2)):shape[1]]#,:]
background = image[:,:(int(shape[1]/2))]#,:]
added_image = cv.addWeighted(background,0.75,overlay,0.3,0)

cv.imshow("test",added_image)
cv.waitKey(0)

#cv2.imwrite('combined.png', added_image)
