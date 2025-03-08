# Benchmark de Multiplicación de Matrices en Python

Este directorio contiene una implementación naïve del algoritmo de multiplicación de matrices en Python.

## Requisitos

- Python 3.6 o superior
- Bibliotecas estándar de Python (json, time, argparse, os, csv)

## Ejecución

Para ejecutar el benchmark, usa el siguiente comando desde el directorio `python/`:

```bash
python main.py
```

Por defecto, el programa utiliza matrices de 500x500 y realiza 10 iteraciones.

### Opciones

Puedes personalizar la ejecución mediante las siguientes opciones:

- `--n`: Dimensión de las matrices cuadradas (por defecto: 500)
- `--iterations`: Número de iteraciones para medir el tiempo promedio (por defecto: 10)

Ejemplo:

```bash
python main.py --n 1000 --iterations 5
```

## Características

El programa:
1. Carga matrices desde archivos JSON almacenados en el directorio `data/`
2. Realiza la multiplicación de matrices usando un algoritmo naïve
3. Mide los tiempos de ejecución para cada iteración
4. Calcula y muestra el tiempo promedio
5. Registra los resultados para análisis comparativo

## Funciones principales

- `load_matrix()`: Carga una matriz desde un archivo JSON
- `multiply_matrices()`: Implementa el algoritmo de multiplicación de matrices
- `measure_multiplication()`: Mide los tiempos de ejecución
- `registrar_resultados()`: Guarda los resultados en un archivo CSV

## Resultados

Los resultados se guardan en el archivo `results/benchmark_python_results.csv`, incluyendo:

- Lenguaje: Python
- Tamaño de matriz
- Número de iteraciones
- Tiempos individuales
- Tiempo promedio
