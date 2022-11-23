def class_list():
    classes_file = open("classes_all1.txt", "r")
    file_content = classes_file.read()
    classes_ = file_content.split(",")
    classes_file.close
    return(classes_)

def label_map_v1():

    classes= class_list()

    with open('training_demo/annotations/label-map.pbtxt', 'a') as the_file:
            for i in range (0, len(classes)):
                class_ = classes[i]
                the_file.write('item\n')
                the_file.write('{\n')
                the_file.write('id :{}'.format(int(i+1)))
                the_file.write('\n')
                the_file.write("name :'{0}'".format(str(class_)))
                the_file.write('\n')
                the_file.write('}\n')
                the_file.write('\n')
                the_file.write('\n')
                    


label_map_v1()
