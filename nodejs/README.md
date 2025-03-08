# Benchmark de Multiplicación de Matrices en Node.js

## Descripción

Esta es la implementación en Node.js del benchmark de multiplicación de matrices. El programa carga dos matrices desde archivos JSON, realiza la multiplicación utilizando un algoritmo naïve, mide los tiempos de ejecución y guarda los resultados en un archivo CSV.

## Requisitos

- Node.js 14.x o superior
- Paquete commander (se instalará con npm)

## Instalación

Antes de ejecutar el benchmark, es necesario instalar las dependencias:

```bash
npm install commander
```

## Uso

Para ejecutar el benchmark con los parámetros predeterminados:

```bash
node main.js
```

### Opciones

- `-n, --dimension <n>`: Especifica la dimensión de las matrices cuadradas a multiplicar (predeterminado: 500).
- `-i, --iterations <count>`: Especifica el número de iteraciones para calcular el tiempo promedio (predeterminado: 10).

Ejemplo:

```bash
node main.js -n 1000 -i 5
```

O usando los nombres largos:

```bash
node main.js --dimension 1000 --iterations 5
```

## Resultados

Los resultados se guardan en el archivo `results/benchmark_nodejs_results.csv` con los siguientes campos:
- language: El lenguaje utilizado (Node.js)
- matrix_size: Dimensión de las matrices
- iterations: Número de iteraciones ejecutadas
- individual_times: Tiempos individuales de cada iteración en segundos
- average_time: Tiempo promedio en segundos
