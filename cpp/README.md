# Benchmark de Multiplicación de Matrices en C++

Este directorio contiene una implementación naïve del algoritmo de multiplicación de matrices en C++.

## Requisitos

- Compilador C++ compatible con C++11 o superior (GCC, Clang, MSVC, etc.)

## Compilación

Para compilar el programa, ejecuta el siguiente comando desde el directorio `cpp`:

### En Linux/macOS

```bash
g++ -std=c++11 -O3 main.cpp -o matrix_benchmark
```

### En Windows (con MinGW)

```bash
g++ -std=c++11 -O3 main.cpp -o matrix_benchmark.exe
```

### En Windows (con MSVC)

```bash
cl /EHsc /O2 main.cpp /Fe:matrix_benchmark.exe
```

## Ejecución

Para ejecutar el benchmark con los parámetros por defecto (matrices de 500x500, 10 iteraciones):

```bash
./matrix_benchmark
```

### Opciones

El programa acepta los siguientes argumentos opcionales:

- `--n <valor>`: Dimensión de las matrices cuadradas (default: 500)
- `--iterations <valor>`: Número de iteraciones para medir el tiempo promedio (default: 10)
- `--help`, `-h`: Muestra un mensaje de ayuda

Ejemplo:

```bash
./matrix_benchmark --n 1000 --iterations 5
```

## Resultados

Los resultados del benchmark se guardarán en el archivo `results/benchmark_cpp_results.csv` con el siguiente formato:

```
language,matrix_size,iterations,individual_times,average_time
C++,500,10,0.123456 0.123456 ...,0.123456
```

Este archivo puede ser utilizado para comparar el rendimiento con otras implementaciones.

## Implementación

El programa:

1. Carga dos matrices cuadradas desde archivos JSON en el directorio `data/`
2. Realiza la multiplicación de matrices utilizando el algoritmo naïve
3. Mide el tiempo de ejecución para cada iteración
4. Calcula el tiempo promedio
5. Registra los resultados en el archivo CSV

La implementación utiliza funciones y bibliotecas estándar de C++ para maximizar la compatibilidad.
