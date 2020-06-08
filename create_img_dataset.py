from pathlib import Path
from PIL import Image
import numpy as np
from sklearn.preprocessing import LabelEncoder

def create_dataset(directory,nrow=64,ncol=64,color='rgb',imgtype='jpg'):
    """Create image dataset with label in numpy array.
    Args:
        directory : images directory. each image class should be separated in different folder. folder name will returned as image label
        nrow : height of image. default is 64
        ncol : width of image. default is 64
        color : type of desired image ouput. 'rgb' for color image, 'greyscale' for greyscale image
        imgtyp : file type of image. default is jpg
    Return:
        images : data of images in numpy array. 4d array if rgb, 3d array if greyscale
        label : label name
        y : encoded label
    """
    
    dirname = Path(directory+'/')
    folder = [f.name for f in dirname.iterdir() if f.is_dir()]
    label = [] 

    # create temporary variabel for storing image data
    # if user want rgb as output, the shape of images would be number_of_image, width_of_image, height_of_image, color_channel
    # if user want greyscale as ouput, the shape of images would be number_of_image, width_of_image, height_of_image
    if (color=='rgb'):
        images = np.zeros((1,nrow,ncol,3), 'uint8')
    elif (color=='greyscale'):
        images = np.zeros((1,nrow,ncol), 'uint8')

    for i in range (len(folder)):
        for filename in Path(directory+folder[i]).rglob('*.'+imgtype):
            image = Image.open(filename).resize((nrow,ncol))
            if (color=='greyscale'):
                image = image.convert('L')
            image = np.array(image)
            #image = np.invert(image)
            image = np.expand_dims(image, axis=0)
            images = np.concatenate((images,image), axis=0)
            label.append(folder[i])    
    images = np.delete(images, (0), axis=0)
    y = LabelEncoder().fit_transform(label)

    return images, label, y