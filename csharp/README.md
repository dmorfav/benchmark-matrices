# Implementación de Multiplicación de Matrices en C#

Esta carpeta contiene la implementación del benchmark de multiplicación de matrices utilizando C#.

## Descripción

El código implementa un algoritmo naïve de multiplicación de matrices cuadradas, carga las matrices desde archivos JSON, mide el tiempo de ejecución y registra los resultados en un archivo CSV.

## Requisitos

- .NET SDK 6.0 o superior
- No se requieren librerías de terceros, solo se utilizan librerías estándar de .NET

## Compilación

Para compilar el proyecto, ejecute el siguiente comando en la terminal:

```bash
dotnet build
```

## Ejecución

Para ejecutar el benchmark, utilice el siguiente comando:

```bash
dotnet run --n 500 --iterations 10
```

Donde:
- `--n`: Dimensión de las matrices cuadradas (por defecto: 500)
- `--iterations`: Número de iteraciones para medir el tiempo promedio (por defecto: 10)

## Estructura del Código

El código está organizado en las siguientes funciones principales:

1. `LoadMatrix`: Carga una matriz desde un archivo JSON.
2. `MultiplyMatrices`: Implementa el algoritmo naïve de multiplicación de matrices.
3. `MeasureMultiplication`: Mide el tiempo de ejecución de múltiples iteraciones.
4. `RegistrarResultados`: Registra los resultados en un archivo CSV.

## Resultados

Los resultados se guardan en el archivo `results/benchmark_csharp_results.csv` con los siguientes campos:
- `language`: El lenguaje utilizado (C#)
- `matrix_size`: Tamaño de las matrices
- `iterations`: Número de iteraciones
- `individual_times`: Tiempos individuales de cada iteración
- `average_time`: Tiempo promedio de ejecución
