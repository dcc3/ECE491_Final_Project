import cv2 as cv
import sys
import os



for dirname,subdir,filelist in os.walk(sys.argv[1]):
	for fname in sorted(filelist):
		image = cv.imread(dirname+fname,1)
		shape = image.shape
		
		tmp = fname.split(".")
		outname= tmp[0]+"_m."+tmp[1]

		overlay = image[:,(int(shape[1]/2)):shape[1]]#,:]
		background = image[:,:(int(shape[1]/2))]#,:]
		added_image = cv.addWeighted(background,0.85,overlay,0.25,0)

		cv.imwrite(dirname+outname, added_image)
