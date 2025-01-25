import sys
import math

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
    
    def __str__(self):
        return str(self.maximo)
    
    def __repr__(self):
        return f"F{self.fila},C{self.columna}: Max: {self.max_posible} Pos: {self.ubicacion} Cand: {self.candidatos} SH: {self.segmento_horizontal} SV: {self.segmento_vertical}"


# Quiero una funcion que separe en segmentos (verticales y horizontales) a los tableros. Actualmento esto lo hace la clase Maximos cuando se definen estos, pero quiero separar las tareas.


class Maximos:
    def __init__(self, tablero):
        self.tablero = tablero
        #self.tablero.celdas = celdas
        # self.topes_derecha = topes_derecha
        # self.topes_abajo = topes_abajo

    def horizontales(self):
        #Defino maximos y a que segmento pertenece cada celda (segun filas)
        maximos_horizontales = []
        segmentos_horizontales = []
        celdas_en_segmento = []
        cuenta_falsos = 0
        celda = -1
        for cel in self.tablero.topes_derecha:
            celda = celda + 1
            if cel:
                celdas_en_segmento.append(celda)
                for a in range(cuenta_falsos + 1):
                    maximos_horizontales.append(cuenta_falsos + 1)
                segmentos_horizontales.append(celdas_en_segmento)
                cuenta_falsos = 0
                celdas_en_segmento = []
            else:
                cuenta_falsos += 1
                celdas_en_segmento.append(celda)

        #Agrego esos maximos y los segmentos a las celdas
        for n in range(self.tablero.maximo ** 2):
            self.tablero.celdas[n].max_posible = maximos_horizontales[n]
            for indice, sublista in enumerate(segmentos_horizontales):
                if n in sublista:
                    self.tablero.celdas[n].segmento_horizontal = indice + 1

    def verticales(self):

        

        #Quiero encontrar una manera de recorrer las celdas a traves de las columnas como si estuviesen dispuestas horizontalmente. 





        #voy a convertir las columnas en filas para aplicar el mismo codigo que los horizontales.
        verticales_procesados = list()
        celdas_procesadas = []
        for fila in range(self.tablero.maximo):
            for columna in range(self.tablero.maximo):
                celdas_procesadas.append(fila + (self.tablero.maximo * columna))

        for n in range(self.tablero.maximo):
            columna = self.tablero.topes_abajo[n::self.tablero.maximo]
            verticales_procesados.append(columna)
        verticales_procesados = sum(verticales_procesados, ())
        verticales_procesados = tuple(verticales_procesados)

        #Defino maximos y a que segmento pertenece cada celda (segun columnas)
        maximos_verticales = []
        segmentos_verticales = []
        celdas_en_segmento = []
        cuenta_falsos = 0
        celda = -1
        for cel in verticales_procesados:
            celda = celda + 1
            if cel:
                celdas_en_segmento.append(celda)
                for a in range(cuenta_falsos + 1):
                    maximos_verticales.append(cuenta_falsos + 1)
                segmentos_verticales.append(celdas_en_segmento)
                cuenta_falsos = 0
                celdas_en_segmento = []
            else:
                cuenta_falsos += 1
                celdas_en_segmento.append(celda)

        #Regreso de Columnas a filas:
        regreso_horizontales = list()
        for n in range(self.tablero.maximo):
            fila = maximos_verticales[n::self.tablero.maximo]
            regreso_horizontales.append(fila)

        #Aplano la tupla    
        maximos_verticales = [item for sublist in regreso_horizontales for item in sublist]


        #Agrego esos maximos y esos segmentos a las celdas
        for n in range(self.tablero.maximo ** 2):
            if maximos_verticales[n] < self.tablero.celdas[n].max_posible:
                self.tablero.celdas[n].max_posible = maximos_verticales[n]

            nueva_ubicacion = celdas_procesadas.index(n)
            for indice, sublista in enumerate(segmentos_verticales):
                if n in sublista:
                    self.tablero.celdas[nueva_ubicacion].segmento_vertical = indice + 1

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

def resolver(intentos, tablero):
    maximos = Maximos(tablero)
    maximos.horizontales()
    maximos.verticales()

    intento = 0
    while intento <= intentos:
        intento = intento + 1
        candidatos = Candidatos(tablero)
        candidatos.buscar_candidatos()
        candidatos.elimina_candidatos_repetidos()


# Hacer una clase para definir candidatos, con diferentes metodos.
# El primero es si hay una pista en esa celda
# Luego pongo todos los candidatos segun maximo posible en cada celda
# Luego elimino los candidatos que ya están en ese segmento (tanto vertical como horizontal)
# Ahora busco algun numero que este como candidato en SOLO una celda del segmento. Usar conjuntos




