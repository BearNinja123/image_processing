# Sample (x, w) or a (w, y) (default w = 512) image from 'flipped' folder into several maxW x maxH (default is 256x256) images. Files put into 'sampled' folder

from multiprocessing import Process
from random import randint
from PIL import Image
from tqdm import tqdm
from numpy import sin, cos, tan, pi
from numpy import random as npr
import numpy as np
import os

def d(x):
    return pi * x / 180

sampleFromFolder = os.path.join(os.getcwd(), 'flipped')
sampleToFolder = os.path.join(os.getcwd(), 'sampled')
maxW, maxH = 256, 256
maxRot = 5
#maxW, maxH = 32, 32

def find(liste, s=None, sArray=None):
    ret = []
    if s != None:
        for i in liste:
            if s in i:
                ret.append(i)
    else:
        for i in liste:
            for s in sArray:
                if s in i:
                    ret.append(i)
                    break
    return ret

def samplePoisson(img, xSampleMax, ySampleMax, sigma=3):
    xSample = npr.normal(xSampleMax//2, scale=xSampleMax // (sigma * 2)) # x sigma on both sides 
    xSample = int(min(max(xSample, 0), xSampleMax))
    ySample = npr.poisson(ySampleMax // 5)
    ySample = int(min(max(ySample, 0), ySampleMax))
    sampledImg = img.crop((xSample, ySample, xSample+maxW, ySample+maxH))
    return sampledImg

def sampleValidImage(img, imgW, imgH, thetaSeen):
    xSampleMin = int(maxH * cos(thetaSeen) * sin(thetaSeen))
    xSampleMax = int(imgW - xSampleMin - maxW)
    ySampleMin = int(maxW * cos(thetaSeen) * sin(thetaSeen))
    ySampleMax = int(imgH - ySampleMin - maxH)
    if xSampleMin > xSampleMax or ySampleMin > ySampleMax or min(xSampleMin, xSampleMax) < 0 or min(ySampleMin, ySampleMax) < 0:
        return -1

    xSample = randint(xSampleMin, xSampleMax)
    ySample = randint(ySampleMin, ySampleMax)
    
    cropImg = img.crop((xSample, ySample, xSample+maxW, ySample+maxH))
    arr = np.array(cropImg)

    if len(arr.shape) == 2: # bw image
        arr = np.repeat(np.expand_dims(arr, -1), 3, axis=2)

    if sum(arr[0][0]) == 0 or sum(arr[0][0]) == 0 or sum(arr[0][-1]) == 0 or sum(arr[-1][0]) == 0 or sum(arr[-1][-1]) == 0:
        return -1
    return cropImg

files = os.listdir(sampleFromFolder)
#files = find(files, sArray=['Monet', 'Gogh', 'Pissarro', 'Sisley', 'Cezanne', 'Gauguin', 'Pierre', 'Mikhail', 'Munch', 'Greco', 'Dali', 'Manet', 'Matisse', 'Lautrec'])

def sampleImgs(start, end, numSampled=4, rotateChange=0.0):
    for i in tqdm(files[start:end]):
        try:
            img = Image.open(os.path.join(sampleFromFolder, i))
            w, h = img.size
            xSampleMax, ySampleMax = w - maxW, h - maxH # max bounds for left and top coordinates for sampled image

            os.chdir(sampleToFolder)
            for j in range(numSampled):
                rotAngle = 0

                # theta seen:

                # | /
                # |/
                # |\
                # |_\ <-- angle here
                # |  \
                # |   \
                # |    \

                if randint(0, 1) == 0:
                    rotAngle = randint(1, maxRot)
                    thetaSeen = d(rotAngle) # thetaSeen is the angle under the point where the corner touches the left side of the image 
                else:
                    rotAngle = randint(360-maxRot, 359)
                    thetaSeen = d(rotAngle - 270) # math stuff explains the -270
                rotImg = img.rotate(rotAngle, expand=1)

                if randint(1, 100) <= int(100 * rotateChange):
                    tries = 0
                    sampledImg = 0
                    while type(sampledImg) == int and tries < 10:
                        sampledImg = sampleValidImage(rotImg, w, h, thetaSeen)
                        tries += 1

                    if(type(sampledImg) == int):
                        xSample = randint(0, xSampleMax)
                        ySample = randint(0, ySampleMax)
                        
                        #sampledImg = img.crop((xSample, ySample, xSample+maxW, ySample+maxH))
                        sampledImg = samplePoisson(img, xSampleMax, ySampleMax)
                else:
                    xSample = randint(0, xSampleMax)
                    ySample = randint(0, ySampleMax)
                    
                    
                    #sampledImg = img.crop((xSample, ySample, xSample+maxW, ySample+maxH))
                    sampledImg = samplePoisson(img, xSampleMax, ySampleMax)

                width, height = sampledImg.size
                assert sampledImg.size == (maxW, maxH)
                saveName = '{}_{}.png'.format(i[:-4], j)
                sampledImg.save(saveName)

            os.chdir(sampleFromFolder)
        except Exception as e:
            os.chdir(sampleFromFolder)
            print(i, width, height, width-xSampleMax, height-ySampleMax, xSampleMax, ySampleMax, e)
            raise

if __name__ == '__main__':
    try:
        os.mkdir(sampleToFolder)
    except:
        print('Couldn\'t make folder to put in sampled images, probably already exists.')

    numCores = 4
    for i in range(numCores):
        chunkSize = int(len(files) / numCores)
        start = i * chunkSize
        end = (i + 1) * chunkSize
        if i == numCores - 1:
            end = len(files)

        p = Process(target=sampleImgs, args=(start, end))
        p.start()
