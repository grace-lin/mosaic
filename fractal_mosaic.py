import os
import math
import Image
from mosaic import Mosaic
from mosaic import _find_closest
from mosaic import _image_value

class FractalMosaic(Mosaic):
    '''A better picture made of smaller pictures.'''
    
    def __init__(self, path):
        '''Create contents of FractalMosaic object, storing a picture database
        indicated by path.'''
        
        Mosaic.__init__(self, path)
        
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
        
def _create_mosaic(direc, pic, min_size, threshold):
    '''Replace a picture, pic, with another if the picture is smaller than
    min_size.'''
        
    if pic.size[0] < min_size or pic.size[1] < min_size:
        close = _find_closest(direc, _image_value(pic))
        new_close = close.resize((pic.size[0], pic.size[1]))
        pic.paste(new_close, (0, 0))
        
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

def _matches(direc, th, pic):
    '''If the color distance between an image from database direc and pic is
    less than threshold th, return the image.'''
    
    for i in direc.keys():
        total = 0
        resized = i.resize((pic.size[0], pic.size[1]))
        for p, q in zip(resized.getdata(), pic.getdata()): # compare each pixel
            total += math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + \
                               (p[2] - q[2]) ** 2)

        average = total / (pic.size[0] * pic.size[1])
        
        if average < th:
            return resized
        
    return None

if __name__ == '__main__':
    di = 'C:\Documents and Settings\User\My Documents\Grace\Y3\CSC148\A4\dali'
    m = FractalMosaic(di)
    #name = 'C:\\Documents and Settings\\User\\My Documents\\Grace\\Anime pics\\CCS-Sakura, Tam cerub xmas.jpg'
    name = 'C:\\Documents and Settings\\User\\Desktop\\karan.jpg'
    #name = 'C:\\Documents and Settings\\User\\My Documents\\Grace\\Anime pics\\Elfen Lied-Lucy bookmark.jpg'
    m.create_mosaic(name, 10, 60)
    m.save_as('C:\\Documents and Settings\\User\\My Documents\\o_new.jpg')
    print 'yay'