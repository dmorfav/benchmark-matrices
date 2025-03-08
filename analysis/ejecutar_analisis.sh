#!/bin/bash

# Activar entorno virtual (ajustar la ruta para ir al directorio superior)
source ../env/bin/activate

# Ejecutar script de análisis
python analizar_resultados.py

echo "Análisis completado. Revisa la carpeta actual para ver los resultados." 