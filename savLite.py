from multiprocessing import Process
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import cv2, os, warnings, joblib

np.random.seed(0)
warnings.filterwarnings('ignore')

def lprint(g):
    print('\n\n\n{}\n\n\n'.format(g))

def vectorizer(folderNum, prefix='Files', toFolder='npArrs'):
    lite = []
    os.chdir('{}_{}'.format(prefix, folderNum))
    files = os.listdir()
    for i in tqdm(files):
        array = plt.imread(i)
        if np.max(array) > 1:
            print('y')
            raise
            array = array.astype(np.float16)
        else:
            array = (2 * array - 1).astype(np.float16)

        try:
            if array.shape == imgSize:
                lite.append(array)
            elif array.shape == imgSize[:-1]:
                lite.append(np.repeat(np.expand_dims(array, -1), 3, axis=2))
            else:
                print(array.shape)
        except:
            pass
    lite = np.array(lite).astype(np.float16)
    #print(lite.shape)
    os.chdir(os.path.join(parentPath, toFolder))
    strI = str(int(folderNum/1000))
    if(len(strI)) < 2:
        strI = '0' + strI
    np.save('imgs{}.npy'.format(strI), lite)


parentPath = os.getcwd()
path = 'thumbnails128x128-Folderized'
toFolder = 'npArrsFFHQ'
imgSize = (128, 128, 3)
os.chdir(path)
folders = os.listdir()
folders.sort()
print(folders)
numCores = 4

'''
try:
    os.mkdir(os.path.join(parentPath, toFolder))
except:
    pass

for i in range(len(folders) // numCores):
    processes = []
    for j in range(4):
        folderNum = (numCores * i + j) * 1000
        if folderNum / 1000 < len(folders): # Files_1000 vs 28 folders
            p = Process(target=vectorizer, args=(folderNum, 'Files', toFolder))
            processes.append(p)
            p.start()

    for j in processes:
        j.join()
        '''

processes = []
for i in range(len(folders) % numCores):
    folderNum = (numCores * (len(folders) // numCores) + i) * 1000
    if folderNum / 1000 < len(folders): # Files_1000 vs 28 folders
        p = Process(target=vectorizer, args=(folderNum, 'Files', toFolder))
        processes.append(p)
        p.start()

for j in processes:
    j.join()
