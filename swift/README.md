# Benchmark de Multiplicación de Matrices en Swift

Este proyecto contiene una implementación en Swift para el benchmark de multiplicación de matrices.

## Requisitos

- Swift 5.3 o superior
- macOS 10.15 o superior

## Estructura del Proyecto

- `Sources/Benchmark/main.swift`: Contiene la implementación del benchmark
- `Package.swift`: Configuración del paquete Swift

## Ejecución del Benchmark

Para obtener el mejor rendimiento, se recomienda ejecutar el benchmark en modo release:

```bash
swift run -c release benchmark
```

### Parámetros disponibles

El benchmark acepta los siguientes parámetros opcionales:

- `--n`: Tamaño de la matriz (valor predeterminado: 500)
- `--iterations`: Número de iteraciones para el benchmark (valor predeterminado: 10)

### Ejemplos

Ejecutar con matrices de 1000x1000 y 5 iteraciones:
```bash
swift run -c release benchmark -- --n 1000 --iterations 5
```

Ejecutar con valores predeterminados:
```bash
swift run -c release benchmark
```

## Resultados

Los resultados del benchmark se guardan en el archivo `../results/benchmark_swift_results.csv`. Este archivo contiene:

- El tamaño de la matriz
- El número de iteraciones
- Los tiempos individuales de cada iteración
- El tiempo promedio de todas las iteraciones

## Nota sobre el rendimiento

El modo release (`-c release`) aplica todas las optimizaciones del compilador y es **significativamente más rápido** que el modo debug. Para obtener mediciones precisas del rendimiento, siempre use el modo release.
