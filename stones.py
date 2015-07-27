import numpy as np
import cv2
import sys
import normalize as nm
from matplotlib import pyplot as plt

def rotate(img, ang):
    rows, cols = img.shape
    M = cv2.getRotationMatrix2D((cols/2,rows/2), ang, 1)
    return cv2.warpAffine(img,M,(cols,rows))

def getMatchLocs(img, template):
    loc = ([], [])
    for tmpl in [rotate(template, d) for d in range(-70, 70, 3)]:
        res = cv2.matchTemplate(img,tmpl,cv2.TM_CCOEFF_NORMED)
        # 0.5 くらいにして曖昧なやつも候補として検出しておくと精度が良くなる
        threshold = 0.6
        x, y = np.where(res >= threshold)
        loc[0].extend(x)
        loc[1].extend(y)
    return loc

def getMatchImg(img, template):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    loc = getMatchLocs(img, template)
    w, h = template.shape[::-1]
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    return img_rgb

stones = {
        'hiyoko':   cv2.imread('pics/stones/hiyoko.png',   0),
        'lion':     cv2.imread('pics/stones/lion.png',     0),
        'zo':       cv2.imread('pics/stones/zo.png',       0),
        'kirin':    cv2.imread('pics/stones/kirin.png',    0),
        'niwatori': cv2.imread('pics/stones/niwatori.png', 0)
        }

symbols = {
        'hiyoko':   ('+HI', '-HI'),
        'lion':     ('+LI', '-LI'),
        'zo':       ('+ZO', '-ZO'),
        'kirin':    ('+KI', '-KI'),
        'niwatori': ('+NI', '-NI')
        }

TL = (91, 182)
BR = (585, 842)

def isValidPosition(x, y):
    return TL[0] <= x <= BR[0] and TL[1] <= y <= BR[1]

def getPosition(x, y):
    xx = int((x - TL[0]) / ((BR[0] - TL[0]) / 3))
    yy = int((y - TL[1]) / ((BR[1] - TL[1]) / 4))
    return xx, yy

# train = sys.argv[1]
# img = nm.normalizeImg(train)

# mimg = getMatchImg(img, rotate(stones['kirin'], 180))
# nm.showImg(mimg)
# exit()

def getStones(img):
    B = np.array([[" . "]*3]*4, dtype=object)
    for name, tmpl in stones.items():
        for turn in [0, 1]:
            if turn:
                tmpl = rotate(tmpl, 180)
            loc = getMatchLocs(img, tmpl)
            w, h = tmpl.shape[::-1]
            pos = []
            for x, y in zip(*loc[::-1]):
                x = x + w / 2
                y = y + h / 2
                if not isValidPosition(x, y):
                    continue
                pos.append(getPosition(x, y))
            for x, y in set(pos):
                B[y][x] = symbols[name][turn]
    return B.tolist()
