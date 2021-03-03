# have the program runner look into each image of a directory, wait long = remove that image from dataset, wait short = keep

import matplotlib.pyplot as plt
from numpy.linalg import norm
from PIL import Image
import numpy as np
import os, time

rmPath = os.path.join(os.getcwd(), 'resized')
os.chdir(rmPath)
files = os.listdir()
for i in files:
    imgPath = os.path.join(os.getcwd(), i)
    img = np.array(Image.open(i))
    if norm(img[0][0]) < 50: # black outline - remove
        os.remove(imgPath)
    elif norm(img[0][0]) > norm(np.array([255, 255, 255])) * 0.9: # white outline - remove
        os.remove(imgPath)
    elif len(img.shape) == 2 or np.mean(np.std(img, axis=2)) < 10: # bw images - remove
        os.remove(imgPath)
    elif norm(img[5][5] - img[-1-5][5]) < 30 and norm(img[5][-1-5] - img[-1-5][-1-5]) < 30: # general outline - remove
        #os.remove(imgPath)
        pass
    else:
        print(int(norm(img[0][0])), np.mean(np.std(img, axis=2)))
        plt.imshow(img)
        start = time.time()
        plt.show()
        duration = time.time() - start
        if duration < 1:
            #os.remove(i)
            pass
        #pass
