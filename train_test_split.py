import os
import shutil
import glob

#a=[ x[0] for x in os.walk('voc_format')]


#a = next(os.walk('voc_format'))[1]
#print(a)

OUTPATH = "\\Users\\ilda_\\Documents\\work\\data_cleaned1\\imgs1"
INPATH = "\\Users\\ilda_\\Documents\\work\\data_cleaned1\\voc_format"

def remove_ext(list_of_pathnames):
    """
    removes the extension from each filename
    """
    return [os.path.splitext(filename)[0] for filename in list_of_pathnames]


for folder in os.listdir(INPATH):


    train_path = OUTPATH + '\\train\\' + folder + '\\'
    test_path  = OUTPATH + '\\test\\' + folder + '\\'

    inpath    = INPATH + '\\' + folder + '\\'

    os.makedirs(train_path , exist_ok=True)
    os.makedirs(test_path, exist_ok=True)
     
    files = os.listdir(inpath)
    print(files)
    print(inpath)
    images = glob.glob(inpath+"*.jpg")
    xml_files = glob.glob(inpath+"*.xml")
    no_of_images = len(images) #-1 is for the url file
    no_xml= len(xml_files)
    print(no_of_images, no_xml)

    test_set = int (no_of_images * 0.1)
    print(folder, "test set:", test_set)
    train_set= no_of_images - test_set #-1 is because of the url file
    print(folder, "train set", train_set)

    images_without_extension=remove_ext(images)
    xml_without_extension=remove_ext(xml_files)

    test_imgs = images_without_extension[:test_set]#the first (testset) number of elements
    print(test_imgs)
    test_xml_files = xml_without_extension[:test_set]
    train_imgs = images_without_extension[test_set:]#everything but the first testset number of elements
    print(train_imgs)
    train_xml_files = xml_without_extension[test_set:]

    for test_img in test_imgs:
        jpg= os.path.basename(os.path.normpath(test_img))
        print("moving jpg", jpg)
        shutil.move( test_img + ".jpg", test_path)
        print( test_img + ".jpg", test_path)
    for test_xml in test_xml_files:
        xml = os.path.basename(os.path.normpath(test_xml))
        print("moving xml ", xml)
        print( test_xml + ".xml", test_path)
        shutil.move( test_xml + ".xml", test_path)
            
    for train_img in train_imgs: 
        jpg= os.path.basename(os.path.normpath(train_img))
        print("moving jpg", jpg)
        shutil.move( train_img+".jpg", train_path)
        print( train_img+".jpg", train_path)
    for train_xml in train_xml_files:
        xml = os.path.basename(os.path.normpath(train_xml))
        print("moving xml", xml)
        print( train_xml+".xml", train_path)
        shutil.move( train_xml + ".xml", train_path)
