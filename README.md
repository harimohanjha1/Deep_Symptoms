&emsp;&emsp;&emsp;&emsp;
##Deep Learning for Detection of Clinical Symptoms of the Retina in Color Fundus Images




Diabetic retinopathy is when damage occurs to the retina due to diabetes. It can eventually lead to blindness. It is an ocular manifestation of diabetes, a systemic disease, which affects up to 80 percent of all patients who have had diabetes for 20 years or more. If we can detect this, and get in there as early as possible, then 98% of the most severe visual loss might be prevented.Training a neural network to do the assessment of eye scans could vastly increase both the speed and accuracy of diagnosis, potentially saving the sight of thousands.In experimental evaluation with the FORTUS
database, we achieve the objective of disease detection with
maximum average accuracy of 78%.
<hr>
##Clinical Symptoms For Retina In FORTUS Dataset

Hemorrhage             |  Lesions           | Tesselated_Fundus             |  Normal
:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:
<img src="https://github.com/harimohanjha1/Deep_Symptoms/blob/master/images/Hemorrhage.jpg?raw=True" width="100"> | <img src="https://github.com/harimohanjha1/Deep_Symptoms/blob/master/images/Lesions.jpg?raw=True" width="100"> | <img src="https://github.com/harimohanjha1/Deep_Symptoms/blob/master/images/Tesselated_Fundus.jpg?raw=True" width="100"> | <img src="https://github.com/harimohanjha1/Deep_Symptoms/blob/master/images/Normal.jpg?raw=True" width="100">

<hr>

<hr>
## Proposed Method

**Convolutional neural networks** (CNN or ConvNet) are a special category of artificial neural networks designed for processing data with a gridlike structure. The ConvNet architecture is based on sparse interactions and parameter sharing and is highly effective for efficient learning of spatial invariances in images. There are four kinds of layers in a typical ConvNet architecture: convolutional (conv), pooling (pool), fullyconnected (affine) and rectifying linear unit (ReLU). Each convolutional layer transforms one set of feature maps into another set of feature maps by convolution with a set of filters.

This model makes an attempt to classify the given dataset into different symptoms training a Convolutional Neural Network (ConvNets) on raw color fundus images which may help in diagnosis of Diabetic Retinopathy

**Dataset**: The  ConvNets is evaluated by learning with the FORTUS data set which is divided in proportion of 4:1 for training and testing purpose.

**Learning mechanism**: Each ConvNet is trained independently on a set of randomly chosen 3Ã—152Ã—205 patches.
Learning rate was kept constant across models at 5e âˆ’ 4. Images were loaded in batches with BATCH_SIZE=30 and were resized to 3*154*205 for training and testing purpose. The models were trained using Adam algorithm with the minibatch size . 

<hr>


##(Schematic representation below)

<img src="https://raw.githubusercontent.com/harimohanjha1/Deep_Symptoms/master/images/process_flow_diag.jpg" width="800">

<hr>

#Folders In This Repo

The data used for this model has not been included in this repository. Only the samples for each symptoms have been included. In order to describe the process of for classification of images notebooks and scripts have been loaded with proper explanation as follows :-

***Images*** 

Contains images of each of the three symptoms specified and one normal fundus image.

***Scripts***

- `Train_Mean_image.py` - Calculates Mean Image from training set for normalization procedure

- `Mean_Normalization.py` - Performs Mean nOrmalization on dataset to produce mean-normalized data for training purpose
- `Fortus_data_validation.ipynb, Fortus_data_validation.py` - Trains the Convolutional Neural Network and there by Calculates     the Precision of It's Prediction
- `Label.py`- Create labels of training set
- `Partition.py`- Partition Data into Training, Validation and Test Images




&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;


***Setup***
 ```Project
 |-Project
  |--Data
   |--Diseases
     |--Hemorrhage
     |--Lesions
     |--Tesselated_Fundus
     |--Normal
  |-- Fortus_mean_image.npz
  |-- image_copy_recur.sh
  |-- img_resize.py
  |-- label.py(Extract labels for training data)
  |-- train_labels.txt
  |-- numpy_image.tar.gz
  |-- test_labels.txt
  |-- training_set_class_balancedFortus_mean_image.npz
  |-- val_labels.txt

 |-- Utilities
|-- calculate_training_set_mean.py
|-- Fortus_Data_Validation.ipynb
|-- Fortus_Data_Validation.py
|-- Fortus_mean_image.npz
|-- mean_normalize_Fortus_images.py
|-- mean_normalize.py
``` 
