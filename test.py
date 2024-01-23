import unittest
import zipfile as zf
from glob import glob
from descompresion import extract_files, merge_by_pandas, csv_by_dictionary, ejercicio_uno_cuatro
from filtrado import (filter_by_languages_genre, filter_by_language, filter_by_column,
                      filter_by_status, change_type_col, series_to_list, print_df_rows)
from procesamiento import compare_dates, create_dict_url
import os
import pandas as pd


class TestDescompresion(unittest.TestCase):

    def setUp(self):
        self.df_test = pd.DataFrame({
            'name': ['Serie A', 'Serie B', 'Serie C', 'Serie D', 'Serie E',
                     'Serie F', 'Serie G', 'Serie H'],
            'date': ['2010-10-03', '2015-10-03', '2015-10-03', '2010-10-13',
                     '2007-10-03', '2023-10-03', '2005-07-03', '2011-03-03'],
            'date2': ['2015-10-03', '2005-10-03', '2016-10-03', '2010-12-13',
                      '2008-10-03', '2009-10-03', '2007-07-03', '2018-03-03'],
            'poster': ["image1.jpg", "", "pic_01.jpg", "image_001.jpg", "picture_1.jpg",
                       "photo123.jpg", "pic01.jpg", ""],
            'path': ["https://example.com/", "https://example.com/photos/", "https://example.net/pictures/",
                     "https://example.org/images/", "https://sample-site.com/gallery/",
                     "https://image-hosting-service.com/user123/",
                     "https://cdn.example.com/assets/", "https://static-images.net/img/"],
            'original_language': ['en', 'es', 'en', 'fr', 'en', 'ru', 'po', 'chi'],
            'overview': ['mystery with crime', 'drama opera', 'action movies', 'comedy central',
                         'just mystery', 'dramatic very dramatic', 'unknown genre', 'no idea about'],
            'languages': ['ja,ko', 'ro', 'ja,ro0', 'JA', 'es', 'it', 'ko', 'en'],
            'status': ['active', 'standby', 'cancelled', 'active', 'standby', 'cancelled',
                       'active', 'standby']

        })

        self.path_dir = './data/'
        self.path_test_dir = './data/test/'

    def test_extract_files(self):
        """Test de la función extract_files"""

        self.clean_after_tests = False  # No limpiar después de esta prueba

        # Prueba para la función extract_files

        if not os.path.exists(self.path_test_dir):
            os.makedirs(self.path_test_dir)

        with open(os.path.join(self.path_test_dir, 'test_file1.csv'), 'w') as file1:
            file1.write('id,value1,value2\n1,100,casa\n2,200,piso\n')

        with open(os.path.join(self.path_test_dir, 'test_file2.csv'), 'w') as file2:
            file2.write('id,value3,value4\n3,300,solar\n4,400,piso\n')

        zip_filename = './data/test/test_files.zip'

        with zf.ZipFile(zip_filename, 'w') as zipf:
            for root, _, files in os.walk(self.path_test_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, self.path_test_dir))

        extract_files(zip_filename, self.path_test_dir)

        files_test = glob(self.path_test_dir + '*.csv')

        # Verifica que los archivos están presentes en el directorio
        self.assertTrue(os.path.exists(files_test[0]))
        self.assertTrue(os.path.exists(files_test[1]))

    def test_merge_by_pandas(self):
        self.clean_after_tests = False  # No limpiar después de esta prueba

        """Prueba para la función merge_by_pandas"""

        # Llama a la función de merge y verifica el DataFrame resultante
        elapsed_time, df = merge_by_pandas(self.path_test_dir)

        self.assertEqual(df.iloc[0]['value4'], 'solar')
        self.assertEqual(df.iloc[1]['value4'], 'piso')

    def test_csv_by_dictionary(self):
        """Test para la función csv_by_dictionary"""

        # Llama a la función de crear diccionario y verifica el resultado
        elapsed_time, csv_dict = csv_by_dictionary(self.path_test_dir)

        self.assertEqual(csv_dict[1]['value1'], '100')
        self.assertEqual(csv_dict[2]['value2'], 'piso')

    def test_ejercicio_uno_cuatro(self):
        """Test para la función ejercicio_uno_cuatro"""

        # Comprueba que la función se ejecute sin errores
        text = ejercicio_uno_cuatro()

        self.assertIn('chunks', text, "La palabra no se encontró en el texto.")
        self.assertIn('vectorizada', text, "La palabra no se encontró en el texto.")

    def test_compare_dates(self):
        """Test para la función compare_dates"""

        good_dates = compare_dates(self.df_test, 'date', 'date2')
        # Realiza aserciones sobre el resultado
        self.assertEqual(len(good_dates), 6)

    def test_create_dict(self):
        """Test para la función create_dict"""

        dict_url_poster = create_dict_url(self.df_test, 'name', 'path', 'poster')

        not_available_count = sum(1 for serie in dict_url_poster.values() if serie['url'] == 'NOT AVAILABLE')

        # Verificar que el resultado coincide con el esperado
        self.assertEqual(not_available_count, 2)

    def test_filter_by_languages_genre(self):
        """Test para la función filter_by_languages_genre"""

        # Llama a la función de filtrado
        result = filter_by_languages_genre(self.df_test, 'original_language', 'en', 'overview', 'mystery', 'crime')

        # Realiza aserciones sobre el resultado
        self.assertEqual(len(result), 2)  # Asegura que hay dos series que cumplen con los criterios

    def test_filtered_by_language(self):
        """Test para la función filtered_by_language"""

        languages_series = filter_by_language(self.df_test, 'languages', 'ja')
        self.assertEqual(languages_series.iloc[0]['languages'],
                         'ja,ko')
        self.assertEqual(languages_series.iloc[2]['languages'],
                         'JA')

    def test_filtered_by_date(self):
        """Test para la función filtered_by_date"""
        self.df_test.date = change_type_col(self.df_test, 'date', 'datetime64[ns]')

        status_series = filter_by_status(self.df_test, 'date', 'status', 2010, 'active')

        self.assertEqual(len(status_series), 2)
        self.assertEqual(self.df_test.date.dtype, 'datetime64[ns]')

    def test_series_to_list(self):
        """Test para la función series_to_list"""

        name_series = series_to_list(self.df_test, 'name')

        self.assertEqual(type(name_series), list)

    def test_filter_by_col(self):
        """ test para la función filter_by_col"""

        name_series = filter_by_column(self.df_test, 'name')
        self.assertEqual(type(name_series), pd.core.series.Series)

    def test_header(self):
        """Test para la funcion print_df_rows"""

        df_head = print_df_rows(self.df_test, 2)
        self.assertEqual(len(df_head), 2)

    def tearDown(self):
        """Elimina los archivos creados despues de algunos test"""

        if hasattr(self, 'clean_after_tests') and self.clean_after_tests:
            files_test = glob('./data/test/*')
            for f in files_test:
                os.remove(f)
            os.rmdir('./data/test/')


if __name__ == '__main__':
    unittest.main()
