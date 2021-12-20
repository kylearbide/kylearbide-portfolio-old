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

# MAGIC %sh
# MAGIC 
# MAGIC 
# MAGIC kaggle --version
# MAGIC pip install --upgrade pip

# COMMAND ----------

# MAGIC %md
# MAGIC The following commands download the files from the kaggle api, but take some time to run and the files we need are already in the dbfs

# COMMAND ----------

#%sh
#export KAGGLE_USERNAME="kylearbide"
#export KAGGLE_KEY="2f2f6f925ce7563df475676b03c5d84c"
#kaggle competitions download -c siim-isic-melanoma-classification 


# COMMAND ----------

#%fs cp -r file:/databricks/driver/siim-isic-melanoma-classification.zip dbfs:/tmp

# COMMAND ----------

# MAGIC %sh
# MAGIC export KAGGLE_USERNAME="kylearbide"
# MAGIC export KAGGLE_KEY="2f2f6f925ce7563df475676b03c5d84c"
# MAGIC kaggle competitions download -c siim-isic-melanoma-classification -f train.csv 

# COMMAND ----------

#%fs cp -r file:/databricks/driver/train.csv.zip dbfs:/tmp

# COMMAND ----------

#%sh unzip /dbfs/tmp/siim-isic-melanoma-classification.zip

# COMMAND ----------

#%sh unzip /dbfs/tmp/train.csv.zip

# COMMAND ----------

# MAGIC %md 
# MAGIC ##3. Load the Labels from a CSV File and Explore the Data
# MAGIC ### Got to the https://www.kaggle.com/c/siim-isic-melanoma-classification/overview and download the training labels (train.csv)
# MAGIC #### Load the train.csv file into Databricks using the Data Upload in the Workspace.

# COMMAND ----------

labels = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("/FileStore/train.csv")

# COMMAND ----------

display(labels)

# COMMAND ----------

display(labels.groupBy("diagnosis").count())

# COMMAND ----------

labels = labels.withColumnRenamed("image_name", "image_id")

# COMMAND ----------

melanoma = labels.where("target = 1" )
benign = labels.where("target = 0" )

# COMMAND ----------

# MAGIC %md
# MAGIC ### 4. Create a Dataframe named "labels" and count the benign and malignant examples in the dataset

# COMMAND ----------

display(labels.groupBy("benign_malignant").count())

# COMMAND ----------

display(labels.groupBy("benign_malignant").count())

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

testState = True
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
# MAGIC pip install tf_slim

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
import pandas as pd

# COMMAND ----------

pip list

# COMMAND ----------

labels.columns

# COMMAND ----------

display(labels.groupBy(["benign_malignant","target"]).count())
#verifies our target labels

# COMMAND ----------

display(labels.groupBy(["Sex","target"]).count())

# COMMAND ----------

ages = labels.groupBy(["age_approx","target"]).count().sort(["age_approx"])
display(ages)

# COMMAND ----------

agesex = labels.groupBy(["Sex","age_approx","target"]).count().sort(["age_approx","Sex"])
display(agesex)

# COMMAND ----------

display(agesex)

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

#File is already in tmp folder but this is how we could move it
#%fs cp -r file:/databricks/driver/retrain.py dbfs:/tmp

# COMMAND ----------

# MAGIC %sh ls -al /tmp

# COMMAND ----------

# MAGIC %md
# MAGIC ### 9. Take the model you just downloaded and edit the model and update it so that it works in databricks
# MAGIC Hint: Add in the following import statements "import tensorflow.compat.v1 as tf" "tf.disable_v2_behavior()""

# COMMAND ----------

# MAGIC %sh pip uninstall -y  tensorflow-gpu

# COMMAND ----------

# MAGIC %sh
# MAGIC pip install "tensorflow-gpu~=1.0"
# MAGIC pip install "tensorflow-hub[make_image_classifier]~=0.6"

# COMMAND ----------

# MAGIC %sh 
# MAGIC ls /dbfs/tmp/

# COMMAND ----------

import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

# COMMAND ----------

# MAGIC %sh /databricks/python/bin/python3 -u "/dbfs/tmp/retrain.py" --image_dir "/dbfs/tmp/training"  --output_graph "/tmp/melanoma.pb"

# COMMAND ----------

# MAGIC %sh ls /dbfs/tmp/

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

# MAGIC %sh
# MAGIC %sh pip uninstall -y  tensorflow-gpu
# MAGIC pip install "tensorflow-gpu~=2.0"
# MAGIC pip install "tensorflow-hub[make_image_classifier]~=0.6"

# COMMAND ----------

import tensorflow.compat.v1 as tf

# COMMAND ----------

# MAGIC %sh
# MAGIC cd /dbfs/tmp/
# MAGIC make_image_classifier \
# MAGIC   --image_dir  "/dbfs/tmp/training" \
# MAGIC   --tfhub_module https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4 \
# MAGIC   --saved_model_dir /dbfs/tmp \
# MAGIC   --labels_output_file class_labels.txt \
# MAGIC   --tflite_output_file new_mobile_model.tflite \
# MAGIC   --summaries_dir my_log_dir

# COMMAND ----------

dbutils.fs.mkdirs("/dbfs/tmp/new_mobile_model.tflite")

# COMMAND ----------

# MAGIC %md ##11. Scoring Images using a Convolution Neural Network

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

# MAGIC %md
# MAGIC The first model incorrectly classifies the melanoma image

# COMMAND ----------

displayPrediction(benignImg, "Benign")

# COMMAND ----------

dbutils.tensorboard.start("file:/tmp/retrain_logs")

# COMMAND ----------

dbutils.tensorboard.stop()

# COMMAND ----------

# MAGIC %md
# MAGIC RUNNING PREDICTIONS ON THE SECOND MODEL
# MAGIC 
# MAGIC Import the "label_image" script from tensorflow

# COMMAND ----------

# MAGIC %sh
# MAGIC wget https://raw.githubusercontent.com/tensorflow/tensorflow/master/tensorflow/lite/examples/python/label_image.py

# COMMAND ----------

# MAGIC %fs cp -r file:/databricks/driver/label_image.py dbfs:/tmp

# COMMAND ----------

# MAGIC %sh
# MAGIC cd /dbfs/tmp/
# MAGIC python3 label_image.py \
# MAGIC   --model_file new_mobile_model.tflite --label_file class_labels.txt \
# MAGIC   --image /dbfs/tmp/training/benign/ISIC_0341663.jpg

# COMMAND ----------

# MAGIC %sh
# MAGIC cd /dbfs/tmp/
# MAGIC python3 label_image.py \
# MAGIC   --model_file new_mobile_model.tflite --label_file class_labels.txt \
# MAGIC   --image /dbfs/tmp/training/melanoma/ISIC_0489267.jpg

# COMMAND ----------

# MAGIC %md
# MAGIC The second model is also able to predict but also incorrectly categorizes the melanoma image
