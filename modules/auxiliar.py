# --- Funciones auxiliares. ----

def mapear_valores (matriz: list[list], indice_a_mapear: int, callback):
    """
    Mapeamos los datos -- > Necesitamos ints
    Usamos callback para llamar a parsear enteros
    """
    for indice_fila in range(len(matriz)):
        valor = matriz[indice_fila][indice_a_mapear]
        matriz[indice_fila][indice_a_mapear] = callback(valor)


def parsear_entero(valor:str):
    """
    Si el valor es un entero, lo devuelve como tal, sino, no.
    """
    if valor.isdigit():
        return int(valor)
    return valor



# -- Archivos
def cargar_ranking(file_path: str, top: int):
    """
    Abre el archivo con el ranking, y lo vuelve una matriz para poder trabajar.
    Parsea los números, y la ordena
    """
    ranking = []
    with open(file_path, 'r', encoding='utf-8') as file:
        texto = file.read()

    for linea in texto.split('\n'):
        if linea:
            lista_datos_linea = linea.split(',')
            ranking.append(lista_datos_linea) #Append aldo del estilo = [nombre, puntaje]
            #Ambos elementos son strings todavia
    
    mapear_valores(ranking, indice_a_mapear= 1, callback=parsear_entero)

    ranking = ranking[1:] #Para que no haya problemas con los str

    ranking.sort(key=lambda fila: fila[1], reverse= True) #Ordenamos segun el puntaje numérico (DESC)


    return ranking[:top]

