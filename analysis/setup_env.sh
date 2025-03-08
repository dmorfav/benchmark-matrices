#!/bin/bash

# Crear entorno virtual
echo "Creando entorno virtual..."
python3 -m venv env

# Activar entorno virtual
echo "Activando entorno virtual..."
source env/bin/activate

# Actualizar pip y setuptools
echo "Actualizando pip y herramientas básicas..."
pip install --upgrade pip setuptools wheel

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

echo "Entorno configurado correctamente. Para activar el entorno ejecuta:"
echo "source env/bin/activate"
echo ""
echo "Para ejecutar el script de análisis:"
echo "python analizar_resultados.py" 