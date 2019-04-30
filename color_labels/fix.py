import cv2 as cv 
import numpy as np
import sys


img = cv.imread(sys.argv[1],0)
img2 = img.copy()
print(np.unique(img))
img2[img > int(sys.argv[2])]=0
img2 = cv.cvtColor(img2,cv.COLOR_GRAY2BGR)
cv.imwrite(sys.argv[3],img2)

