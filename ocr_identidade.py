"""
    Detalhe, converter as imagens para RGBA é crucial para o alpha_composite,
    assim como redimensiona-las de forma espelhada também.

"""
import os

from PIL import Image
import cv2
import pytesseract as ocr
import numpy as np
import json


def binarizar(img):  # definindo binarização dos cortes
    a = np.asarray(img)
    a = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY)
    ret, imbin = cv2.threshold(a, 127, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)
    return Image.fromarray(imbin)


def mesclar_imagem(mascara):  # mescla a respectiva mascara a identidade
    identidade = Image.open('identidade.jpg').resize(mascara.size).convert('RGBA')
    mescla = Image.alpha_composite(identidade, mascara)
    return binarizar(mescla)

# criando de fato, nossa lista de imagens pre-processadas para o OCR tesseract
DIR_MASCARAS = ['masks/' + mask for mask in os.listdir('masks/')]
MASCARAS = [mesclar_imagem(Image.open(mascara).convert('RGBA')) for mascara in DIR_MASCARAS]

# com isto, poderemos consultar qualquer campo da nossa identidade
# por meio do nosso data book!
DATA_BOOK = {}
for i, mask in enumerate(DIR_MASCARAS):
    campo = mask.replace('masks/', '').replace('.png', '')
    DATA_BOOK.__setitem__(campo, MASCARAS[i])

# agora, geramos o json identidade
text_list = [ocr.image_to_string(imgMasc, lang='por') for imgMasc in MASCARAS]

identidade_dict = {}
for i, textfield in enumerate(DATA_BOOK):
    identidade_dict.__setitem__(textfield, text_list[i])

print(json.dumps(identidade_dict, indent=4))  # imprime toda a identidade em json!!
