import os
import cv2 as cv
import matplotlib.pyplot as plt
images_per_letter = 3000
train_num  = 2500
new_data_set_path = "/home/sainath/Music/dataset/"
def directorise(new_set,letter):
    os.mkdir(new_data_set_path + letter)
    image_set,image_addr_set = new_set
    path = new_data_set_path + letter+"/"
    
    
    os.mkdir(path+"/train")
    for i in range(train_num):
        train_path = path + "/train/"
        cv.imwrite(train_path+image_addr_set[i],image_set[i])
        print("Image "+str(i)+" added to "+  path + "/train")
    
    
    
    os.mkdir(path+"/test")
    for i in range(train_num,images_per_letter):
        test_path = path + "/test/"
        cv.imwrite(test_path+image_addr_set[i],image_set[i])
        print("Image "+ str(i) + "added to " + path + "/test")




def image_collector(letter):
    classes = []
    path = os.getcwd()+"/"+letter
    for dp,dn,fn in os.walk(path):
        classes = dn
        break
    print(letter,classes)
    new_set = ([],[])
    number_of_images = 0
    for cls in classes:
        images = []
        for dp,dn,fn in os.walk(path+"/"+cls):
            images = fn
            dirpath = dp
            break
        newImages = []
        for image in images:
            img = cv.imread(path+"/"+cls+"/"+image,0)
            #plt.imshow(img)
            #plt.show()
            newImages.append(img)
        new_set[0].extend(newImages)
        new_set[1].extend(images)
        if len(new_set) > images_per_letter:

            break
    return (new_set[0][0:images_per_letter],new_set[1][0:images_per_letter])


#main
letters = []
for (dirpath,dirnames,filenames) in os.walk(os.getcwd()):
    letters = dirnames
    break
#import matplotlib.pyplot as plt
for letter in letters:
    new_set = image_collector(letter)
    image_set,image_addr_set = new_set


    directorise(new_set,letter)
