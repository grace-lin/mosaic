import os
import math
import Image

class Mosaic(object):
    '''A picture made of smaller pictures.'''
    
    def __init__(self, path):
        '''Create contents of Mosaic object, storing a picture database
        indicated by path.'''
        
        imgs = os.listdir(path)
        files = {} # put each image with its average value into a dictionary
        for i in imgs[:-1]:
            pic = Image.open(os.path.join(path, i))
            files[pic] = _image_value(pic)
        self.files = files
        self.mosaic = None
        
    def create_mosaic(self, filename, min_size):
        '''Create and store a photomosaic version of the single picture
        specified by filename.'''
        
        pic = Image.open(filename)
        mosaic = _create_mosaic(self.files, pic, min_size)
        self.mosaic = mosaic
    
    def save_as(self, filename):
        '''Save the resulting photomosaic to file at filename.'''
        
        if self.mosaic: # save only if a mosaic has been created
            self.mosaic.save(filename)

def _create_mosaic(direc, pic, min_size):
    '''Replace a picture, pic, with another if the picture is smaller than
    min_size.'''
    
    if pic.size[0] < min_size or pic.size[1] < min_size:
        close = _find_closest(direc, _image_value(pic))
        new_close = close.resize((pic.size[0], pic.size[1]))
        pic.paste(new_close, (0, 0))
    
    else:        
        x, y = pic.size[0], pic.size[1]
        
        # splitting the original picture into quarters
        a, b, c, d = pic.crop((0, 0, x / 2, y / 2)), \
         pic.crop((x / 2, 0, x, y / 2)), pic.crop((0, y / 2, x / 2, y)), \
         pic.crop((x / 2, y / 2, x, y))
        
        pic.paste(_create_mosaic(direc, a, min_size), (0, 0))
        pic.paste(_create_mosaic(direc, b, min_size), (x / 2, 0))
        pic.paste(_create_mosaic(direc, c, min_size), (0, y / 2))
        pic.paste(_create_mosaic(direc, d, min_size), (x / 2, y / 2))
        
    return pic

def _find_closest(d, pic_c):
    '''From directory d, return the Color-closest picture to the given
    colour, pic_c, of a picture.'''
    
    close = d.keys()[0] # use the first so there's something to compare to
    dist = math.sqrt((pic_c[0] - d[close][0]) ** 2 + \
                     (pic_c[1] - d[close][1]) ** 2 + \
                     (pic_c[2] - d[close][2]) ** 2)
    if len(d.keys()) > 1: # compare other pictures if there other exist
        for i in d.keys()[1:]:
            new_dist = math.sqrt((pic_c[0] - d[i][0]) ** 2 + \
                                 (pic_c[1] - d[i][1]) ** 2 + \
                                 (pic_c[2] - d[i][2]) ** 2)
            if new_dist < dist:
                close, dist = i, new_dist
    return close

def _image_value(pic):
    '''Return an average Colour value represented as a tuple (R, G, B) for
    image pic.'''

    hist = pic.histogram()
    R, G, B = hist[:256], hist[256:512], hist[512:]
    pix = pic.size[0] * pic.size[1] # number of pixels
    if pix == 0:
        return (0, 0, 0)
    
    r_total, g_total, b_total = 0, 0, 0
    for i in range(256): #this will give indices
        r_total += i * R[i]
        g_total += i * G[i]
        b_total += i * B[i]
    return (r_total / pix, g_total / pix, b_total / pix)

if __name__ == '__main__':
    di = 'C:\Documents and Settings\User\My Documents\Grace\Y3\CSC148\A4\dali'
    m = Mosaic(di)
    name = 'C:\\Documents and Settings\\User\\My Documents\\Grace\\Anime pics\\CCS-Sakura, Tam cerub xmas.jpg'
    m.create_mosaic(name, 20)
    m.save_as('C:\\Documents and Settings\\User\\My Documents\\new.jpg')
    print 'yay'