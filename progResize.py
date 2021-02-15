# Resize images from 256x256 into toSize x toSize

from multiprocessing import Process
from PIL import Image
from tqdm import tqdm
import numpy as np
import os, cv2

arrs = list(range(40))
inputPath = os.path.join(os.getcwd(), 'npArrs')
inputPath = os.path.join(os.getcwd(), 'arrResized')

def resizeChunk(toSize, path, num):
    arr = np.load(path).astype(np.float32)
    ret = []
    factor = toSize / 256
    for i in tqdm(arr):
        h, w = i.shape[0], i.shape[1]
        newH, newW = int(h * factor), int(w * factor)
        ret.append(cv2.resize(i, (newH, newW)))
    ret = np.array(ret).astype(np.float16)
    os.chdir(resizedPath)
    np.save('imgs{}_{}.npy'.format(num, toSize), ret)

numCores = 4
sizes = [32]

try:
    os.mkdir(resizedPath)
except:
    pass

for size in sizes:
    for arrNum in arrs:
        path = '{}/imgs{}.npy'.format(inputPath, arrNum)
        resizeChunk(size, path, arrNum)
        print(path)
        #p = Process(target=resizeChunk, args=(sizes[i], path, j))
        #p.start()
