# Análisis de datos de peliculas  

El repositorio se compone de los siguientes archivos:
- main.py
- descompresion.py
- procesamiento.py
- filtrado.py
- visualización.py
- test.py
- conclusiones.md
- coverage.sh
- requirements.txt


El fichero main.py puede abrirse mediante consola 
con el siguiente comando una vez te encuentres
en la carpeta contenedora:

$ python main.py

Comenzará la ejecución de cada script de forma
secuencial o abrir cada módulo por separado, 
siempre comenzando con descompresión.py

Para la ejecución de los test y su cobertura
puede ejecutarse el script en bash:

$ bash ./coverage.sh

Ejecutará los comando para realizar el test y 
su covertura, dependendiendo de tu sistema
linux, unix o windows abrirá tu navegador
predeterminado el reporte en html.

Las conclusiones se encuentran también en formato
markdown así que pueden abrirse con un editor 
de texto.

Para la instalación de las dependencias tienes
que situarte en la tu enviroment y poner:

$ pip install -r requirements.txt

Licencia:
Apache-2.0 license
