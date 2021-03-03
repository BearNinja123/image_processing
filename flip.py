# Flip images horizontall from the "resized" folder and put the resized images in the "flipped" folder.

from multiprocessing import Process
from tqdm import tqdm
from PIL import Image
import numpy as np
import os, cv2

#imgPath = os.path.join(os.getcwd(), 'images')
imgPath = os.path.join(os.getcwd(), 'resizedMet')
augPath = os.path.join(os.getcwd(), 'flippedMet')
files = os.listdir(imgPath)

def augChunk(start, end):
    for i in tqdm(range(start, end)):
        try:
            img = Image.open(os.path.join(imgPath, files[i]))
            img.save(files[i])

            flipped = img.transpose(method=Image.FLIP_LEFT_RIGHT)
            flipped.save(files[i][:-4] + '_F' + files[i][-4:]) # .jpg/.png extensions

        except Exception as e:
            #os.chdir(imgPath)
            print(e)

if __name__ == '__main__':
    try:
        os.mkdir(augPath)
    except:
        print('Couldn\'t make resized folder, probably already exists.')

    os.chdir(augPath)
    numCores = 4
    numImgs = len(files)
    chunkSize = numImgs // numCores
    for i in range(numCores):
        start = i * chunkSize
        end = (i+1) * chunkSize
        if i == numCores-1:
            end = numImgs

        p = Process(target=augChunk, args=(start, end))
        p.start()
