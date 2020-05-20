#!/usr/bin/env python3
from numpy.random import Generator, MT19937
import numpy as np
from PIL import Image, ImageFont, ImageDraw
from PIL import ImageFilter
from itertools import count
from string import printable
def imageSsizesGen(rnd):
  a = 500*[(800,600)]+500*[(1024,768)]
  rnd.shuffle(a)
  return tuple(a)

patternsFontPath = ('/usr/share/fonts/truetype/lyx/cmex10.ttf',
 '/usr/share/fonts/truetype/lyx/rsfs10.ttf',
 '/usr/share/fonts/truetype/lyx/eufm10.ttf',
 '/usr/share/fonts/truetype/lyx/cmr10.ttf',
 '/usr/share/fonts/truetype/lyx/stmary10.ttf',
 '/usr/share/fonts/truetype/lyx/cmmi10.ttf',
 '/usr/share/fonts/truetype/lyx/msbm10.ttf',
 '/usr/share/fonts/truetype/lyx/msam10.ttf',
 '/usr/share/fonts/truetype/lyx/wasy10.ttf',
 '/usr/share/fonts/truetype/lyx/cmsy10.ttf',
 '/usr/share/fonts/truetype/lyx/esint10.ttf')
def imagePattern(img,rnd,patternsFontPath = patternsFontPath):
     draw,size = ImageDraw.Draw(img),img.size
     for fontSize in rnd.integers(5*[150,220]+10*[100,110]+10*[30,80]):
       position = (rnd.integers(0,size[0]),rnd.integers(0,size[1]))
       font = ImageFont.truetype(rnd.choice(patternsFontPath),fontSize)
       color = tuple(rnd.integers(115,250) for i in '...')
       draw.text(position, rnd.choice(tuple(printable)) , color, font=font)
def main():
  rnd = Generator(MT19937(0))
  font = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf',40)
  for index,size in  zip(count(),imageSsizesGen(rnd)):
     filename = '{:0>3}.jpg'.format(index)
     text = filename + ' {}x{}'.format(size[0],size[1])
     print(text)
     backgroundColor = tuple(rnd.integers(128) for i in '...')
     img = Image.new("RGB", size, backgroundColor)
     imagePattern(img,rnd)
     draw = ImageDraw.Draw(img)
     textSize=font.getsize(text)
     draw.rectangle([30,30] + [textSize[0]+30] + [textSize[1]+30], fill=backgroundColor)
     draw.text((30,30),text, tuple(128+np.array(backgroundColor,dtype=np.uint8)), font=font)
     img.save("../pictures/"+filename,quality=100)
if __name__=='__main__':
  main()
