#Random Forest using tensorflow
from __future__ import print_function

import os
import tensorflow as tf
from tensorflow.contrib.tensor_forest.python import tensor_forest
from tensorflow.python.ops import resources
#from keras.datasets import mnist

os.environ["CUDA_VISIBLE_DEVICES"] = ""

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("/Users/sumanthpareekshit/Downloads/mnist/",one_hot = False)

#Parameters
num_steps = 500
batch_size = 1024
nclasses = 10
nfeatures = 784
ntrees = 10
mnodes = 1000

#Input and target data
X = tf.placeholder(tf.float32,shape=[None, nfeatures])
Y = tf.placeholder(tf.int32, shape=[None])

#Random Forest parameters
hparams = tensor_forest.ForestHParams(num_classes = nclasses,
                                      num_features = nfeatures,
                                      num_trees = ntrees,
                                      max_nodes = mnodes).fill()

#Build the Random Forest
forest_graph = tensor_forest.RandomForestGraphs(hparams)
train_op = forest_graph.training_graph(X,Y)
loss_op = forest_graph.training_loss(X,Y)

#Accuracy measurements
infer_op,_,_ = forest_graph.inference_graph(X)
correct_prediction = tf.equal(tf.argmax(infer_op,1),tf.cast(Y,tf.int64))
accuracy_op = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

#Initialize the variables
init_vars = tf.group(tf.global_variables_initializer(),
                     resources.initialize_resources(resources.shared_resources()))

#Start the session
sess = tf.Session()
sess.run(init_vars)

#Train
for i in range(1,num_steps+1):
    batch_x,batch_y = mnist.train.next_batch(batch_size)
    _,l = sess.run([train_op,loss_op],feed_dict={X:batch_x, Y:batch_y})
    if i%50 == 0 or i==1:
        acc = sess.run(accuracy_op,feed_dict={X:batch_x, Y:batch_y})
        print('Step %i, Loss: %f, Acc: %f' %(i,l,acc))

#Test
test_x,test_y = mnist.test.images,mnist.test.labels
print("Test Accuracy:", sess.run(accuracy_op,feed_dict={X:test_x, Y:test_y}))
