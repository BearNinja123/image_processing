import os, sys, shutil, zeroAdder, random
from tqdm import tqdm

#initPath = sys.argv[1]
#accPath = sys.argv[2]
initPath = os.getcwd()
accPath = 'flippedMet'

zeroAdder.add(os.path.join(initPath, accPath), 0)
os.chdir(initPath)

fldr = '{}-Folderized'.format(accPath)

try:
	os.mkdir(fldr)
except:
	print('Dir already exists.')

os.chdir(os.path.join(initPath, accPath))
allFiles = os.listdir()
random.shuffle(allFiles) # we actually want the files to be shuffled because it allows greater training variety
currFldr = 'Files_0'
for i in tqdm(range(len(allFiles))):
	if i % 1000 == 0:
		currFldr = 'Files_{}'.format(i)
		try:
			os.chdir(os.path.join(initPath, fldr))
			os.mkdir('Files_{}'.format(i))
		except Exception as e:
			print(e)
	try:
		shutil.copy(os.path.join(initPath, accPath, allFiles[i]), os.path.join(initPath, fldr, currFldr))
	except:
		print('{} denied.'.format(os.path.join(initPath, accPath, allFiles[i])))
