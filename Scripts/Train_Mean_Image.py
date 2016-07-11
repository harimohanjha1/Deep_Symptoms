from __future__ import division
import os
import numpy as np 
import glob
from scipy.misc import imread

DATA_PATH = '~/FortusDataset_DR_Detection/Data/training_set_class_balanced'

paths = glob.glob(DATA_PATH+'/*jpg')

sample_image = imread(paths[0])

mean_image = np.zeros_like(sample_image)
count = 0

for path in paths:
	image = imread(path)
	mean_image = (mean_image*count+image)/(count+1)
	count += 1

np.savez('Fortus_mean_image.npz', mean_image)
