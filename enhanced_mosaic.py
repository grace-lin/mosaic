import os
import math
import Image
import copy
from mosaic import Mosaic
from mosaic import _image_value

class EnhancedMosaic(Mosaic):
    '''A better picture made of smaller pictures.'''
    
    def __init__(self, path):
        '''Create contents of FractalMosaic object, storing a picture database
        indicated by path.'''
        
        imgs = os.listdir(path)
        files = {} # put each image with its average value into a dictionary
        for i in imgs[:-1]:
            pic = Image.open(os.path.join(path, i))
            files[pic] = (_image_value(pic), _mipmap(pic))
        self.files = files
        self.mosaic = None
        
        # to find which image to resize from, take the smallest side, s_s
        # math.floor(math.log(s_s, 2)) will return to what power s_s is of 2
        # resize from the array[^]
        
    def create_mosaic(self, filename, min_size, threshold):
        '''Create and store a photomosaic version of the single picture
        specified by filename, replacing any similar region with a matching
        picture that meets threshold.'''

        pic = Image.open(filename)
        mosaic = _create_mosaic(self.files, pic, min_size, threshold)
        self.mosaic = mosaic        
    
    def save_as(self, filename):
        '''Create and store a photomosaic version of the single picture
        specified by filename.'''
        
        Mosaic.save_as(self, filename)
        
def _create_mosaic(direc, pic, min_size, threshold, ):
    '''Replace a picture, pic, with another if the picture is smaller than
    min_size.'''
        
    if pic.size[0] < min_size or pic.size[1] < min_size:
        close = _find_closest(direc, _image_value(pic))
        mm = _smallest(direc[close][1], pic) # returns resized close
        pic.paste(mm, (0, 0))
        
    else:
        match = _matches(direc, threshold, pic)
        if match: # if pic matches any image in direc
            pic.paste(match, (0, 0))
            return pic
            
        x, y = pic.size[0], pic.size[1]
        
        # splitting pic into quarters
        a, b, c, d = pic.crop((0, 0, x / 2, y / 2)), \
         pic.crop((x / 2, 0, x, y / 2)), pic.crop((0, y / 2, x / 2, y)), \
         pic.crop((x / 2, y / 2, x, y))
        
        pic.paste(_create_mosaic(direc, a, min_size, threshold), (0, 0))
        pic.paste(_create_mosaic(direc, b, min_size, threshold), (x / 2, 0))
        pic.paste(_create_mosaic(direc, c, min_size, threshold), (0, y / 2))
        pic.paste(_create_mosaic(direc, d, min_size, threshold), \
                  (x / 2, y / 2))
        
    return pic

def _find_closest(d, pic_c):
    '''From directory d, return the Color-closest picture to the given
    colour, pic_c, of a picture.'''
    
    close = d.keys()[0] # use the first so there's something to compare to
    dist = math.sqrt((pic_c[0] - d[close][0][0]) ** 2 + \
                     (pic_c[1] - d[close][0][1]) ** 2 + \
                     (pic_c[2] - d[close][0][2]) ** 2)
    if len(d.keys()) > 1: # compare other pictures if there other exist
        for i in d.keys()[1:]:
            new_dist = math.sqrt((pic_c[0] - d[i][0][0]) ** 2 + \
                                 (pic_c[1] - d[i][0][1]) ** 2 + \
                                 (pic_c[2] - d[i][0][2]) ** 2)
            if new_dist < dist:
                close, dist = i, new_dist
    return close

def _matches(direc, th, pic):
    '''If the color distance between an image from database direc and pic is
    less than threshold th, return the image.'''
    
    for i in direc.keys():
        total = 0
        mm = _smallest(direc[i][1], pic) # returns resized i
        for p, q in zip(mm.getdata(), pic.getdata()): # compare each pixel
            total += math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + \
                               (p[2] - q[2]) ** 2)

        average = total / (pic.size[0] * pic.size[1])
        if average < th:
            return mm
        
    return None

def _mipmap(pic):
    '''Given an image pic, return a list images of pic scaled in half each time
    until a side of 1 pixel is reached.'''
    
    # ==> this will save time on resizing in _create_mosaic, _matches
    
    mipmap = [pic]
    while min(pic.size) > 1:
        pic = pic.resize((pic.size[0] / 2, pic.size[1] / 2))
        mipmap.insert(0, pic)
    return mipmap

def _smallest(mipmap, pic):
    '''Returns an image from mipmap the same size as pic.'''

    smallest = min(pic.size)
    index = int(math.floor(math.log(smallest, 2)))
    if index > len(mipmap) - 1:
        mm = copy.copy(mipmap[-1])
    else:
        mm = copy.copy(mipmap[index])
    
    if mm.size != pic.size: # if there is one side different from pic
        mm = mm.resize((pic.size[0], pic.size[1]))
    return mm

if __name__ == '__main__':
    di = 'C:\Documents and Settings\User\My Documents\Grace\Y3\CSC148\A4\dali'
    m = EnhancedMosaic(di)
    name = 'C:\\Documents and Settings\\User\\My Documents\\Grace\\Anime pics\\CCS-Sakura, Tam cerub xmas.jpg'
    #name = 'C:\\Documents and Settings\\User\\My Documents\\Grace\\Y3\\CSC148\\A4\\karan.jpg'
    #name = 'C:\\Documents and Settings\\User\\My Documents\\Grace\\Anime pics\\Elfen Lied-Lucy bookmark.jpg'
    m.create_mosaic(name, 10, 60)
    m.save_as('C:\\Documents and Settings\\User\\My Documents\\o_new.jpg')
    print 'yay'