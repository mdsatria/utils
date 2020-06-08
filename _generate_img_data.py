from pathlib import Path
from PIL import Image
import numpy as np

def get_rgbDset(directory, nrow, ncol, imgtype='jpg', save='no', r_name='x_r.csv', g_name='x_g.csv', b_name='x_b.csv', label_name='y.csv'):
    """
    Read multiple RGB images and return 4D numpy array. 
    Image must JPG file.
    General assumption each class separated in different folder
    -------
    Parameters
    directory : directory containing images. image with different label should be located in different folder
    nrow : width of desired image ouput
    ncol : height of desired image ouput
    imgtype : file extension of image. default is jpg
    """
    # define image file extension
    imgtype = '*.' + imgtype
    # get all folder/directory in path
    dirname = Path(directory)
    folder = [f.name for f in dirname.iterdir() if f.is_dir()]
    # create variable to save label and image
    label = []    
    images = np.zeros((1,nrow,ncol,3), 'uint8')

    for i in range (len(folder)):
        for filename in Path(directory+folder[i]).rglob(imgtype):
            image = np.array(Image.open(filename).resize((nrow,ncol)))
            image = np.expand_dims(image, axis=0)
            images = np.concatenate((images,image), axis=0)
            label.append(folder[i])    
    images = np.delete(images, (0), axis=0)
    #label = np.array(label)
    
    if (save=='no'):
        return images, label
    elif (save=='yes'):
        r = images[:,:,:,0].reshape(-1, nrow*ncol)
        g = images[:,:,:,1].reshape(-1, nrow*ncol)
        b = images[:,:,:,2].reshape(-1, nrow*ncol)
        np.savetxt(r_name, r.astype(int), delimiter=',', fmt='%d')
        np.savetxt(g_name, g.astype(int), delimiter=',', fmt='%d')
        np.savetxt(b_name, b.astype(int), delimiter=',', fmt='%d')
        np.savetxt(label_name, label, delimiter=',')

        return 'images data and its label are saved in csv files'

def construct_image(r, g, b, ncol, nrow):
    r = r.reshape(ncol, nrow).astype('uint8')
    g = g.reshape(ncol, nrow).astype('uint8')
    b = b.reshape(ncol, nrow).astype('uint8')

    img = np.dstack((r, g, b))

    return img
