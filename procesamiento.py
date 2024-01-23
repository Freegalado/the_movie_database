from descompresion import merge_by_pandas
import pandas as pd


def change_type_col(df: pd.DataFrame, col: str, dtype: str) -> pd.Series:
    """
    Se recibe el nombre de una columna y se cambia su dtype.

    Arg:
    df -> dataframe
    col -> columna del dataframe
    dtype -> tipo de dato

    Return:
    df_col -> pandas series con un cambio de dtype
    """

    df_col = df[col].astype(dtype)

    return df_col


def air_days(df: pd.DataFrame, start: str, end: str) -> pd.Series:
    """
    Se realiza la resta de dos fechas.

    Arg:
    df -> dataframe con los datos
    start -> columna con la fecha de inicio
    end -> columna con la fecha final

    Return:
    days -> pandas series con el número de días
    """
    air_days = df[end] - df[start]
    days = air_days.dt.days

    return days


def drop_na(df: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    """
    Se revisan las columnas provistas para revisar si contienen ,
    valores nulos.

    Arg:
    df -> dataframe con los datos
    start -> columna con la fecha de inicio
    end -> columna con la fecha final

    Return:
    df -> dataframe sin valores nulos
    """

    df = df.dropna(subset=[start, end])

    return df


def compare_dates(df: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    """
    Se revisa que la columna final es mayor a la inicial, para tener
    coherencia en las fechas. No puede haber una fecha del tipo
    inicio: 2023-08-12 final: 2010-05-10

    Arg:
    df -> dataframe con los datos
    start -> columna con la fecha de inicio
    end -> columna con la fecha final

    Return:
    df -> dataframe con fechas correctas
    """

    df = df[df[start] < df[end]]
    return df


def longest_emission(df: pd.DataFrame, days: str) -> None:
    """
    Se recibe el dataframe el cual se ordena según la columna ingresada, se imprime
    el head y un texto.

    Arg:
    df -> dataframe con los datos a ordenar
    days -> columna por la cual se realizará la ordenación

    Return:
    None
    """

    df = df.sort_values(by=days, ascending=False)
    print('Los primeros 10 registros del dataset con el mayor número\n'
          'de emisión son:\n')
    print(df.head(10))


def create_dict_url(df: pd.DataFrame, name: str, homepage: str, poster: str) -> dict:
    """
    Se recibe un dataframe con un set de columnas para devolver el nombre de la serie (name),
    una url que se creará con la union de las columnas homepage y poster. Se devolverá un
    diccionario con dicha información. Si alguna de las columnas que componen el url esta
    vacio, la url completa será NOT AVAILABLE.

    Arg:
    df -> dataframe con los datos
    name -> columna con el nombre de las series
    homepage -> columna con la ruta incompleta del poster
    poster -> columna con el nombre del fichero que contiene la imagen del poster

    Return
    series_dict -> diccionario con el nombre de la serie y su url del poster
    """
    series_dict = {}

    for index, row in df.iterrows():
        names = row[name]
        homepages = row[homepage] if pd.notna(row[homepage]) and row[homepage] != "" else "NOT AVAILABLE"
        poster_path = row[poster] if pd.notna(row[poster]) and row[poster] != "" else "NOT AVAILABLE"

        # Verificar si alguna es "NOT AVAILABLE"
        if homepages == "NOT AVAILABLE" or poster_path == "NOT AVAILABLE":
            series_dict[names] = {'url': "NOT AVAILABLE"}
        else:
            series_dict[names] = {'url': homepages + poster_path}

    return series_dict


def first_items(dic: dict, N: int) -> None:
    """
    Se recibe un diccionario y se define el número de elementos a mostrar,
    se imprime los resultados.

    Arg:
    dic ->  diccionario con los datos
    N -> número de elementos a mostrar

    Return:
    None
    """
    print(f"Los primeros {N} registros del diccionario mostrando nombre y url son:")
    for key, value in list(dic.items())[:N]:
        print(f"{key}: {value}")


def main():
    path_dir = './data/'  # ruta con los datos

    _, data = merge_by_pandas(path_dir)  # Concanetación de datos

    df = data.copy()  # Copia del dataframe para modificarlo

    # 2.1

    # Cambio de dtypes de object a datetime
    df['first_air_date'] = change_type_col(df, 'first_air_date', 'datetime64[ns]')
    df['last_air_date'] = change_type_col(df, 'last_air_date', 'datetime64[ns]')

    # Eliminación de filas con valores nulos
    df = drop_na(df, 'first_air_date', 'last_air_date')

    # Comparación de fechas para coherencia
    df = compare_dates(df, 'first_air_date', 'last_air_date')

    # Obtención del número de días
    df['air_days'] = air_days(df, 'first_air_date', 'last_air_date')

    print('Ejercicio 2.1\n')

    # Impresión de las series con mayor serialización
    longest_emission(df, 'air_days')

    # Ejercicio 2.2
    # Diccionario con la serie y la url de su poster
    dict_url_poster = create_dict_url(data, 'name', 'homepage', 'poster_path')

    print('Ejercicio 2.2\n')

    # Impresión de los primeros items del diccionario
    first_items(dict_url_poster, 5)


if __name__ == '__main__':
    main()
