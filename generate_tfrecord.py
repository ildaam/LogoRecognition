"""
Usage:
  # From tensorflow/models/
  # Create train data:
  python generate_tfrecord.py --csv_input=data/train_labels.csv  --output_path=train.record
  # Create test data:
  python generate_tfrecord.py --csv_input=data/test_labels.csv  --output_path=test.record
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import sys
sys.path.append('\\Users\\ilda_\\Documents\\work\\LogosProject\\models\\research\\object_detection')
#added object_detection folder to the system path so that its content can be
#accessed without having to run this script inside the object_detection file
import pandas as pd
import tensorflow as tf
import tensorflow.compat.v1 as tf

from PIL import Image
from collections import namedtuple, OrderedDict
from utils import dataset_util



flags = tf.app.flags
flags.DEFINE_string('csv_input', '', 'Path to the CSV input')
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
flags.DEFINE_string('image_dir', '', 'Path to images')
FLAGS = flags.FLAGS

#classes stored in a separate txt file for better readability
#266 classes with 0samples NOT counted as one
def class_list():
    classes_file = open("classes_all1.txt", "r")
    file_content = classes_file.read()
    classes_ = file_content.split(",")
    classes_file.close()
    print("The list is: ", classes_)

    folders_file = open("classes_folder.txt", "r")
    file_content = folders_file.read()
    classes_folders = file_content.split(",")
    folders_file.close()
    print("The list is: ", classes_folders)
    return(classes_, classes_folders)


# use the classes list with all labels here and not the classes list used down in main
def class_text_to_int(row_label):
    if row_label not in classes_:
        print('ROW LABEL',row_label)
        classes_.append(row_label)
        print("Added:", row_label, "to classes")
    for i in range (0,len(classes_)):
        current_class=classes_[i]
        if row_label == current_class:
            return (i+1)
        if row_label == current_class + '-symbol' or row_label == current_class + '-text' or row_label == current_class + '1' or row_label == current_class + '2' or row_label==current_class+ '3':
            return (i+1)
        else:
            continue
    print(classes_)



def split(df, group):
    data = namedtuple('data', ['name', 'object'])
    
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]
    


def create_tf_example(group, path, file_):
    #print ("GROUP", group)
    #print("PATH", path)
    #group.name is the groups ID which should be the same as the filename in the folder

    #format.(group.object.filename[0])
    filename= file_

    with tf.gfile.GFile(os.path.join(path, '{}'.format(filename)) , 'rb') as fid: 
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size
    #print("WIDTH" , width)
    #print("HEIGHT", height) 

    filename_b = filename.encode('utf8')
    print("encoded filename",filename_b)
    
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int(row['class']))



    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename_b),
        'image/source_id': dataset_util.bytes_feature(filename_b),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))

    print("crated a tf example for filename:", filename)

    return tf_example 


def main(_):
        
    writer = tf.python_io.TFRecordWriter(FLAGS.output_path)
    examples = pd.read_csv(FLAGS.csv_input, encoding = 'unicode_escape', index_col = False)
    grouped_filename= split(examples, 'ID')

    classes, classes_folders= class_list()
    #loop through all folders
    for class_ in classes_folders:
        path = os.getcwd() + '\\' + FLAGS.image_dir + '\\' + class_
        files = os.listdir(path)
        ch1= '_'
        ch2 = '.'
        file_list=[]
        ID_list=[]
        #loop throgh all files within the folder and check that it's an image
        for file_ in files:
            if file_.endswith('.jpg'):
                file_list.append(file_)
                _=file_.split(ch1, 1)[1]
                file_onlyID = _.split(ch2, 1) [0] #this gives only the ID from the filename
                ID_list.append(file_onlyID)

        group_list = []
        for group in grouped_filename:
            group_list.append(group)

        for i in range (0, len(group_list)):
            group = group_list[i]
            for k in range (0, len(ID_list)):
                ID = int(ID_list[k])
                file_ = file_list[k]
                #check that we have the right image
                if group.name == ID:
                    tf_example = create_tf_example(group, path, file_)
                    if tf_example != None:
                        writer.write(tf_example.SerializeToString())
    

    writer.close()
    output_path = os.path.join(os.getcwd(), FLAGS.output_path)
    print('Successfully created the TFRecords: {}'.format(output_path))

if __name__ == '__main__':
    tf.app.run()


   #access group elements like xmin like this
    #for row, index in group.object.iterrows():
    #   print("ID IS", group.name)
    #  print("XMIIN", '\n', group.object.xmin)

    #specific = examples.iloc[23054] #the last element in the csv file
        #rows are series and features can be accessed 
    #specific['xmin']