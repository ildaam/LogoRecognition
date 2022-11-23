import os
import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import csv

classes_test= ['abus', 'accenture']

def class_list():
    folders_file = open("classes_folder.txt", "r")
    file_content = folders_file.read()
    classes_folders = file_content.split(",")
    folders_file.close
    return(classes_folders)

def xml_to_csv(path):
    xml_list = []
    xml_df_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                    (int(root.find('size')[0].text)),
                    (int(root.find('size')[1].text)),
                    ((member[0].text)),
                    (int(member[4][0].text)),
                    (int(member[4][1].text)),
                    (int(member[4][2].text)),
                    (int(member[4][3].text))
                     )
            xml_list.append(value)

            
    xml_df = pd.DataFrame(xml_list)
   
    return xml_df


def main():

    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']

    classes= class_list()
    print(classes)

    for directory in ['train', 'test']:
        xml_df_list = []
        with open('annotations/{}_labels_newww.csv'.format(directory), 'w') as csv_file:
            dw = csv.DictWriter(csv_file, delimiter=',', fieldnames=column_name)
            dw.writeheader()
            for class_ in classes:
                _path = os.path.join(os.getcwd(), 'images\{}'.format(directory))
                image_path= _path + '\\' + class_ + '\\'
                xml_df = xml_to_csv(image_path) 
                xml_df.to_csv(csv_file, mode = 'a', index=False, header=False)
                print('Successfully converted xml to csv.')

main()
 