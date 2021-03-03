# Resize images from the "images" folder and put the resized images in the "resized" folder.
# If the height of the image is greater than the width by 1.5 (portrait), crop the image to capture
# the top half of the image (usually contains faces and more striking features of the artwork).
# After cropping, resize the images such that the shortest side of the image is 512px wide.

from multiprocessing import Process
from tqdm import tqdm
from PIL import Image
import numpy as np
import os, cv2

#imgPath = os.path.join(os.getcwd(), 'images')
imgPath = os.path.join(os.getcwd(), 'metfaces1024')
augPath = os.path.join(os.getcwd(), 'resizedMet')
resizeSize = 256
files = os.listdir(imgPath)

def augChunk(start, end, size=512):
    for i in tqdm(range(start, end)):
        try:
            img = Image.open(os.path.join(imgPath, files[i]))
            w, h = img.size

            if h > w * 1.5:
                img = img.crop((0, 0, w, int(w*1.5))) # left, top, right, bottom
            w, h = img.size
            scale = size / min(w, h)
            new_w, new_h = int(w * scale), int(h * scale)

            if new_w < size: # rounding sometimes makes numbers into 511 instead of 512
                new_w = size
            if new_h < size:
                new_h = size
            newSize = (new_w, new_h)

            img = img.resize(newSize)

            os.chdir(augPath)
            img.save(files[i])
            os.chdir(imgPath)

        except Exception as e:
            os.chdir(imgPath)
            print(e)

if __name__ == '__main__':
    try:
        os.mkdir(augPath)
    except:
        print('Couldn\'t make resized folder, probably already exists.')

    numCores = 4
    numImgs = len(files)
    chunkSize = numImgs // numCores
    for i in range(numCores):
        start = i * chunkSize
        end = (i+1) * chunkSize
        if i == numCores-1:
            end = numImgs

        #p = Process(target=augChunk, args=(start, end))
        p = Process(target=augChunk, args=(start, end, resizeSize))
        p.start()
