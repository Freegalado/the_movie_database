#!/bin/bash

# Correr las pruebas con coverage
coverage run -m unittest test.py

# Generar el informe HTML
coverage html

# Usar el comando de navegador proporcionado para abrir el informe
xdg-open ./htmlcov/index.html || open ./htmlcov/index.html || start ./htmlcov/index.html

