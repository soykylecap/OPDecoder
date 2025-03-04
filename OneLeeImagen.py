import cv2 as cv
import sys
import numpy as np
import pytesseract as pt
from PIL import ImageGrab
#import pyperclip

def LeerOP():
    pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    imagen = cv.imread(cv.samples.findFile("OP5x5.jpg"), cv.IMREAD_GRAYSCALE)

    imagen = ImageGrab.grabclipboard()
    imagen = cv.cvtColor(np.array(imagen), cv.COLOR_RGB2GRAY)






    if imagen is None:
        sys.exit("No puedo encontrar la imagen")

    imagen = cv.threshold(imagen, 200, 255, cv.THRESH_BINARY)[1] #la pasa a blanco y negro

    # cv.imshow("byN", imagen)
    # cv.waitKey(3000)
    # cv.destroyAllWindows()

    alto = np.shape(imagen)[0]
    ancho = np.shape(imagen)[1]


    # -----------------------------------------
    # Acá quiero determinar automaticamente de que tamaño es el OnePuzzle

    imagen_bordes = cv.Canny(imagen, 1, 100)
    lineas = cv.HoughLinesP(imagen_bordes,1,np.pi/180,1)
    for linea in lineas:
        x1, y1, x2, y2 = linea[0]
        cv.line(imagen_bordes, (x1,y1), (x2,y2), (255), 1)

    # cv.imshow("", imagen_bordes)
    # cv.waitKey(0)
    # cv.destroyAllWindows()




    #-------------------------------------------

    tamaño = 5
    tamaño_celda = int((ancho + alto) / 2 / tamaño)
    #acá extraigo los numeros de cada celda
    inicia_numeros = list()
    topes_derecha = list()
    topes_abajo = list()

    for fila in range(tamaño): 
        for columna in range(tamaño):

            # Reconocimiento OCR
            celda = imagen[(tamaño_celda*fila)+10:(tamaño_celda*(fila+1))-10, (tamaño_celda*columna)+10:(tamaño_celda*(columna+1))-10]
            
            numero = pt.image_to_string(celda, config='--psm 10 -c tessedit_char_whitelist=123456789')
            numero = numero.strip()
            if numero == "": 
                numero = None
            else:
                numero = int(numero)
            inicia_numeros.append(numero)

            # Identifico los topes 
            # Primero lo hago con los de la derecha
            
            if columna != tamaño-1:
                raya_derecha = imagen_bordes[(tamaño_celda*fila)+20:(tamaño_celda*(fila+1))-20, (tamaño_celda*(columna+1))-20:(tamaño_celda*(columna+1))+20]
                lineas_celda = cv.HoughLinesP(raya_derecha,1,np.pi/180,1)
                if lineas_celda[0][0][0] - lineas_celda[1][0][0] >= 8:
                    topes_derecha.append(True)
                else:
                    topes_derecha.append(False)
            else:
                topes_derecha.append(True)

            # Ahora lo hago con los de abajo

            if fila != tamaño-1:
                raya_abajo = imagen_bordes[(tamaño_celda*(fila+1))-20:(tamaño_celda*(fila+1))+20, (tamaño_celda*(columna))+20:(tamaño_celda*(columna+1))-20]
                # cv.imshow("h", raya_abajo)
                # cv.waitKey(0)
                # cv.destroyAllWindows()
                lineas_celda = cv.HoughLinesP(raya_abajo,1,np.pi/180,50)
                # print (fila,columna)
                # print (lineas_celda[1][0][1])
                # print (lineas_celda[0][0][1])

                if lineas_celda[1][0][1] - lineas_celda[0][0][1] >= 8:
                    topes_abajo.append(True)
                else:
                    topes_abajo.append(False)
            else:
                topes_abajo.append(True)

    inicia_numeros = tuple(inicia_numeros)
    topes_derecha = tuple(topes_derecha)
    topes_abajo = tuple(topes_abajo)

    return inicia_numeros, topes_abajo, topes_derecha

    # cv.imshow("Imagen capturada", imagen_bordes)
    # cv.waitKey(0)
    # cv.destroyAllWindows()


