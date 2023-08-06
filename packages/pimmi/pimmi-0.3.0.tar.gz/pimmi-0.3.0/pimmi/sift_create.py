import cv2 as cv

img = cv.imread('/home/bmazoyer/Downloads/PXL_20221018_144602040.jpg')
gray= cv.cvtColor(img,cv.COLOR_BGR2GRAY)
sift = cv.SIFT_create()
kp = sift.detect(gray,None)
img=cv.drawKeypoints(gray,kp,img, color=(125,0,0))
cv.imwrite('sift_keypoints.jpg',img)