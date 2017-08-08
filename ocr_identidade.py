import pytesseract
import os
from PIL import Image
import cv2
import numpy as np


#detalhe, converter as imagens para RGBA é crucial para o alpha_composite,
# assim como redimensiona-las de forma espelhada também.
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
# inserir o caminho do seu tesseract, caso ele não esteja definido nas suas variaveis de ambiente 

dir_mascaras = ['masks/' + mask for mask in os.listdir('masks/')]  #captura todas as mascaras disponiveis no diretorio masks


def binarize(img):  #definindo binarização dos cortes
    a = np.asarray(img)
    a = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY)
    ret, imbin = cv2.threshold(a, 127, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)
    return Image.fromarray(imbin)


def mesclarImagem(mascara):  #mescla a respectiva mascara a identidade
    identidade = Image.open('identidade.jpg').resize(mascara.size).convert('RGBA')
    mescla = Image.alpha_composite(identidade, mascara)
    return binarize(mescla)
    #return mescla

# criando de fato, nossa lista de imagens pre-processadas para o OCR tesseract
imMascaras = [mesclarImagem(Image.open(mascara).convert('RGBA')) for mascara in dir_mascaras]

data_book = {}  # com isto, poderemos consultar qualquer campo da nossa identidade por meio do nosso data book!
for i, mask in enumerate(dir_mascaras):
    campo = mask.replace('masks/', '').replace('.png', '')
    data_book.__setitem__(campo, imMascaras[i])

# agora, geramos o json identidade -- begin
text_list = [pytesseract.image_to_string(imgMasc, lang='por') for imgMasc in imMascaras]

identidade_dict = {}
for i, textfield in enumerate(data_book):
    identidade_dict.__setitem__(textfield, text_list[i])

print(identidade_dict)  #imprime toda a identidade em json!!

## end

#print(pytesseract.image_to_string(data_book['data_exp'], lang='por'))  # uso individual do OCR para os campos da identidade, enjoy!
#data_book['data_exp'].show() #  tambem pode visualizar a imagem de cada campo individualmente, usado para ver o resultado dos filtros aplicados
