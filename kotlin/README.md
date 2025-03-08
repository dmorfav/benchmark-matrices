# Benchmark de Multiplicación de Matrices en Kotlin

Esta es la implementación en Kotlin del benchmark de multiplicación de matrices.

## Requisitos

- JDK 21 o superior
- No se requiere instalación de Gradle (se utiliza Gradle Wrapper)

## Estructura del Proyecto

```
kotlin/
├── build.gradle.kts            # Configuración de Gradle
├── gradle/                     # Archivos del Gradle Wrapper
├── gradlew                     # Script de Gradle Wrapper para Unix/macOS
├── gradlew.bat                 # Script de Gradle Wrapper para Windows
├── README.md                   # Este archivo
└── src/
    └── main/
        └── kotlin/
            └── Main.kt         # Código fuente principal
```

## Configuración del Proyecto

El proyecto utiliza Gradle Wrapper, lo que significa que no necesitas tener Gradle instalado en tu sistema. Los scripts `gradlew` (para Unix/macOS) y `gradlew.bat` (para Windows) se encargarán de descargar la versión correcta de Gradle automáticamente.

## Compilación

Para compilar el proyecto, ejecuta:

```bash
# En Unix/macOS
./gradlew clean build

# En Windows
gradlew.bat clean build
```

## Ejecución

Para ejecutar el benchmark con valores predeterminados (matriz 500x500, 10 iteraciones):

```bash
# En Unix/macOS
./gradlew run

# En Windows
gradlew.bat run
```

Para especificar el tamaño de la matriz y el número de iteraciones:

```bash
# En Unix/macOS
./gradlew run --args="--n 1000 --iterations 5"

# En Windows
gradlew.bat run --args="--n 1000 --iterations 5"
```

## Resultados

Los resultados se guardarán en el archivo `results/benchmark_kotlin_results.csv`, que contiene los siguientes campos:
- `language`: Kotlin
- `matrix_size`: Tamaño de la matriz
- `iterations`: Número de iteraciones
- `individual_times`: Tiempos individuales de cada iteración en segundos
- `average_time`: Tiempo promedio en segundos

## Implementación

La implementación utiliza:
- Kotlin 1.9.22
- kotlinx.serialization 1.6.2 para la lectura de matrices desde archivos JSON
- JDK 21
- Algoritmo naïve (O(n³)) para la multiplicación de matrices

## Notas Adicionales

El programa espera encontrar los archivos de matrices en el directorio `data` ubicado en la raíz del proyecto principal. Los archivos deben tener el formato `matrix_A_{n}.json` y `matrix_B_{n}.json`, donde `{n}` es el tamaño de la matriz.

Para generar estos archivos, puedes utilizar el script Python incluido en el directorio `dataset` del proyecto principal.
