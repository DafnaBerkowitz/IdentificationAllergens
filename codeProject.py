
import cv2
import os
import pytesseract
from PIL import Image
import sys
import numpy as np
import argparse
# Designate Our .kv design file

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
sys.path.append(r'C:\Users\Pc\source\repos\WpfApp1\packages\IronPython.2.7.11\lib')
IallergicEng=['Gluten','milk','peanuts','Soy','tuna','Eggs','Fish','nuts','tonsils']
IallergicFra=['Gluten', 'lait', 'cacahuètes', 'soja', 'thon', 'œufs', 'poisson', 'noix', 'amygdales']
IallergicRus=['Глютен', 'молоко', 'арахис', 'соя', 'тунец', 'яйца', 'рыба', 'орехи', 'миндалины']
IallergicSpa=['Gluten', 'leche', 'maní', 'soja', 'atún', 'huevos', 'pescado', 'nueces', 'amígdalas']

def try3(arrAllerg,path):
  path = path.replace('\\\\', "/")
  path=path.replace("[\'","")
  path=path.replace("\']","")
  image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
  #thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

  result = 255 - image

  #data = pytesseract.image_to_string(result, lang='eng',config='--psm 10 ')
  #print(data)
  cv2.imwrite('thresh.png', image)
  cv2.imwrite('result.png', result)

  img = Image.open('thresh.png')
  img.convert(mode='L').save('img2.jpg')
  img=Image.open('img2.jpg')
  #רזולוציה
  width, heightS = img.size
  new_size = width*3, heightS*3
  img = img.resize(new_size, Image.LANCZOS)
  img = img.point(lambda x:0 if x < 128 else 200, '1')

  # Use OCR to read the text from the image
  #out_below = pytesseract.image_to_string(img)

  # Print the text
  #print(out_below)
  data = pytesseract.image_to_string(img, lang='eng')
  print(data)

  data=data.replace(',', '')
  data=data.replace('.','')
  print(data)
  dataLower=data.lower()
  dataArry= dataLower.split()
  cantEat=False
  for i in arrAllerg:
      word=IallergicEng[int(i)]
      wlower = word.lower()
      for j in dataArry:
          jlower = j.lower()
          if wlower==jlower:
              cantEat=True
              break

  if cantEat==True:
      return("You can't eat this!")

  else:
      return("With an appetite!")

