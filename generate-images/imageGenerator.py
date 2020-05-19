#!/usr/bin/env python3
from numpy.random import Generator, MT19937
import numpy as np
from PIL import Image, ImageFont, ImageDraw
from PIL import ImageFilter
from itertools import count
from string import ascii_lowercase,digits,printable
from glob import glob
def imageSsizesGen(rnd):
  a = 500*[(800,600)]+500*[(1024,768)]
  rnd.shuffle(a)
  return tuple(a)

def textGen(rnd,size,font):
     rndStr = ''.join(rnd.choice(tuple(ascii_lowercase+digits),size=8))
     img = Image.new("RGB", size, (0,0,0))
     draw = ImageDraw.Draw(img)
     for i in range(8):
       position = (rnd.integers(0,size[0]),rnd.integers(0,size[1])) 
       color = tuple(rnd.integers(128,255) for i in '...')
       draw.text(position, rndStr , color, font=font)
     sign = {True : 1, False : -1}[rnd.integers(2) == 0]
     for r in sign*rnd.random(8):
       img = img.rotate(r)

     font = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf',80)  
     draw = ImageDraw.Draw(img)
     draw.text((10,10), rndStr , (255,255,255), font=font)   

     return img

patternsFontPath = glob('/usr/share/fonts/truetype/lyx/*.ttf')
def LayerPattern(rnd,size,patternsFontPath = patternsFontPath):
     img = Image.new("RGB", size, (0,0,0))
     draw = ImageDraw.Draw(img)
     for i in range(40):
       position = (rnd.integers(0,size[0]),rnd.integers(0,size[1])) 
       font = ImageFont.truetype(rnd.choice(patternsFontPath),rnd.integers(40,80))  
       color = tuple(rnd.integers(128,255) for i in '...')
       draw.text(position, rnd.choice(tuple(printable)) , color, font=font)
     sign = {True : 1, False : -1}[rnd.integers(2) == 0]
     for r in sign*2*rnd.random(8):
       img = img.rotate(r)
     return img

def main():
  rnd = Generator(MT19937(0))
  #fontsFilenames = glob('/usr/share/fonts/truetype/lyx/*.ttf')#glob("/usr/share/fonts/truetype/**/*.ttf",recursive=True)
  for index,size in  zip(count(),imageSsizesGen(rnd)):
     #fontname = rnd.choice(fontsFilenames)
     #font = ImageFont.truetype(fontname,rnd.integers(25,40))
     filename = '{:0>3}.jpg'.format(index)
     print(filename,size)
     img = LayerPattern(rnd,size)#textGen(rnd,size,font)
     a = np.array((np.array(img)>0),dtype=np.uint8)
     b = np.array(Image.new("RGB", size, tuple(rnd.integers(128) for i in '...')))
     b[rnd.choice(size[1],size=50)] = tuple(rnd.integers(128) for i in '...')
     c = (1-a)*b+np.array(img)
     c[rnd.choice(size[1],size=50)] = tuple(rnd.integers(128) for i in '...')
     img = Image.fromarray(c, 'RGB')
     font = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf',40)  
     draw = ImageDraw.Draw(img)
     draw.text((10,10),(5*' ')+filename + ' {}*{}'.format(size[0],size[1]), (255,255,255), font=font)  
     img.save(filename,quality=100)
if __name__=='__main__':
  main()
