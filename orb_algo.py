#match_orb return the number of good matched points between two images using ORB
def match_orb(img1,img2,thr):
    orb = cv.ORB_create()
    kp, des = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)
    bf = cv.BFMatcher(cv.NORM_HAMMING)
    matches = bf.knnMatch(des, des2, k=2)
    good_points = []
    for m, n in matches:
        if m.distance < thr * n.distance:
            good_points.append(m)
    return len(good_points)
