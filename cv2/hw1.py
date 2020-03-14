import numpy as np
import cv2
import time 
# from matplotlib import pyplot as plt

STRIDE = 31 # 9, 11 ,15 ,21, 31
STRIDE_HALF = (STRIDE-1)//2
SEARCH_RANGE = 20
SEARCH_LIST = [] 
for i in range(-SEARCH_RANGE,SEARCH_RANGE,1):
    for j in range(-SEARCH_RANGE,SEARCH_RANGE,1):
        SEARCH_LIST.append((i,j))
print (SEARCH_LIST) # [(-50,-50), (-50, -49), ..... (50,50)]

def getROI(center, img):
    '''
    Return img ROI in original img, 
    Return NOne , if exceed map boundary
    Input : 
        center : (x,y)
    Output : 
        img (ROI)
    '''
    (x,y) = center
    # Boundary check 
    if x-STRIDE_HALF   < 0 or x-STRIDE_HALF   > w-1 or\
       x+STRIDE_HALF+1 < 0 or x+STRIDE_HALF+1 > h-1 or\
       y-STRIDE_HALF   < 0 or y-STRIDE_HALF   > w-1 or\
       y+STRIDE_HALF+1 < 0 or y+STRIDE_HALF+1 > h-1 :
        return None 

    return img[x-STRIDE_HALF : x+STRIDE_HALF+1 , y-STRIDE_HALF : y+STRIDE_HALF+1]

def getAbsAvg(img):
    '''
    return double 
    '''
    (h, w, d) = img.shape
    sum = 0
    for y in range(h): # Col
        for x in range(w): # Row
            sum += abs(img[y][x][0])
    return sum# /(h*w)

# RGB 3 channel all have identical value.
start_time = time.time()
# 讀取圖檔
# img is a 3D array : 
# img[0] -> first row of img
# img[0][0] -> first element (up-right corner) of img with RGB 3 channel
imgA = cv2.imread('trucka.bmp')
imgB = cv2.imread('truckb.bmp')
# 以灰階的方式讀取圖檔
# img_gray = cv2.imread('trucka.bmp', cv2.IMREAD_GRAYSCALE)


# Get img info.
(h, w, d) = imgA.shape
print("width={}, height={}, depth={}".format(w, h, d))

min_centers = []
ori_centers = []
for y in range(STRIDE_HALF ,h , STRIDE): # Col
    for x in range(STRIDE_HALF , w , STRIDE): # Row
        roi_a = getROI( (x,y) ,imgA)
        roi_b = getROI( (x,y) ,imgB)

        ori_centers.append((x,y))
        
        # ----- Search range -------#
        min_disparity = float('inf')
        min_center = (0,0)
        for tentative_dcenter in SEARCH_LIST:
            t_x = x + tentative_dcenter[0]
            t_y = y + tentative_dcenter[1]
            
            # Boundary check 
            if t_x < 0 or t_x > w-1 or t_y < 0 or t_y > h-1:
                continue
            
            t_roi = getROI((t_x,t_y) , imgA)
            try:
                len(t_roi)
            except:
                continue
            else:
                pass 
            t_dis = getAbsAvg(t_roi - roi_b)
            
            if t_dis < min_disparity:
                min_disparity = t_dis
                min_center = (t_x,t_y)
        
        print ("min_disparity : " + str(min_disparity))
        print ("min_center : " + str(min_center))
        min_centers.append(min_center)
        if (x,y) == (STRIDE_HALF,STRIDE_HALF):
            cv2.imshow("ROI_A", roi_a)
            cv2.imshow("ROI_B", roi_b)
            #cv2.imshow("disparity_img", disparity_img)
            pass 
        # print (imgA[y][x][0])
        # print (imgB[y][x][0])

# Cut an ROI 
# roi = img[60:160, 320:420]
# cv2.imshow("ROI", roi)
# 顯示圖片

#---- add arrow to image A -----# 
for i in range(len(ori_centers)):
    #                      pt1        pt2         color
    cv2.arrowedLine(imgA, ori_centers[i], min_centers[i], (0, 0, 255), thickness=1, line_type=cv2.LINE_4, shift=0, tipLength=0.1)
    
print("--- %s seconds ---" % (time.time() - start_time))

cv2.imshow('trucka', imgA)
#cv2.imshow('truckb', imgB)
# 按下任意鍵則關閉所有視窗
cv2.waitKey(0)
cv2.destroyAllWindows()

'''
# 使用 OpenCV 讀取圖檔
img_bgr = cv2.imread('trucka.bmp')

# 將 BGR 圖片轉為 RGB 圖片
img_rgb = img_bgr[:,:,::-1]

# 或是這樣亦可
# img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

# 使用 Matplotlib 顯示圖片
plt.imshow(img_rgb)
plt.show()
'''