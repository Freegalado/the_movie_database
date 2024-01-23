import pandas as pd

from descompresion import merge_by_pandas
from procesamiento import change_type_col


def filter_by_languages_genre(df: pd.DataFrame, col_lang: str,
                              lang: str, overview: str, genre1: str, genre2: str) -> pd.DataFrame:
    """
    Se filtra un dataframe que busca palabras dentro de una columna con texto cumpliendo la
    condición de encontrar ambas, teniendo otra condición de tener la coincidencia en una columna.

    Arg:
    df -> dataframe con los datos
    col_lang -> columna en la cual realizar la búsqueda
    lang -> palabra a buscar
    overview -> texto en el cual realizar la busqueda de palabras
    genre1 -> palabra 1 a buscar
    genre2 -> palabra 2 a buscar

    Return:
    filtered_series -> filas que cumplen la condición en la columna y en el texto
    """
    filtered_series = df[(df[col_lang] == lang) & (df[overview].str.lower().str.contains(genre1 + '|' + genre2))]
    return filtered_series


def series_to_list(df: pd.DataFrame, name: str) -> list:
    """
    Se provee un dataframe y una columna para obtener una serie y transformarla en una lista

    Arg:
    df -> dataframe con los datos

    Return:
    list_names -> lista con los valores de la columna
    """
    list_names = df[name].tolist()
    return list_names


def print_names(serie_list: list) -> None:
    """
    Función que sirve para imprimir los elementos de una serie, tambien
    imprime un texto descriptivo.

    Arg:
    serie_list: lista con los valores de la serie

    Return:
    None
    """
    print('\nLas series en idioma original inglés que contienen los géneros\n'
          'crimen y misterio son :')
    for serie in serie_list:
        print(serie)


def filter_by_status(df: pd.DataFrame, start: str, status: str,
                     byYear: int, byStatus: str) -> pd.DataFrame:
    """
    Se obtiene una serie bajo dos condiciones, la primera es que haya coincidencia con el año y
    la segunda es que se encuentre una palabra en otra columna.

    Arg:
    df: El dataframe con los datos
    start: columna con las fechas de inicio
    status: columna con el estado de la serie
    byYear: año a buscar
    byStatus: estado de la serie a buscar

    Return:
    filtered_series: dataframe con las coincidencias en año y estado de búsqueda
    """
    filtered_series = df[(df[start].dt.year == byYear) & (df[status].str.lower().str.contains(byStatus))]
    return filtered_series


def print_names_list(lista: list, nElements: int) -> None:
    """
    Imprime los elementos de una lista, el número de elementos son definidos en la función

    Arg:
    lista: lista con los elementos a imprimir
    nElements: número de elementos de la lista a imprimir

    Return:
    None
    """
    slice_list = lista[:nElements]
    print(f'\nLas {nElements} series que iniciaron en el 2023 y fueron canceladas son:')
    for serie in slice_list:
        print(serie)


def filter_by_language(df: pd.DataFrame, col: str, lang: str) -> pd.Series:
    """
    Se recibe un dataframe que sera filtrado mediante una palabra en una columna

    Arg:
    df: dataframe con los datos
    col: columna con los datos
    lang: palabra a buscar

    Return:
    filtered_series: serie con los valores filtrados
    """
    filtered_series = df[df[col].str.lower().str.contains(lang, na=False)]
    return filtered_series


def filter_by_column(df: pd.DataFrame, col: str) -> pd.Series:
    """
    Obtención de una serie de un dataframe

    Arg:
    df: dataframe con los valores
    col: columna a convertir en serie

    Return:
    filtered_series: serie del dataframe
    """
    filtered_series = df[col]
    return filtered_series


def print_df_rows(df: pd.DataFrame, nElements: int) -> pd.DataFrame:
    """
    Se obtienen un determinado número de filas como encabezado

    Arg:
    df: dataframe con los valores
    nElements: número de filas

    Return:
    df: encabezado con determinado número de filas
    """
    df = df.head(nElements)
    return df


def main():
    path_dir = './data/'  # ruta con los datos

    _, data = merge_by_pandas(path_dir)  # Concanetación de datos

    df = data.copy()  # Copia del dataframe para modificarlo

    # Ejercicio 3.1

    filtered_by_lang_genres = filter_by_languages_genre(df, 'original_language',
                                                        'en', 'overview',
                                                        'mystery', 'crime')

    name_series = series_to_list(filtered_by_lang_genres, 'name')

    print('\nEjercicio 3.1\n')
    print_names(name_series)  # impresion de las series

    # Ejercicio 3.2

    # Cambio de tipo de dato a datetime
    df['first_air_date'] = change_type_col(df, 'first_air_date', 'datetime64[ns]')

    # Filtrado por año y estado
    filtered_status_series = filter_by_status(df, 'first_air_date',
                                              'status', 2023, 'canceled')

    # transformación de la serie a una lista
    canceled_list_series = series_to_list(filtered_status_series, 'original_name')

    print('\nEjercicio 3.2\n')
    print_names_list(canceled_list_series, 20)

    # filtrado del dataframe por lengua japonesa
    japaneses_languages_series = filter_by_language(df, 'languages', 'ja')

    # Subset de columnas
    cols_filters = ['name', 'original_name', 'networks', 'production_companies']

    # subset del dataframe
    jap_series = filter_by_column(japaneses_languages_series, cols_filters)

    print('\nEjercicio 3.2\n')
    print(print_df_rows(jap_series, 20))


if __name__ == '__main__':
    main()
