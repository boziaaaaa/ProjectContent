#coding=utf8
from PIL import Image
import pytesseract
image = Image.open(r'./picture/src/111.PNG')
# code = pytesseract.image_to_string(image,lang='chi_sim')
code = pytesseract.image_to_string(image)

print(code)
