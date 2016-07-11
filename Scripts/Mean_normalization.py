import os
import numpy as np 
import glob
from scipy.misc import imread
import h5py
# import pdb

DATA_PATH = '~/FortusDataset_DR_Detection/Data/training_set_class_balanced'
MEAN_IMAGE_PATH = '~/FortusDataset_DR_Detection/Data/'
OUTPUT_DATA_DIR = '~/FortusDataset_DR_Detection/Data/train_data_mean_normalized'
paths = glob.glob(DATA_PATH+'/*jpg')
Fortus_labels = ['N','H','L','T']
# h5f = h5py.File("Fortus_dataset.h5", 'w')

# array_of_images = []
# array_of_labels = []
mean_image = np.load(os.path.join(MEAN_IMAGE_PATH, 'Fortus_mean_image.npz'), 'r')['arr_0']
# pdb.set_trace()
count = 0
for path in paths:
	image = imread(path).astype(np.float64)
	mean_normalized_image = image - mean_image
	mean_normalized_image = mean_normalized_image.reshape(-1)
	#Add labels
	label = Fortus_labels.index(path.split('/')[-1][0])

	np.savez_compressed(os.path.join(OUTPUT_DATA_DIR, path.split('/')[-1]), image=image, label=label)
	# array_of_images.append(mean_normalized_image)
	# array_of_labels.append(label)

	count += 1
	if count % 100 == 0:
		print "Images processed: %d" % count

# h5f.create_dataset('X_train', data=array_of_images)
# h5f.create_dataset('y_train', data=array_of_labels)
# h5f.close()
