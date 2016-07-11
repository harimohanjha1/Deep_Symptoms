
# coding: utf-8

# In[1]:
from __future__ import division
import numpy as np
import pandas as pd
import os
import glob
import tensorflow as tf

from skimage import io, transform
from skimage.transform import resize
from skimage.util import img_as_float, img_as_ubyte
import matplotlib.cm as cm
from matplotlib import pyplot as plt
from matplotlib import pyplot as plt

import time
import math
from six.moves import xrange


# In[2]:

DATA_PATH = '/users/TeamDiabeticRetinopathy/FortusDataset_DR_Detection/Data/train_data_mean_normalized'
data = glob.glob(DATA_PATH + '/*.jpg.npz')
NUM_CLASSES = 4 
NUM_HCONV1 =64
IMG_ROWS_BIG = 1536 
IMG_COLS_BIG = 2048 
IMAGE_PIXELS = IMG_COLS_BIG*IMG_ROWS_BIG 
IMG_ROWS_SMALL = 154 
IMG_COLS_SMALL = 205 
BATCH_SIZE = 30
LEARNING_RATE = 5e-6
TRAINING_PROP = 0.8 
MAX_STEPS = 15
HEIGHT = 1536
WIDTH = 2048
num = 1


# In[3]:

def placeholder_inputs(batch_size):
    """Generate placeholder variables to represent the input tensors.
    
    These placeholders are used as inputs by the rest of the model building
    code and will be fed from the downloaded data in the .run() loop, below.
    Args:
        batch_size: The batch size will be baked into both placeholders.
    Returns:
        images_placeholder: Images placeholder.
        labels_placeholder: Labels placeholder.
    """
    # Note that the shapes of the placeholders match the shapes of the full
    # image and label tensors, except the first dimension is now batch_size
    # rather than the full size of the train or test data sets.
    images_placeholder = tf.placeholder(tf.float32, shape=(BATCH_SIZE, IMG_ROWS_SMALL, IMG_COLS_SMALL, 3))
    labels_placeholder = tf.placeholder(tf.int32, shape=(BATCH_SIZE, NUM_CLASSES))
    return images_placeholder, labels_placeholder


# In[4]:

def inference(images, keep_prob, fc_hidden_units1=512):
    """ Builds the model as far as is required for running the network
    forward to make predictions.

    Args:
        images: Images placeholder, from inputs().
        keep_prob: Probability used for Droupout in the final Affine Layer
        fc_hidden_units1: Number of hidden neurons in final Affine layer
    Returns:
        softmax_linear: Output tensor with the computed logits.
    """
    
    with tf.variable_scope('h_conv1') as scope:
        weights = tf.get_variable('weights', shape=[4, 4, 3, NUM_HCONV1], 
                                  initializer=tf.contrib.layers.xavier_initializer())
        biases = tf.get_variable('biases', shape=[NUM_HCONV1])
        
        # Flattening the 3D image into a 1D array
        #x_image = tf.reshape(images, [-1,IMG_ROWS_SMALL, IMG_COLS_SMALL,3])
        z = tf.nn.conv2d(images, weights, strides=[1, 1, 1, 1], padding='VALID')
        h_conv1 = tf.nn.relu(z+biases, name=scope.name)
        print h_conv1.get_shape
    h_pool1 = tf.nn.max_pool(h_conv1, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME', name='h_pool1')
    print h_pool1.get_shape
    with tf.variable_scope('h_conv2') as scope:
        weights = tf.get_variable('weights', shape=[4, 4, 64, 64], 
                                  initializer=tf.contrib.layers.xavier_initializer())
        biases = tf.get_variable('biases', shape=[64])
        z = tf.nn.conv2d(h_pool1, weights, strides=[1, 1, 1, 1], padding='VALID')
        h_conv2 = tf.nn.relu(z+biases, name=scope.name)
        print h_conv2.get_shape
    
    h_pool2 = tf.nn.max_pool(h_conv2, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME', name='h_pool2')
    print h_pool2.get_shape
    
    with tf.variable_scope('h_fc1') as scope:
        code_shape = int(np.ceil((((IMG_ROWS_SMALL-3)/2.0)-3)/2.0)*np.ceil((((IMG_COLS_SMALL-3)/2.0)-3)/2.0))
        weights = tf.get_variable('weights', shape=[code_shape*NUM_HCONV1, NUM_CLASSES], 
                                  initializer=tf.contrib.layers.xavier_initializer())
        biases = tf.get_variable('biases', shape=[NUM_CLASSES])
        h_pool2_flat = tf.reshape(h_pool2, [-1, code_shape*NUM_HCONV1])
        
        
        logits = (tf.matmul(h_pool2_flat, weights) + biases)
        
    """
    with tf.name_scope('hidden1'):
    	weights = tf.Variable(tf.truncated_normal([IMAGE_PIXELS, fc_hidden_units1], stddev=1.0 / math.sqrt(float(IMAGE_PIXELS))),name='weights')
    	biases = tf.Variable(tf.zeros([fc_hidden_units1]),name='biases')
    
    hidden1 = tf.nn.relu(tf.matmul(images, weights) + biases)
    hidden2 = tf.nn.relu(tf.matmul(hidden1, weights) + biases)
    logits = tf.matmul(hidden2, weights) + biases

    """
    return logits


# In[5]:

def calc_loss(logits, labels):
    """Calculates the loss from the logits and the labels.
    Args:
        logits: Logits tensor, float - [batch_size, NUM_CLASSES].
        labels: Labels tensor, int32 - [batch_size].
    Returns:
        loss: Loss tensor of type float.
    """
    labels = tf.to_float(labels)
    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits, labels, name='xentropy')
    loss = tf.reduce_mean(cross_entropy, name='xentropy_mean')
    return loss


# In[6]:

#Done_3rd
def training(loss, learning_rate=5e-4):
    """Sets up the training Ops.
    Creates a summarizer to track the loss over time in TensorBoard.
    Creates an optimizer and applies the gradients to all trainable variables.
    The Op returned by this function is what must be passed to the
    `sess.run()` call to cause the model to train.
    Args:
        loss: Loss tensor, from loss().
        learning_rate: The learning rate to use for gradient descent.
    Returns:
        train_op: The Op for training.
    """
    # Add a scalar summary for the snapshot loss.
    tf.scalar_summary(loss.op.name, loss)
    # Create the Adam optimizer with the given learning rate.
    optimizer = tf.train.AdamOptimizer(learning_rate)
    # Create a variable to track the global step.
    global_step = tf.Variable(0, name='global_step', trainable=False)
    # Use the optimizer to apply the gradients that minimize the loss
    # (and also increment the global step counter) as a single training step.
    train_op = optimizer.minimize(loss, global_step=global_step)
    return train_op


# In[7]:

def evaluation(logits, labels, topk=1):
    """Evaluate the quality of the logits at predicting the label.
    Args:
        logits: Logits tensor, float - [batch_size, NUM_CLASSES].
        labels: Labels tensor, int32 - [batch_size], with values in the
                  range [0, NUM_CLASSES).
        topk: the number k for 'top-k accuracy'
    Returns:
        A scalar int32 tensor with the number of examples (out of batch_size)
        that were predicted correctly.
    """
    # For a classifier model, we can use the in_top_k Op.
    # It returns a bool tensor with shape [batch_size] that is true for
    # the examples where the label is in the top k (here k=1)
    # of all logits for that example.
    
    correct = tf.nn.in_top_k(logits, tf.reshape(tf.slice(labels, [0,1], [int(labels.get_shape()[0]), 1]),[-1]), topk)
    # Return the number of true entries.
    return tf.reduce_sum(tf.cast(correct, tf.int32))


# In[8]:

def next_batch(size, file_name_list, current_batch_ind):
	
    if current_batch_ind + size > len(file_name_list):
    	current_batch_ind =0
    	file_name_list = np.random.shuffle(file_name_list)

    
    """
      
         batch_x : np array to store pixel of image
         batch_y : np array to store label of image
         curr_list_of_file_names : part of the data set 
                                 consisting of the images and the labels 
                                 for current requested mini batch
    """

    batch_x = np.zeros((size, IMG_ROWS_SMALL, IMG_COLS_SMALL, 3), dtype=np.float64)
    batch_y = np.zeros((size, NUM_CLASSES), dtype = np.int64)
    curr_list_of_file_names = file_name_list[current_batch_ind:current_batch_ind+size-1]
    
    #print 'testing'
   
    file_id = 0
    for file_name in curr_list_of_file_names:
    	# loading file from data set curr_list_of_file_names
    	f = np.load(file_name,'r')
        #small = transform.resize(f['image'],(IMG_ROWS_SMALL,IMG_COLS_SMALL,3))
	#print file_name
    	batch_x[file_id] = np.asarray(resize(f['image'],(154,205,3)))/255.0
    	l = int(f['label'])
    	batch_y[file_id][l]=1	    
        file_id+=1

    current_batch_ind += size 
    return batch_x, batch_y, current_batch_ind, file_name_list 


# In[9]:

def fill_feed_dict(data_set, images_pl, labels_pl, current_batch_ind):
    """Fills the feed_dict for training the given step.
    A feed_dict takes the form of:
    feed_dict = {
                  <placeholder>: <tensor of values to be passed for placeholder>,
                  ....
                }
    Args:
        data_set: The set of images and labels, from input_data.read_data_sets()
        images_pl: The images placeholder, from placeholder_inputs().
        labels_pl: The labels placeholder, from placeholder_inputs().
    Returns:
        feed_dict: The feed dictionary mapping from placeholders to values.
    """
    # Create the feed_dict for the placeholders filled with the next
    # `batch size ` examples.
    
    batch=next_batch(BATCH_SIZE, data_set, current_batch_ind)
    data_set = batch[3]
    current_batch_ind = batch[2]

    
    feed_dict = {
      images_pl: batch[0],
      labels_pl: batch[1],
    }
    return feed_dict, data_set, current_batch_ind


# In[ ]:

def do_eval(sess, eval_correct, images_placeholder, labels_placeholder, data_set):
    """Runs one evaluation against the full epoch of data.
    Args:
        sess: The session in which the model has been trained.
        eval_correct: The Tensor that returns the number of correct predictions.
        images_placeholder: The images placeholder.
        labels_placeholder: The labels placeholder.
        data_set: The set of images and labels to evaluate, from
                input_data.read_data_sets().
    """
    # And run one epoch of eval.
    true_count = 0  # Counts the number of correct predictions.
    precision =0.0000
    steps_per_epoch = len(data_set) // BATCH_SIZE
    num_examples = steps_per_epoch * BATCH_SIZE
    current_batch_ind=0
    print 'Testing'
    for step in xrange(steps_per_epoch):
        feed_dict, data_set, current_batch_ind= fill_feed_dict(data_set, images_placeholder,
                               labels_placeholder, current_batch_ind)
        #'print sess.run(eval_correct, feed_dict=feed_dict)'
        true_count = sess.run(eval_correct, feed_dict=feed_dict)
        
    precision = true_count/num_examples
    print('  Num examples: %d  Num correct: %d  Precision @ 1: %0.04f' %
            (num_examples, true_count, (true_count/num_examples)))


# In[ ]:

#for df in data[:10]:
#	print df
train_data = data[:int(TRAINING_PROP*len(data))]
test_data = data[int(TRAINING_PROP*len(data)):]
#train_data = train_data.reset_index(drop = True)
#test_data = test_data.reset_index(drop = True)
print len(train_data)
print len(test_data)
print len(data)
with tf.Graph().as_default():

    # Generate placeholders for the images and labels.
    images_placeholder, labels_placeholder = placeholder_inputs(BATCH_SIZE)
    #print images_placeholder
    #print labels_placeholder

    # Build a Graph that computes predictions from the inference model.
    logits = inference(images_placeholder, 0.5, 512)
    print logits

    # Add to the Graph the Ops for loss calculation.
    loss = calc_loss(logits, labels_placeholder)

    # Add to the Graph the Ops that calculate and apply gradients.
    train_op = training(loss, LEARNING_RATE)

    # Add the Op to compare the logits to the labels during evaluation.
    eval_correct = evaluation(logits, labels_placeholder)
    print eval_correct

    # Build the summary operation based on the TF collection of Summaries.
    #summary_op = tf.merge_all_summaries()

    # Create a saver for writing training checkpoints.
    #saver = tf.train.Saver()
    # Create a session for running Ops on the Graph.
    sess = tf.Session()

    # Run the Op to initialize the variables.
    init = tf.initialize_all_variables()
    init = tf.initialize_all_variables()
    config = tf.ConfigProto()
    config.gpu_options.allocator_type = 'BFC'
    with tf.Session(config = config) as s:
        sess.run(init)
        sess.run(init)
    print 'checking'

    # Instantiate a SummaryWriter to output summaries and the Graph.
    #summary_writer = tf.train.SummaryWriter('../Data/', sess.graph)
    # And then after everything is built, start the training loop.
    current_batch_ind = 1
    for step in xrange(MAX_STEPS):
            start_time = time.time()

            # Fill a feed dictionary with the actual set of images and labels
            # for this particular training step.
            print num
            num = num+1
            feed_dict, train_data, current_batch_ind= fill_feed_dict(train_data,
                                 images_placeholder,
                                 labels_placeholder,
				 current_batch_ind)
            

            # Run one step of the model.  The return values are the activations
            # from the `train_op` (which is discarded) and the `loss` Op.  To
            # inspect the values of your Ops or variables, you may include them
            # in the list passed to sess.run() and the value tensors will be
            # returned in the tuple from the call.
            _, loss_value = sess.run([train_op, loss],
                               feed_dict=feed_dict)

            duration = time.time() - start_time

            # Write the summaries and print an overview fairly often.
            if step % 1 == 0:
                # Print status to stdout.
                print('Step %d: loss = %.2f (%.3f sec)' % (step, loss_value, duration))
                # Update the events file.
                #summary_str = sess.run(summary_op, feed_dict=feed_dict)
                #summary_writer.add_summary(summary_str, step)
                #summary_writer.flush()

            # Save a checkpoint and evaluate the model periodically.
            if (step + 1) % 3 == 0 or (step + 1) == MAX_STEPS:
                #saver.save(sess, '../Data/', global_step=step)
                # Evaluate against the training set.
                print('Training Data Eval:')
                do_eval(sess, eval_correct, images_placeholder, labels_placeholder, train_data)
                # Evaluate against the validation set.
                print('Validation Data Eval:')
                do_eval(sess, eval_correct, images_placeholder, labels_placeholder, test_data)

