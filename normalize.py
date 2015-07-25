import numpy as np
import cv2
import sys
from matplotlib import pyplot as plt

def __getDetector():
    # return cv2.ORB_create()
    return cv2.AKAZE_create()

def __calcKpAndDes(imgName, mask = None):
    img = cv2.imread(imgName, 0)
    return (img,) + __getDetector().detectAndCompute(img, mask)

def __getMatcher():
    return cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

def showImg(img):
    plt.imshow(img),plt.show()

def drawKp(img, kp):
    img = cv2.drawKeypoints(img, kp, outImage = None, color = (0, 255, 255))
    plt.imshow(img),plt.show()

def getBoardMask():
    # サイズから空イメージ作れればいい
    boardImg = cv2.imread('pics/board.jpg', cv2.IMREAD_GRAYSCALE)
    isInMask = lambda x, y: x < 91 or x > 585 or y < 182 or y > 842
    isInLogo = lambda x, y: 192 < x < 500 and 855 < y < 940
    for x in range(0, 687):
        for y in range(0, 1033):
            boardImg[y][x] = 255 if isInMask(x, y) else 0
            # boardImg[y][x] = 255 if isInLogo(x, y) else 0
    return boardImg

def drawMatches(img1, kp1, img2, kp2, matches):
    img = cv2.drawMatches(img1, kp1, img2, kp2, matches[:10], flags=2, outImg = None)
    plt.imshow(img),plt.show()

def __doMatching(des1, des2):
    return sorted(__getMatcher().match(des1, des2), key = lambda x:x.distance)

def __getMatchedPts(qKp, tKp, matches):
    qPts = np.float32([ qKp[m.queryIdx].pt for m in matches ]).reshape(-1,1,2)
    tPts = np.float32([ tKp[m.trainIdx].pt for m in matches ]).reshape(-1,1,2)
    return qPts, tPts

def __findHomography(srcPts, destPts):
    return cv2.findHomography(srcPts, destPts, cv2.RANSAC, 5.0)

# 入力画像に判定結果の盤境界を表示する
def showBoardEdges(qImg, tImg, qPts, tPts):
    M, _ = __findHomography(qPts, tPts)
    h,w = qImg.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)
    img = cv2.polylines(tImg,[np.int32(dst)],True,255,3, cv2.LINE_AA)
    showImg(img)

def normalizeImg(imgFile):
    query = 'pics/board.jpg'
    train = imgFile

    # 特徴点抽出
    qImg, qKp, qDes = __calcKpAndDes(query, getBoardMask())
    tImg, tKp, tDes = __calcKpAndDes(train)

    matches    = __doMatching(qDes, tDes)
    qPts, tPts = __getMatchedPts(qKp, tKp, matches)
    M, mask    = __findHomography(tPts, qPts)

    # TODO: 写像のサイズ (持ち駒判断)
    img = cv2.warpPerspective(tImg, M, tuple(np.array([qImg.shape[1], qImg.shape[0]])))
    return img

train = sys.argv[1]

img = normalizeImg(train)
showImg(img)

# cv2.imwrite('result.png', img)
