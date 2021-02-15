import numpy as np
import os, time
from PIL import Image
from tqdm import tqdm

def add(path, startIndex=3): # startIndex=4 works for img(number here) named images
    os.chdir(path)
    files = os.listdir()
    files.sort()
    for i in tqdm(files):
        filler = ''
        for j in range(16 - len(i)):
            filler += '0'
        os.rename(i, (i[:startIndex] +  filler + i[startIndex:]))
 
def rescale(factor, path):
    os.chdir(path)
    for i in tqdm(os.listdir()):
        try:
            img = Image.open(i)
            new_w = int(img.size[0] * factor)
            new_h = int(img.size[1] * factor)
            resized = img.resize((new_w, new_h))
            resized.save(i)
        except Exception as e:
            print(e)
    os.chdir('..')

def dist(p1, p2):
    deltas = []
    for i in range(len(p1)):
        deltas.append(p1[i]-p2[i])
    
    ssum = 0
    for i in range(len(deltas)):
        ssum += deltas[i]**2
    
    return ssum ** 0.5
def alphize(pilObj, bw=None, bgCol=None, customCol=None, thresh=30):
    copy = pilObj.convert('RGBA')
    pix = pilObj.getdata()
    
    if customCol != None:
        midCol = customCol

    elif bgCol != 0:
        if bw == 1:
            midCol = (240,)
        else:
            midCol = (240, 240, 240)
    else:
        if bw == 1:
            midCol = (15,)
        else:
            midCol = (15, 15, 15)

    newWat = []

    pixArr = np.array(pix)
    col4D = np.array([customCol[0], customCol[1], customCol[2], 0])
    pixArr = np.concatenate((pixArr, 255*np.ones((pixArr.shape[0], 1), dtype=int)), axis=1)
    newWat = np.array(pixArr, copy=True)
    dists = np.sum((pixArr - col4D) ** 2, axis=1) - 255 ** 2 
    newWat[dists < thresh ** 2] = np.array([255, 255, 255, 0])
    newWat = list(newWat)
    for i in range(len(newWat)):
        newWat[i] = tuple(newWat[i])

    copy.putdata(tuple(newWat))
    return copy

def copy(path, newPath, normPath='/home/tcrasher'):
    toPath = newPath
    os.chdir(path)
    for i in os.listdir():
        try:
            img = Image.open(i)
            try:
                os.chdir(toPath)
            except:
                print('Making directory.')
                os.chdir(normPath)
                dirName = str(time.time())
                os.mkdir(dirName)
                toPath = os.path.join(normPath, dirName)
                os.chdir(toPath)
            img.save(i)
            os.chdir(path)
        except Exception as e:
            print(e)
            os.chdir(path)
    
    return toPath
