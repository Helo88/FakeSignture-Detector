    def match_surf(self, img1, img2, thr):
        surf = cv.xfeatures2d.SURF_create() #create surf obj extract all features
        kp1, des1 = surf.detectAndCompute(img1, None)#find the keypoints and descriptors
        kp2, des2 = surf.detectAndCompute(img2, None) #find the keypoints and descriptors
        FLANN_INDEX_KDTREE = 0  #checks=50 & trees=5 r default args
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)  # or pass empty dictionary
        flann = cv.FlannBasedMatcher(index_params, search_params) #create FlannBasedMatcher object
        matches = flann.knnMatch(des1, des2, k=2) #Match descriptors. #k=2 cos of me comparing 2 images at atime
        good_points = []
        # Apply ratio test
        for m, n in matches:
            if m.distance < thr * n.distance: # choose near good points
                good_points.append(m)
        return len(good_points)
