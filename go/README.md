# Benchmark de Multiplicación de Matrices en Go

Este directorio contiene una implementación naïve del algoritmo de multiplicación de matrices en Go.

## Requisitos

- Go 1.15 o superior

## Compilación

Para compilar el programa, ejecuta los siguientes comandos desde el directorio `go/`:

```bash
# Compilar el programa
go build -o matrix_benchmark
```

Esto generará un ejecutable llamado `matrix_benchmark`.

## Ejecución

Para ejecutar el benchmark, usa el siguiente comando:

```bash
./matrix_benchmark
```

Por defecto, el programa utiliza matrices de 500x500 y realiza 10 iteraciones.

### Opciones

Puedes personalizar la ejecución mediante las siguientes opciones:

- `-n`: Tamaño de las matrices cuadradas (por defecto: 500)
- `-iterations`: Número de iteraciones para medir el tiempo promedio (por defecto: 10)

Ejemplo:

```bash
./matrix_benchmark -n 1000 -iterations 5
```

## Resultados

Los resultados se guardan en el archivo `results/benchmark_go_results.csv`, incluyendo:

- Lenguaje: Go
- Tamaño de matriz
- Número de iteraciones
- Tiempos individuales
- Tiempo promedio
