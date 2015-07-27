import sys
import normalize as nm
import stones
import god
from matplotlib import pyplot as plt

train = sys.argv[1]
img, turn = nm.normalizeImg(train)
b = stones.getStones(img)
mv, ms = god.godMessage(b, turn)
print("次の一手は・・・・" + mv)
print(ms)
