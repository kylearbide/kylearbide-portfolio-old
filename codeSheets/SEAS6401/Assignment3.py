# Databricks notebook source
# MAGIC %md
# MAGIC title: Detecting Melanoma with Deep Learning Homework 3
# MAGIC 
# MAGIC tags:
# MAGIC - deep-learning
# MAGIC - ml
# MAGIC - image classification 
# MAGIC - HLS
# MAGIC - Python
# MAGIC - tensorflow
# MAGIC - tensorboard
# MAGIC libraries:
# MAGIC   - pypi:
# MAGIC       package: mxnet
# MAGIC       package: tensorflow-hub
# MAGIC       

# COMMAND ----------

# MAGIC %md #Detecting Melanoma with Deep Learning
# MAGIC 
# MAGIC Melanoma is one of the mostly deadliest forms of skin cancer with over 75,000 cases in the US each year.
# MAGIC 
# MAGIC Melanoma is also hard to detect as not all skin moles and lesions are cancerous. 
# MAGIC 
# MAGIC This demo is based on the [ISIC 2017](https://challenge.kitware.com/#challenge/583f126bcad3a51cc66c8d9a): Skin Lesion Analysis Towards Melanoma Detection Contest Sponsored by the *International Skin Imaging Collaboration*

# COMMAND ----------

# MAGIC %md ##0. Cluster Setup
# MAGIC 
# MAGIC Datbricks Runtime 5.3 ML (includes Apache Spark 2.4.0, GPU , Scala 2.11)
# MAGIC 
# MAGIC Driver: p2.xlarge, Workers: 1 * p2.xlarge
# MAGIC 
# MAGIC PyPi Libraries
# MAGIC   - mxnet
# MAGIC   - tensorflow-hub
# MAGIC   
# MAGIC Tested on demo, azure and field-eng shards

# COMMAND ----------

# MAGIC %md ##1. Using s3 Mount to the Kaggle Dataset and bring into your Cluster Environment
# MAGIC 
# MAGIC Datbricks Runtime 5.3 ML (includes Apache Spark 2.4.0, GPU , Scala 2.11)

# COMMAND ----------

# MAGIC %sh
# MAGIC sudo apt-get install s3fs
# MAGIC pip install torch-utils

# COMMAND ----------

dbutils.fs.ls("/FileStore/tables/tanvi_patel_accessKeys.csv")

# COMMAND ----------

file_type = "csv"
first_row_header="true"
delimiter = ","
aws_keys_df = spark.read.format(file_type)\
.option("header", first_row_header)\
.option("sep",delimiter)\
.load("/FileStore/tables/tanvi_patel_accessKeys.csv")

# COMMAND ----------

from pyspark.sql.functions import *
import urllib
ACCESS_KEY= aws_keys_df.select('Access key ID').collect()[0][0]
SECRET_KEY=aws_keys_df.select('Secret access key').collect()[0][0]
ENCODED_SECRET_KEY=urllib.parse.quote(SECRET_KEY,"")

# COMMAND ----------

print(SECRET_KEY)

# COMMAND ----------

AWS_S3_BUCKET="melanomatrain"
MOUNT_NAME="/mnt/melanoma1"
url= "s3a://%s:%s@%s" % (ACCESS_KEY, ENCODED_SECRET_KEY, AWS_S3_BUCKET)
#dbutils.fs.mount(url, MOUNT_NAME)

# COMMAND ----------

# MAGIC %fs ls dbfs:/mnt/melanoma1

# COMMAND ----------



# COMMAND ----------

# MAGIC %md ##2. Using Kaggle API to Download the Data
# MAGIC ### Got to the https://www.kaggle.com/c/siim-isic-melanoma-classification/overview and download the train dataset (from the jpeg folder)
# MAGIC 
# MAGIC Datbricks Runtime 5.3 ML (includes Apache Spark 2.4.0, GPU , Scala 2.11)

# COMMAND ----------

# MAGIC %sh pip install kaggle

# COMMAND ----------

# MAGIC %md 
# MAGIC ##3. Load the Labels from a CSV File and Explore the Data
# MAGIC ### Got to the https://www.kaggle.com/c/siim-isic-melanoma-classification/overview and download the training labels (train.csv)
# MAGIC #### Load the train.csv file into Databricks using the Data Upload in the Workspace.

# COMMAND ----------

labels = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("/FileStore/tables/train-1.csv")

# COMMAND ----------

display(labels)

# COMMAND ----------

display(labels.groupBy("diagnosis").count())

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4. Create a Dataframe named "labels" and count the benign and malignant examples in the dataset

# COMMAND ----------

#insert code here

# COMMAND ----------

# MAGIC %md ## 5. Cache Data to the SSD
# MAGIC Use code provided below

# COMMAND ----------

import os
import shutil

# Import these two packages to time out the caching for troubleshooting
import multiprocessing
import time


def cacheFilesAndReturn(images, subdir):
  file_dir = '/tmp/training/'+subdir+'/'
  try:
    os.makedirs(str(file_dir))
  except:
    pass
  for image_id in images:
    shutil.copyfile("/dbfs/mnt/melanoma1/%s.jpg" % image_id, str(file_dir)+"%s.jpg" % image_id)
    
def timeOut(process, seconds):
  process.start()
  time.sleep(seconds)
  process.terminate()
  process.join()

# COMMAND ----------

# MAGIC %md
# MAGIC ### 6. We will only run the Cache statements for around 30 seconds to bring in a sample of the data into memory
# MAGIC Use the code below to cache the data

# COMMAND ----------

if testState == True:
  melanomaProcess = multiprocessing.Process(target=cacheFilesAndReturn, name="cacheFilesAndReturn",args=(melanoma.select("image_id").rdd.map(lambda x: x[0]).collect(), "melanoma"))
  timeOut(melanomaProcess, 30)
else:
  cacheFilesAndReturn(melanoma.select("image_id").rdd.map(lambda x: x[0]).collect(), "melanoma")

# COMMAND ----------

if testState == True:
  benignProcess = multiprocessing.Process(target=cacheFilesAndReturn, name="cacheFilesAndReturn", args=(benign.select("image_id").rdd.map(lambda x: x[0]).collect(), "benign"))
  timeOut(benignProcess, 30)
else:
  cacheFilesAndReturn(benign.select("image_id").rdd.map(lambda x: x[0]).collect(), "benign")

# COMMAND ----------

# MAGIC %md 
# MAGIC ##7. Explore the Dataset - Add additional Exploratory Steps
# MAGIC Hints: *Better understand if the labels match the training data.

# COMMAND ----------

# MAGIC %sh 
# MAGIC pip install mxnet
# MAGIC pip install tensorflow_hub

# COMMAND ----------

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import mxnet
import tensorflow.compat.v1 as tf
#tf.disable_v2_behavior()
import tensorflow_hub as hub
#import tensorflow as tf
import tf_slim as slim


# COMMAND ----------

pip list

# COMMAND ----------

melanomaImg = "/tmp/training/melanoma/" + os.listdir("/tmp/training/melanoma/")[0]
benignImg = "/tmp/training/benign/" + os.listdir("/tmp/training/benign/")[0]
print(melanomaImg)
print(benignImg)

# COMMAND ----------

with open(melanomaImg, 'rb') as fp:
  str_image = fp.read()

# COMMAND ----------

plt.imshow(mxnet.image.imdecode(open(melanomaImg, 'rb').read()).asnumpy())
plt.title("Melanoma")
display(plt.show())

# COMMAND ----------

plt.imshow(mxnet.image.imdecode(open(benignImg, 'rb').read()).asnumpy())
plt.title("Benign")
display(plt.show())

# COMMAND ----------

mxnet.image.imdecode(open(melanomaImg, 'rb').read()).asnumpy()

# COMMAND ----------

# MAGIC %md ##8.Train the Model using a Convolution Neural Network
# MAGIC 
# MAGIC Here we will use transfer learning to train an image classifier. 
# MAGIC It uses feature vectors computed by Inception V3 trained on ImageNet

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC <img src="https://cdn-images-1.medium.com/max/1800/0*mH17FEz4LHpaJrPb.png" alt="drawing" width="800"/>

# COMMAND ----------

# DBTITLE 1,Download the inception v3 library for transfer learning
# MAGIC %sh
# MAGIC wget https://raw.githubusercontent.com/tensorflow/tensorflow/c565660e008cf666c582668cb0d0937ca86e71fb/tensorflow/examples/image_retraining/retrain.py

# COMMAND ----------

# MAGIC %sh ls -al /tmp

# COMMAND ----------

# MAGIC %md
# MAGIC ### 9. Take the model you just downloaded and edit the model and update it so that it works in databricks
# MAGIC Hint: Add in the following import statements "import tensorflow.compat.v1 as tf" "tf.disable_v2_behavior()""

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC Transfer learning: Get the model you downloaded and apply another layer
# MAGIC Will output a weight file used to test your model

# COMMAND ----------

# MAGIC %sh /databricks/python/bin/python3 -u {insert pretrained model here} --image_dir "/dbfs/tmp/training"  --output_graph "/tmp/melanoma.pb"

# COMMAND ----------

# MAGIC %sh
# MAGIC ls /dbfs/user/

# COMMAND ----------

# MAGIC %fs ls 

# COMMAND ----------

dbutils.fs.cp("file:/tmp/melanoma.pb", "dbfs:/melanoma/melanoma.pb", True)

# COMMAND ----------

dbutils.fs.cp('file:/tmp/retrain_logs', 'dbfs:/melanoma/', True)

# COMMAND ----------

# MAGIC %md
# MAGIC ### 10. Download a different pretrained model and conduct transfer learning and train the model to add additional melanoma and benign features

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC The first pretrained model was given to us. We need to find another pretrained model and apply the same methods to great an out put

# COMMAND ----------

# Insert Code Here

# COMMAND ----------

# MAGIC %md ##11. Scoring Images using a Convolution Neural Network

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC Take the .pb file and run against the set of test images. Scores the results of the predictive model

# COMMAND ----------

dbutils.fs.mkdirs("file:/tmp/retrain_logs")

# COMMAND ----------

dbutils.fs.cp('dbfs:/melanoma/train', 'file:/tmp/retrain_logs', True)

# COMMAND ----------

dbutils.fs.cp('dbfs:/melanoma/melanoma.pb', 'file:/tmp/melanoma.pb', True)

# COMMAND ----------

with tf.gfile.FastGFile("/tmp/melanoma.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

# COMMAND ----------

def displayPrediction(img_path, label):
  image_data = tf.gfile.FastGFile(img_path, 'rb').read()
  with tf.Session() as sess:
    # Feed the image_data as input to the graph and get first prediction
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    
    predictions = sess.run(softmax_tensor, \
             {'DecodeJpeg/contents:0': image_data})
    
    # Sort to show labels of first prediction in order of confidence
    #top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
    plt.imshow(mxnet.image.imdecode(open(img_path, 'rb').read()).asnumpy())
    plt.title(label)
    plt.figtext(0,0,'Model Prediction: Not Cancer: %.5f, Cancer: %.5f' % (predictions[0][1], predictions[0][0]))
    display(plt.show())
    plt.close()

# COMMAND ----------

displayPrediction(melanomaImg, "Melanoma")

# COMMAND ----------

displayPrediction(benignImg, "Benign")

# COMMAND ----------

dbutils.tensorboard.start("file:/tmp/retrain_logs")

# COMMAND ----------

# dbutils.tensorboard.stop()
