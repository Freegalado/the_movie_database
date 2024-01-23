import zipfile as zf
from glob import glob
import re
import time
import pandas as pd
import csv


def extract_files(origin: str, dest: str) -> None:
    """
    Se recibe una ruta donde se encuentra el archivo
    descomprimido, verifica que los ficheros tienen
    la extensión .zip o tar.gz y se extrae su contenido
    en la misma ruta.

    Arg:
    path_dir -> ruta a los archivos

    Return:
    None
    """

    regex = re.compile(r'[\\/]')  # Busca la \ y / en la ruta para sistemas unix y windows
    file = regex.split(origin)[-1]  # Separa la ruta y se queda con la parte final que es el archivo

    # Buscar archivos del tipo
    zip_file = ".zip"
    tar_file = "tar.gz"

    # Si no existe archivos a buscar se muestran mensaje de error
    if zip_file not in file and tar_file not in file:
        raise ValueError('Proceso Finalizado: El fichero no es tiene extensión .zip o .tar.gz')

    # Abrimos el archivo zip en modo de lectura
    with zf.ZipFile(origin, 'r') as zip_f:
        # Descompresión de archivos
        zip_f.extractall(dest)

    print('Descompresión Finalizada \n')


def merge_by_pandas(path_dir: str) -> tuple[float, pd.DataFrame]:
    """
    Se recibe una ruta donde se encuentran los archivos,
    se buscan todos los archivos csv, se concatenan por el
    indice. Se devuelve el DF y el tiempo de ejecución

    Arg:
    path_dir -> ruta a los archivos

    Return:
    df -> DataFrame de los archivos concatenados
    elapsed_time -> tiempo de ejecución
    """
    # Iniciar el contador de tiempo
    start = time.time()

    #  Búsqueda de archivos
    list_files = sorted(glob(path_dir + '*.csv'), reverse=True)

    # Concatenación de archivos por la columna id
    df_concat = pd.concat([pd.read_csv(f, sep=',', index_col='id') for f in list_files],
                          ignore_index=False, axis=1)

    end = time.time()

    elapsed_time = end - start

    return elapsed_time, df_concat


def csv_by_dictionary(path_dir: str) -> tuple[float, dict]:
    """
        Se recibe una ruta donde se encuentran los archivos,
        se buscan todos los archivos csv, se iteran en los datos
        para crear el diccionario.

        Arg:
        path_dir -> ruta a los archivos

        Return:
        final_dict -> diccionario con los datos
        elapsed_time -> tiempo de ejecución
        """

    # Iniciar el contador de tiempo
    start_time = time.time()

    # Inicializar el diccionario resultante
    final_dict = {}

    # Obtener la lista de archivos CSV en la carpeta
    list_files = glob(path_dir + '*.csv')

    # Iterar sobre la lista de archivos CSV e ir almacenando en el diccionario
    for file in list_files:
        with open(file, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                # Utilizar la columna 'id' como clave en el diccionario
                id = row['id']
                final_dict[int(id)] = row

    # Detener el contador de tiempo
    end_time = time.time()

    elapsed_time = end_time - start_time
    return elapsed_time, final_dict


# Ejercicio 1.4
def ejercicio_uno_cuatro() -> str:
    """
    Función que no recibe parámetros contiene un string
    que es devuelto.

    Arg:
    None

    Return:
    text -> texto del problema
    """

    text = ('\nLa principal diferencia al utilizar la función'
            'dict_reader vs reader_csv es que en la primera se realiza\n'
            'un proceso de lectura linea a linea\n'
            'mediante un iterador y en la segunda una la lectura vectorizada '
            'de los datos.\n'
            'Esto quiere decir que se pueden procesar datos por columnas enteras.\n'
            'Lo que hace a pandas una herramienta para cargar y procesar una gran cantidad\n'
            'de datos, en el caso de tener que trabajar con un total de 10 GB\n'
            'tendría que conocer la capacidad de memoria en la maquina local.\n'
            'Pero en general seguiría utilizando pandas pero haría la carga de datos\n'
            'por trozos (chunks) para tener un mejor manejo de memoria.\n')

    return text


def main():
    path_file = './data/TMDB.zip'
    path_dir = './data/'

    # 1.1
    extract_files(path_file, path_dir)

    # 1.2
    elapsed_time, df = merge_by_pandas(path_dir)

    print(f'El tiempo de ejecución de la union de DataFrames fue de {elapsed_time:.4f} segundos. \n')
    print(df.head())

    # 1.3
    elapsed_time, csv_dict = csv_by_dictionary(path_dir)

    print(f'El tiempo de ejecución de la realización del diccionario fue de {elapsed_time:.4f} segundos. \n')
    print('Se muestran los items de la key 60140 \n')
    print(csv_dict[60140])

    # 1.4
    print(ejercicio_uno_cuatro())


if __name__ == "__main__":
    main()
