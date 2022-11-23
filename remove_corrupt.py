
import os
import glob
import shutil

def remove_ext(list_of_pathnames):
    """
    removes the extension from each filename
    """
    return [os.path.splitext(filename)[0] for filename in list_of_pathnames]

folders_path= "C:/Users/ilda_/Documents/work/data_cleaned1/voc_format"

for folder in os.listdir(folders_path):
     
    images_path= folders_path + "/" + folder + "/"
    os.chdir(images_path)  
    os.mkdir("corrupted files")
    newpath = os.path.join(images_path,"corrupted files") # made it os independent... 


    list_of_jpgs = glob.glob(images_path+"*.jpg")
    list_of_xmls = glob.glob(images_path+"*.xml")


    print(list_of_jpgs, "\n\n", list_of_xmls) #remove

    jpgs_without_extension = remove_ext(list_of_jpgs)
    xmls_without_extension = remove_ext(list_of_xmls)

    print(jpgs_without_extension, "\n\n", xmls_without_extension) #remove

    for filename in jpgs_without_extension:
        if filename not in xmls_without_extension:
            print("moving", filename) #remove
            shutil.move((filename + '.jpg'), newpath)   # move image to new path.
            #shutil.move((filename + '.xml'), newpath)   # move image to new path.

