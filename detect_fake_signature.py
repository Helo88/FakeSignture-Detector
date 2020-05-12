import cv2 as cv
from orb_algo import match_orb
from surf_algo import match_surf

#img1-4: four real signatures of a person
img1 = cv.imread("008008_000.png",0)
img2 =cv.imread("008008_001.png",0)
img3 = cv.imread("008008_003.png",0)
img4 =cv.imread("008008_004.png",0)

#test: a signature to be tested
test=cv.imread("021008_001.png",0)

lst_img=[img1,img2,img3,img4]
good_orb=[]
good_surf=[]
test_orb=[]
test_surf=[]
i=0
th=0.75

#match each two images of real signatures with ORB and Surf , store the number of good points in good_orb and good_surf
while(i<len(lst_img)-1):
    j=i+1
    while(j<len(lst_img)):
        good_orb.append(match_orb(lst_img[i],lst_img[j],th))
        good_surf.append(match_surf(lst_img[i], lst_img[j], th))
        j+=1
    i+=1

#threshold_orb: average number of good matched points between img1-4 using ORB
threshold_orb = sum(good_orb)/len(good_orb)

#threshold_surf: average number of good matched points between img1-4 using Surf
threshold_surf = sum(good_surf)/len(good_surf)

#match test with img1-4
for img in lst_img:
    test_orb.append(match_orb(img,test,th))
    test_surf.append(match_surf(img, test, th))

result_orb=''
strength_orb=0
result_surf=''
strength_surf=0

#if good matches between test and any real signature exceed the threshold then it is verified
if(max(test_orb)>=threshold_orb):
    result_orb='Verified'
    strength_orb=(max(test_orb)-threshold_orb)/threshold_orb
else:
   result_orb='Forged'
   strength_orb = (threshold_orb-max(test_orb))/threshold_orb

if(max(test_surf)>=threshold_surf):
    result_surf='Verified'
    strength_surf = (max(test_surf) - threshold_surf)/threshold_surf
else:
    result_surf='Forged'
    strength_surf = (threshold_surf - max(test_surf))/threshold_surf

if(result_surf==result_orb):
    print(result_surf)
else:
    if(strength_surf>strength_orb):
        print(result_surf)
    else:
        print(result_orb)
