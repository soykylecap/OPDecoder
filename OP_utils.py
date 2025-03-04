
import sys
import math
from collections import Counter

def horizontalizar(maximo, datos):
    recorrido = list() #En esta variable defino una nueva manera de recorrer las listas de datos. Hace el zigzag recorriendo primero todas las celdas de cada columna.
    for columna in range(maximo):
        for fila in range(maximo):
            recorrido.append(columna + (maximo * fila))
    topes_abajo_horizontalizados = list()
    for r in recorrido:
        topes_abajo_horizontalizados.append(datos[r]) #En esta lista quedan los datos verticales ordenados para que se recorran como si fuesen horizontales
    return topes_abajo_horizontalizados, recorrido


class Celda:
    def __init__(self, fila, columna, ubicacion, final_abajo, final_derecha, numero_inicio = None, segmento_horizontal = None, segmento_vertical = None, max_posible = None, numero = None, candidatos = None):
        self.fila = fila
        self.columna = columna
        self.ubicacion = ubicacion
        self.final_abajo = final_abajo
        self.final_derecha = final_derecha
        self.numero_inicio = numero_inicio
        self.segmento_horizontal = segmento_horizontal
        self.segmento_vertical = segmento_vertical
        self.numero = numero
        self.max_posible = max_posible
        self.candidatos = candidatos
    
    def __repr__(self):
        return f"F{self.fila},C{self.columna}: Max: {self.max_posible} Pos: {self.ubicacion} Cand: {self.candidatos} SH: {self.segmento_horizontal} SV: {self.segmento_vertical} \n"


class Tablero:
    def __init__(self, maximo, topes_abajo, topes_derecha, inicia_numeros, celdas = None):
        self.maximo = maximo
        self.topes_abajo = topes_abajo
        self.topes_derecha = topes_derecha
        self.inicia_numeros = inicia_numeros
        self.celdas = celdas

    def configurar_celdas(self):
        lista_celdas = list()
        for pos in range(self.maximo ** 2):
            fila = (pos // self.maximo) + 1
            columna = (pos + 1) - (fila - 1) * self.maximo
            celda = Celda(fila, columna, pos, self.topes_abajo[pos], self.topes_derecha[pos], self.inicia_numeros[pos])  #crea una celda en el tablero con los datos que ya tengo
            lista_celdas.append(celda) #agrega esa posicion configurada a la lista de celdas
        #return lista_celdas
        self.celdas = lista_celdas

    def maximos_horizontales(self):
        #Defino maximos y a que segmento pertenece cada celda (segun filas)
        maximos = []
        cuenta_falsos = 0
        celda = -1
        topes = self.topes_derecha
        for tope in topes:
            celda = celda + 1
            if tope:
                cuenta_falsos += 1
                for a in range(cuenta_falsos): 
                    maximos.append(cuenta_falsos) #Cuando encuentra un tope derecho, define el numero maximo y lo anota tantas veces como espacios hubo hasta encontrarlo.
                cuenta_falsos = 0
            else:
                cuenta_falsos += 1

        #Agrego esos maximos y los segmentos a las celdas
        for n in range(self.maximo ** 2):
            self.celdas[n].max_posible = maximos[n]

    def segmentos_horizontales(self):
        segmentos = []
        celdas_en_segmento = []
        celda = -1
        topes = self.topes_derecha
        for tope in topes:
            celda = celda + 1
            if tope:
                celdas_en_segmento.append(celda)
                segmentos.append(celdas_en_segmento)
                celdas_en_segmento = []
            else:
                celdas_en_segmento.append(celda)

        #Agrego esos segmentos a las celdas
        for n in range(self.maximo ** 2):
            for indice, sublista in enumerate(segmentos):
                if n in sublista:
                    self.celdas[n].segmento_horizontal = indice + 1


    def maximos_verticales(self):
        datos = horizontalizar(self.maximo, self.topes_abajo) 
        topes = datos[0]
        recorrido = datos[1]
        #Ahora puedo aplicar el mismo codigo que en los horizontales. AHORA PUEDO HACER UNA MISMA FUNCION PARA AMBOS.
        maximos = []
        cuenta_falsos = 0
        celda = -1
        for tope in topes:
            celda = celda + 1
            if tope:
                cuenta_falsos += 1
                for a in range(cuenta_falsos): 
                    maximos.append(cuenta_falsos) #Cuando encuentra un tope derecho, define el numero maximo y lo anota tantas veces como espacios hubo hasta encontrarlo.
                cuenta_falsos = 0
            else:
                cuenta_falsos += 1

        #Agrego esos maximos a las celdas
        for n, r in enumerate(recorrido): 
            if maximos[r] < self.celdas[n].max_posible:
                self.celdas[n].max_posible = maximos[r]


    def segmentos_verticales(self):
        datos = horizontalizar(self.maximo, self.topes_abajo) 
        topes = datos[0]
        recorrido = datos[1]
        #Ahora puedo aplicar el mismo codigo que en los horizontales. AHORA PUEDO HACER UNA MISMA FUNCION PARA AMBOS.
        segmentos = []
        celdas_en_segmento = []
        celda = -1
        for tope in topes:
            celda = celda + 1
            if tope:
                celdas_en_segmento.append(celda)
                segmentos.append(celdas_en_segmento)
                celdas_en_segmento = []
            else:
                celdas_en_segmento.append(celda)

        #Agrego esos segmentos a las celdas
        for n, r in enumerate(recorrido): 
            for indice, sublista in enumerate(segmentos):
                if r in sublista:
                    self.celdas[n].segmento_vertical = indice + 1


    def __str__(self):
        return str(self.maximo)
    
    def __repr__(self):
        return f"F{self.fila},C{self.columna}: Max: {self.max_posible} Pos: {self.ubicacion} Cand: {self.candidatos} SH: {self.segmento_horizontal} SV: {self.segmento_vertical}"



class Candidatos:
    def __init__(self, tablero):
        self.tablero = tablero
    
    def buscar_candidatos(self):
        for c in self.tablero.celdas:
            if c.numero_inicio != None:
                c.candidatos = [c.numero_inicio, ]
                c.numero = c.numero_inicio

    def elimina_candidatos_repetidos(self):
        for c in self.tablero.celdas:
            candidatos = list()
            if c.numero_inicio == None:
                for candidato in range(c.max_posible): #En cada celda, pone todos los candidatos de acuerdo al maximo posible
                    candidatos.append(candidato + 1)
                for c2 in self.tablero.celdas:
                    if c2.segmento_horizontal == c.segmento_horizontal:
                        if c2.numero in candidatos: candidatos.remove(c2.numero) #Elimina de candidatos los numeros que existen en la misma fila.
                for c3 in self.tablero.celdas:
                    if c3.segmento_vertical == c.segmento_vertical:
                        if c3.numero in candidatos: candidatos.remove(c3.numero) #Elimina de candidatos los numeros que existen en la misma fila.
                
            c.candidatos = candidatos

            if len(candidatos) == 1:
                c.numero = candidatos[0]

    def unico_en_segmento_horizontal(self):
        segmentos = dict()
        celdas_en_segmento = []
        for seg in range(1, self.tablero.celdas[-1].segmento_horizontal + 1):
            for celda in self.tablero.celdas:
                if celda.segmento_horizontal == seg:
                    celdas_en_segmento.append(celda.candidatos)
                    segmentos.update({seg:celdas_en_segmento})
                else:
                    celdas_en_segmento = []

        #Lo siguiente toma cada segmento, recorre todos los candidatos y buscar algun numero que sea candidato en una sola celda.
        for seg in segmentos:
            segmento = segmentos[seg]
            segmento = [num for sublista in segmento for num in sublista]
            contados = Counter(segmento) #Hace un diccionario donde el key es el numero y su valor la cantidad de veces que aparece en la lista
            for index, valor in contados.items(): #Busca alguna key con valor 1
                if valor == 1: 
                    for celda in self.tablero.celdas:
                        #print (self.tablero.celdas[24].numero)
                        if celda.segmento_horizontal == seg and index in celda.candidatos:   #Acá hay que reemplazar el 1 por el numero de segmento.
                            celda.numero = index
                            print(f"El numero del segmento {seg} es el {index} y está en la celda {celda}")


def resolver(intentos, tablero):
    intento = 0
    while intento <= intentos:
        intento = intento + 1
        candidatos = Candidatos(tablero)
        candidatos.buscar_candidatos()
        candidatos.elimina_candidatos_repetidos()
        #candidatos.unico_en_segmento_horizontal() #Acá hay algo mal xq a veces asigna mal





# Hacer una clase para definir candidatos, con diferentes metodos.
# El primero es si hay una pista en esa celda
# Luego pongo todos los candidatos segun maximo posible en cada celda
# Luego elimino los candidatos que ya están en ese segmento (tanto vertical como horizontal)
# Ahora busco algun numero que este como candidato en SOLO una celda del segmento. Usar conjuntos




