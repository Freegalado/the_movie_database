import matplotlib.pyplot as plt
import seaborn as sns
from descompresion import merge_by_pandas
from procesamiento import change_type_col
import pandas as pd

sns.set_style('darkgrid')
plt.style.use('ggplot')


def plot_series_year_start(df: pd.DataFrame, byYear: str) -> None:
    """
    Se realiza un gráfico de barras ordenadas, mostrando el conteo de los valores
    de la columna ingresada, tomando los valores de la columna como indíce.

    Arg:
    df: dataframe con los datos
    byYear: columna a utilizar para la gráfica en formato datetime

    Return:
    None

    """
    # conteo y ordenación de los valores
    series_per_year = df[byYear].dt.year.value_counts().sort_index()

    # Crear el gráfico de barras
    plt.figure(figsize=(14, 8))
    sns.barplot(x=series_per_year.index.astype('int'), y=series_per_year.values)
    plt.title('Número de Series por Año de Inicio')
    plt.xlabel('Año de Inicio')
    plt.ylabel('Número de Series')
    plt.xticks(rotation=90, ha='center')
    plt.tight_layout()
    plt.show()

def plot_series_by_decade(df: pd.DataFrame, byStart: str) -> None:
    """
    Se reciben los valores de tiempo (año), para realizar una operación y encontrar
    la década del valor, este se usará para realizar el recuento de los valores de tiempo
    y se realizará un gráfico de líneas por tipo de serie. Se filtran los valores para empezar
    desde 1940.

    Arg:
    df: dataframe con los valores
    byStart: columna con valores de tiempo

    Return:
    None
    """
    # Crear una nueva columna 'decade' basada en el año de inicio de la serie
    df['decade'] = (df[byStart].dt.year // 10) * 10

    # Filtrar las series producidas desde 1940
    df = df[df[byStart].dt.year >= 1940]

    # Crear el gráfico de líneas
    plt.figure(figsize=(14, 8))
    sns.lineplot(x='decade', y='count', hue='type', data=df.groupby(['decade', 'type']).size().reset_index(name='count'))
    plt.title('Número de Series por Categoría y Década')
    plt.xlabel('Década')
    plt.ylabel('Número de Series')
    plt.legend(title='Categoría')
    plt.show()

def plot_genre_percentage(df: pd.DataFrame, byGenre: str) -> None:
    """
    Se realiza un gráfico circular, mostrando los porcentajes por genero de los
    valores de la columna proporcionada, cuando el porcentaje del genero es menor al
    1% se colocan dentro de la categoría Other.

    Arg:
    df: dataframe con los valores
    byGenre: columna que contiene los generos

    Return:
    None
    """
    # Filtrar las series con el campo "genres" no vacío
    df = df.dropna(subset=[byGenre])

    # Contar el número de series por género
    genre_counts = df[byGenre].str.split(', ').explode().value_counts()

    # Calcular el porcentaje respecto al total
    total_series = genre_counts.sum()
    genre_percentage = genre_counts / total_series * 100

    # Agrupar géneros que representan menos del 1% del total en la categoría "Other"
    threshold = 1.0
    small_genres = genre_percentage[genre_percentage < threshold]
    genre_percentage = genre_percentage[genre_percentage >= threshold]
    genre_percentage['Other'] = small_genres.sum()

    # Crear un gráfico circular
    plt.figure(figsize=(12, 12))
    plt.pie(genre_percentage, labels=genre_percentage.index, autopct='%1.1f%%',
            startangle=90, textprops={'size': 'smaller',
                                      'rotation_mode': 'anchor',
                                      'ha': 'center',
                                      'va': 'center',
                                      'rotation': 90}, pctdistance=0.85)
    plt.title('Porcentaje de Series por Género')
    plt.show()


def main():
    path_dir = './data/'

    _, data = merge_by_pandas(path_dir)

    df = data.copy()

    df['first_air_date'] = change_type_col(df, 'first_air_date', 'datetime64[ns]')

    # Ejercicio 4.1
    plot_series_year_start(df,'first_air_date')

    # Ejercicio 4.2
    plot_series_by_decade(df,'first_air_date')

    # Ejercicio 4.3
    plot_genre_percentage(df, 'genres')

if __name__ == '__main__':
    main()

