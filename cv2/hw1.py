import cv2
import time # for time.time()

#----- Adjustable Parameters ----# 

STRIDE = 15 # 9, 11 ,15 ,21, 31
SEARCH_RANGE =30

#------ Constant(Don't modify) ------# 
OUTPUT_FILE = 'result/' + str(STRIDE) + '*' + str(STRIDE) + "_range" + str(SEARCH_RANGE) + ".bmp"
STRIDE_HALF = (STRIDE-1)//2
SEARCH_LIST = [] 
for i in range(-SEARCH_RANGE,SEARCH_RANGE,1):
    for j in range(-SEARCH_RANGE,SEARCH_RANGE,1):
        SEARCH_LIST.append((i,j))

def getROI(center, img):
    '''
    Return img ROI in original img, 
    Return None,  if any pixel exceeds map boundary
    Input : 
        center : (x,y)
    Output : 
        img (ROI)
    '''
    (x,y) = center
    (h, w) = img.shape
    # Boundary check 
    if  0 <= x-STRIDE_HALF   < w and\
        0 <= x+STRIDE_HALF+1 < w and\
        0 <= y-STRIDE_HALF   < h and\
        0 <= y+STRIDE_HALF+1 < h:
        return img[y-STRIDE_HALF : y+STRIDE_HALF+1, x-STRIDE_HALF : x+STRIDE_HALF+1]
    else:
        return None 

def getDiff(img_a, img_b):
    '''
    return int difference between two imgs.  
    '''
    (h, w) = img_b.shape
    sum = 0
    for y in range(h): # Col
        for x in range(w): # Row
            # This method is slower then abs(), int()
            '''
            (a, b) = (img_a[y][x], img_b[y][x])
            if a >= b:
                sum += a - b
            else:
                sum += b - a
            '''
            sum += abs(int(img_a[y][x]) - int(img_b[y][x])) # Avoid uint8 overflow
    return sum

def getBestfit(center,img_s, img_t):
    '''
    Input : 
        img_s : image source, imgA
        img_t : image target, imgB's ROI
        center: center point
    Output : 
        return bestpt = (x,y)
    '''
    (x,y) = center
    (h, w) = img_s.shape
    min_disparity = float('inf')
    min_center = (0,0)
    # ----- Search range -------#
    for tentative_dcenter in SEARCH_LIST:
        (t_x, t_y) = (x + tentative_dcenter[0], y + tentative_dcenter[1])

        # Boundary check
        if not (0 <= t_x < w  and  0 <= t_y < h):
            continue
        
        t_roi = getROI((t_x,t_y) , img_s)
        # check t_ros is legal ROI
        try:
            len(t_roi)
        except:
            continue
        else:
            pass 
        # Get tentative disparity image
        tentative_dis = getDiff(t_roi, img_t)
        if tentative_dis < min_disparity:
            # Update min value
            min_disparity = tentative_dis
            min_center = (t_x,t_y)
    print ("min_disparity : " + str(min_disparity))
    print ("min_center : " + str(min_center))
    return min_center

def main ():
    start_time = time.time()

    # img is a 3D array : 
    # img[0] -> first row of img
    # img[0][0] -> first element (up-right corner) of img with RGB 3 channel
    imgA = cv2.imread('trucka.bmp',cv2.IMREAD_GRAYSCALE)
    imgB = cv2.imread('truckb.bmp',cv2.IMREAD_GRAYSCALE)

    # Get img info.
    (h, w) = imgA.shape
    print("width={}, height={}".format(w, h))

    min_centers = [] # List of bestfit  centers
    ori_centers = [] # List of original centers
        
    for y in range(STRIDE_HALF ,h , STRIDE): # Col
        for x in range(STRIDE_HALF , w , STRIDE): # Row
            roi_b = getROI( (x,y) ,imgB) # Get target ROI
            try:
                len(roi_b)
            except:
                continue
            else: # If is legal ROI
                ori_centers.append((x,y))
                min_centers.append(getBestfit((x,y) ,imgA ,roi_b)) # Get bestfit ROI

    img_output = cv2.cvtColor(imgA, cv2.COLOR_GRAY2BGR)
    #---- draw arrow on image A -----# 
    for i in range(len(ori_centers)):
        #                      pt1        pt2         color
        cv2.arrowedLine(img_output, min_centers[i], ori_centers[i], (0, 255, 0), thickness=1, line_type=cv2.LINE_4, shift=0, tipLength=0.1)

    print("--- %s seconds ---" % (time.time() - start_time))

    cv2.imshow('img_output', img_output) # Show image
    cv2.imwrite(OUTPUT_FILE, img_output) # Output picture
    cv2.waitKey(0)
    cv2.destroyAllWindows()
main()