
import cv2
import os
import pytesseract
from PIL import Image
import sys
import numpy as np
import argparse


pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'

# The list of allergens in 4 languages: English, French, Russian, and Spanish
IallergicEng=['Gluten','milk','peanuts','Soy','tuna','Eggs','Fish','nuts','tonsils']
IallergicFra=['Gluten', 'lait', 'cacahuètes', 'soja', 'thon', 'œufs', 'poisson', 'noix', 'amygdales']
IallergicRus=['Глютен', 'молоко', 'арахис', 'соя', 'тунец', 'яйца', 'рыба', 'орехи', 'миндалины']
IallergicSpa=['Gluten', 'leche', 'maní', 'soja', 'atún', 'huevos', 'pescado', 'nueces', 'amígdalas']

'''
Image processing function:
Gets 3 parameters: the list of allergens for testing,
 the path of the image to be tested,
and the processing language
 
 Returns a final answer in str if the product is allowed to be eaten
'''
def Answer_processing(arrAllerg, path, lang):

  if path=="galleryToCameraPage.png":
      return "Product image not captured, please return to previous step"

  # Arranging the path
  path = path.replace('\\\\', "/")
  path=path.replace("[\'","")
  path=path.replace("\']","")
  image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
  cv2.imwrite('thresh.png', image)# white on black

  img = Image.open('thresh.png')

  #Optimal resolution for the process according to tests we did
  width, heightS = img.size
  new_size = width*3, heightS*3
  img = img.resize(new_size, Image.LANCZOS)
  img = img.point(lambda x:0 if x < 128 else 200, '1')

  # Use OCR to read the text from the image  according to the language selected

  if lang=="English":
    data = pytesseract.image_to_string(img, lang='eng')
    arrAllergLang=IallergicEng
  if lang == "Spanish":
      data = pytesseract.image_to_string(img, lang='spa')
      arrAllergLang = IallergicSpa
  if lang == "Russian":
      data = pytesseract.image_to_string(img, lang='rus')
      arrAllergLang = IallergicRus
  if lang == "French":
      data = pytesseract.image_to_string(img, lang='fra')
      arrAllergLang = IallergicFra


#Download markings that will interfere with the identification of the text
#according to tests we have done
  data=data.replace(',', '')
  data=data.replace('.','')
  print(data)#for us
  #Unity in uppercase and lowercase letters
  dataLower=data.lower()

  dataArry= dataLower.split()#Division into an array
  cantEat=False
  #We will go through the list of allergens from the user and look in the text layout
  for i in arrAllerg:
      word=arrAllergLang[int(i)]
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

