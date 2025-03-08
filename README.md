# Benchmark de Multiplicación de Matrices

## Resumen

Este proyecto realiza un benchmark de multiplicación de matrices "naive" (ingenua) utilizando diferentes lenguajes de programación. El objetivo es comparar el rendimiento en la ejecución de un mismo algoritmo implementado en C++, C#, Go, Java, Kotlin, Node.js, Python y Swift.

Se busca evidenciar las diferencias inherentes a cada lenguaje, ya sea por su naturaleza compilada o interpretada, la optimización de su runtime (o JVM en el caso de Java y Kotlin) y las características de desarrollo propias. Se utiliza un algoritmo clásico de complejidad O(n³) para resaltar cómo el lenguaje y el entorno de ejecución afectan la eficiencia computacional.

## Descripción del Algoritmo

### Fundamento Matemático

Dadas dos matrices cuadradas A y B de dimensión n × n, el producto de ambas se define matemáticamente como:

```
C[i][j] = ∑ₖ₌₀ⁿ⁻¹ A[i][k] × B[k][j]
```

Para 0 ≤ i, j < n.

### Proceso y Complejidad

El algoritmo implementado en todos los lenguajes sigue estos pasos:

1. **Entrada**: Dos matrices A y B generadas con valores numéricos aleatorios.
2. **Inicialización**: Crear una matriz C de n × n con valores inicializados a cero.
3. **Cálculo**: Mediante tres bucles anidados, calcular cada elemento C[i][j] acumulando el producto de los correspondientes elementos de A y B.
4. **Salida**: La matriz resultante C.

La implementación utiliza tres bucles, cada uno iterando n veces, lo que determina una complejidad temporal de O(n³). Este crecimiento cúbico en el número de operaciones hace que el problema sea ideal para evaluar el rendimiento bajo diferentes entornos y lenguajes.

## Estructura del Proyecto

```
benchmark-matrices/
├─ cpp/                      # Implementación en C++
│  ├─ main.cpp
│  └─ README.md
├─ csharp/                   # Implementación en C#
│  ├─ main.cs
│  ├─ MatrixBenchmark.csproj
│  └─ README.md
├─ data/                     # Matrices de prueba pre-generadas
│  ├─ matrix_A_100.json
│  ├─ matrix_A_1000.json
│  ├─ matrix_A_10000.json
│  ├─ matrix_A_250.json
│  ├─ matrix_A_500.json
│  ├─ matrix_A_5000.json
│  ├─ matrix_A_750.json
│  ├─ matrix_B_100.json
│  ├─ matrix_B_1000.json
│  ├─ matrix_B_10000.json
│  ├─ matrix_B_250.json
│  ├─ matrix_B_500.json
│  ├─ matrix_B_5000.json
│  └─ matrix_B_750.json
├─ dataset/                  # Script para generar nuevas matrices
│  └─ generar_dataset.py
├─ go/                       # Implementación en Go
│  ├─ go.mod
│  ├─ main.go
│  └─ README.md
├─ java/                     # Implementación en Java
│  ├─ src/
│  │  └─ Main.java
│  ├─ compile.sh
│  ├─ pom.xml
│  └─ README.md
├─ kotlin/                   # Implementación en Kotlin
│  ├─ src/
│  │  └─ Main.kt
│  ├─ build.gradle.kts
│  └─ README.md
├─ nodejs/                   # Implementación en Node.js
│  ├─ main.js
│  └─ README.md
├─ python/                   # Implementación en Python
│  ├─ main.py
│  └─ README.md
├─ results/                  # Directorio para almacenar resultados
│  ├─ benchmark_cpp_results.csv
│  ├─ benchmark_csharp_results.csv
│  ├─ benchmark_go_results.csv
│  ├─ benchmark_java_results.csv
│  ├─ benchmark_kotlin_results.csv
│  ├─ benchmark_nodejs_results.csv
│  ├─ benchmark_python_results.csv
│  └─ benchmark_swift_results.csv
├─ swift/                    # Implementación en Swift
│  ├─ main.swift
│  ├─ Package.swift
│  └─ README.md
├─ .gitignore
├─ LICENSE
└─ README.md
```

## Lenguajes Evaluados

Se seleccionaron los siguientes lenguajes, representativos de distintos paradigmas y modelos de ejecución:

- **Go**: Lenguaje compilado con fuerte soporte para concurrencia.
- **Python**: Lenguaje interpretado; en este benchmark se utiliza una implementación en puro Python (sin librerías como NumPy).
- **C++**: Lenguaje compilado de alto rendimiento, tradicional en cálculos intensivos.
- **C#**: Lenguaje compilado que se ejecuta sobre .NET runtime, ofreciendo un balance entre rendimiento y facilidad de desarrollo.
- **Node.js**: Ambiente de ejecución para JavaScript, cuyo carácter interpretado y orientado a eventos presenta un caso de estudio interesante.
- **Java**: Ejecutado sobre la JVM, aprovechando las ventajas del JIT (Just-In-Time Compilation).
- **Kotlin**: Lenguaje moderno que se ejecuta sobre la JVM, permitiendo explorar las ventajas del JIT y la comparabilidad con Java.
- **Swift**: Lenguaje compilado, con un enfoque moderno en el desarrollo, evaluado en su versión "pura" para computación intensiva.

## Metodología Experimental

### Generación de Datos de Prueba

- **Matrices de Prueba**: Se generan matrices de dimensiones n × n (500×500 y 1000×1000 por ejemplo) utilizando números aleatorios.
- **Reproducibilidad**: Se utiliza una semilla fija en el generador de números aleatorios para asegurar la reproducibilidad de los experimentos.

### Medición del Rendimiento

- **Temporización de Alta Precisión**: Cada lenguaje utiliza funciones de medición de tiempo de alta resolución nativas.
- **Repeticiones y Promedio**: Se realizan múltiples iteraciones (10 por defecto) y se calcula el promedio para mitigar variaciones debidas a condiciones del entorno.
- **Ambiente Controlado**: Se recomienda ejecutar los benchmarks en un entorno homogéneo (misma máquina, sin procesos intensivos concurrentes) para asegurar la comparabilidad de resultados.

## Requisitos Generales

Cada implementación requiere su propio entorno de desarrollo. A continuación se detallan los requisitos para cada lenguaje:

- **Python**: 3.6 o superior
- **Go**: 1.15 o superior
- **Java**: JDK 11 o superior
- **Kotlin**: JDK 21 o superior
- **Node.js**: 14.x o superior
- **Swift**: 5.3 o superior (macOS 10.15+)
- **C++**: Compilador compatible con C++11 o superior
- **C#**: .NET SDK 6.0 o superior

## Generación del Dataset

Para generar nuevas matrices de prueba, utilice el script `dataset/generar_dataset.py`:

```bash
cd dataset
python generar_dataset.py
```

Por defecto, este script genera matrices de 100x100, 250x250, 500x500, 750x750, 1000x1000, 5000x5000 y 10000x10000 con una semilla fija (42) para asegurar la reproducibilidad. Puede modificar el script para generar matrices de otros tamaños.

## Instalación y Ejecución

### Ejecutar Todos los Benchmarks a la Vez

El proyecto incluye un script que permite ejecutar todos los benchmarks en secuencia:

```bash
./run_benchmarks.sh
```

Este script acepta varias opciones:

- `-h, --help`: Muestra ayuda sobre el uso del script
- `-i, --iterations NUM`: Establece el número de iteraciones (por defecto: 10)
- `-s, --sizes SIZES`: Establece los tamaños de matriz separados por comas (por defecto: 100,250,500,750,1000)
- `-g, --generate`: Genera nuevas matrices antes de ejecutar los benchmarks
- `--no-cpp, --no-csharp, --no-go, etc.`: Permite omitir benchmarks específicos
- `--no-analysis`: Omite el análisis final de resultados

Ejemplo:
```bash
./run_benchmarks.sh -i 5 -s 100,500,1000 --no-swift --no-csharp
```

### Ejecutar Benchmarks Individuales

Alternativamente, cada implementación tiene sus propias instrucciones de instalación y ejecución. Todas aceptan parámetros similares:

- `--n`, `-n`: Dimensión de las matrices cuadradas (por defecto: 500)
- `--iterations`, `-i`: Número de iteraciones para medir el tiempo promedio (por defecto: 10)

### Python

```bash
cd python
python main.py --n 500 --iterations 10
```

### Go

```bash
cd go
go build -o matrix_benchmark
./matrix_benchmark -n 500 -iterations 10
```

### Java

```bash
cd java
./compile.sh
java -jar target/benchmark.jar --n 500 --iterations 10
```

### Kotlin

```bash
cd kotlin
./gradlew run --args="--n 500 --iterations 10"
```

### Node.js

```bash
cd nodejs
npm install
node main.js -n 500 -i 10
```

### Swift

```bash
cd swift
swift run -c release benchmark -- --n 500 --iterations 10
```

### C++

```bash
cd cpp
g++ -std=c++11 -O3 main.cpp -o matrix_benchmark
./matrix_benchmark --n 500 --iterations 10
```

### C#

```bash
cd csharp
dotnet build
dotnet run --n 500 --iterations 10
```

## Formato de Resultados

Los resultados de cada benchmark se guardan en archivos CSV individuales en el directorio `results/` con el siguiente formato:

```
language,matrix_size,iterations,individual_times,average_time
Python,500,10,0.123456 0.123457 ...,0.123456
```

Cada archivo contiene:
- `language`: El lenguaje utilizado
- `matrix_size`: Dimensión de las matrices (n)
- `iterations`: Número de iteraciones realizadas
- `individual_times`: Tiempos individuales de cada iteración (en segundos)
- `average_time`: Tiempo promedio de todas las iteraciones (en segundos)

## Análisis de Resultados

El proyecto incluye scripts para analizar y visualizar los resultados de los benchmarks. Después de ejecutar los benchmarks, puede generar un análisis automático:

```bash
cd analysis
./ejecutar_analisis.sh
```

El análisis genera:

- Tablas comparativas de rendimiento entre lenguajes
- Gráficos de barras para comparar tiempos de ejecución
- Análisis de escalabilidad (cómo crece el tiempo de ejecución con el tamaño de la matriz)
- Gráficos de desviación estándar para evaluar la consistencia de los benchmarks
- Información sobre tiempo mínimo, máximo y desviación estándar de cada lenguaje

Los resultados del análisis se guardan en el directorio `analysis/resultados_analisis/`.

## Comparación de Resultados

Para comparar los resultados entre diferentes lenguajes, puede:

1. Ejecutar todos los benchmarks con `./run_benchmarks.sh`
2. Revisar el análisis automático generado en `analysis/resultados_analisis/`
3. O utilizar los archivos CSV en el directorio `results/` para análisis personalizados

## Resultados Esperados

Aunque los resultados específicos dependerán de la implementación y el entorno de ejecución, se espera observar:

- **Lenguajes Compilados Nativos (C++, Go, Swift)**: Generalmente ofrecerán los tiempos de ejecución más rápidos debido a la optimización en tiempo de compilación y la generación de código nativo.
- **Lenguajes con Compilación JIT (Java, Kotlin, C#)**: Podrán alcanzar rendimientos competitivos gracias a la optimización JIT que ofrecen sus respectivos runtimes (.NET para C# y JVM para Java/Kotlin).
- **Lenguajes Interpretados (Python, Node.js)**: Se espera que tengan tiempos de ejecución significativamente mayores debido a la sobrecarga de la interpretación.

## Conclusiones

Este benchmark evidencia que la elección del lenguaje de programación impacta de forma significativa el rendimiento en problemas computacionales intensivos como la multiplicación de matrices naive.

La comparación directa entre estos lenguajes resalta la importancia de seleccionar el lenguaje adecuado según las necesidades del proyecto: mientras que la rapidez de ejecución es crucial en aplicaciones de alto rendimiento, otros factores como la facilidad de desarrollo y el ecosistema de herramientas pueden ser determinantes en proyectos de distinta índole.

## Contribución

Para contribuir al proyecto, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama para tu cambio.
3. Realiza tus cambios y haz commit.
4. Haz push a tu rama.
5. Crea un Pull Request.

## Futuras Líneas de Investigación

- **Optimización Algorítmica**: Comparar la implementación naive con versiones optimizadas (por ejemplo, bloqueada o utilizando técnicas de paralelización).
- **Análisis del Impacto de la Concurrencia**: Evaluar cómo la ejecución en múltiples hilos afecta el rendimiento en cada lenguaje.
- **Benchmarking en Diferentes Entornos**: Realizar pruebas en diversos sistemas operativos y arquitecturas de hardware.

## Licencia

Este proyecto está bajo la Licencia MIT.






