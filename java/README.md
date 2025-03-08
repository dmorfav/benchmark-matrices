# Benchmark de Multiplicación de Matrices en Java

Este proyecto implementa un benchmark para la multiplicación de matrices en Java, similar al benchmark implementado en Python.

## Características

- Implementación usando únicamente librerías nativas de Java (sin dependencias externas)
- Algoritmo naïve para la multiplicación de matrices
- Carga de matrices desde archivos JSON
- Medición de tiempos de ejecución
- Registro de resultados en formato CSV

## Requisitos

- Java JDK 11 o superior

## Compilación

### Opción 1: Usando el script de compilación (sin Maven)

Se proporciona un script para compilar el proyecto sin necesidad de Maven:

```bash
# Dar permisos de ejecución al script
chmod +x compile.sh

# Ejecutar el script
./compile.sh
```

Esto generará un archivo JAR ejecutable en la carpeta `target/`.

### Opción 2: Compilación manual

Si prefieres compilar manualmente:

```bash
# Crear directorio para los archivos compilados
mkdir -p target/classes

# Compilar el código fuente
javac -d target/classes src/benchmark/Main.java

# Crear un JAR ejecutable
cd target/classes
jar cvfe ../benchmark.jar benchmark.Main benchmark/*.class
cd ../..
```

### Opción 3: Usando Maven (si está disponible)

Si tienes Maven instalado:

```bash
mvn clean package
```

## Ejecución

Para ejecutar el benchmark con la configuración predeterminada (matrices de tamaño 500x500 y 10 iteraciones):

```bash
java -jar target/benchmark.jar
```

O si prefieres ejecutar directamente la clase:

```bash
java -cp target/classes benchmark.Main
```

Para especificar el tamaño de las matrices y el número de iteraciones:

```bash
java -jar target/benchmark.jar --n 1000 --iterations 5
```

O con la clase directamente:

```bash
java -cp target/classes benchmark.Main --n 1000 --iterations 5
```

## Parámetros

- `--n`: Dimensión de las matrices cuadradas (predeterminado: 500)
- `--iterations`: Número de iteraciones para medir el tiempo promedio (predeterminado: 10)

## Resultados

Los resultados se guardarán en el archivo `results/benchmark_java_results.csv` con el siguiente formato:

```
language,matrix_size,iterations,individual_times,average_time
Java,500,10,0.123456 0.123457 ...,0.123456
```

El archivo incluye el lenguaje, tamaño de la matriz, número de iteraciones, tiempos individuales de cada iteración y el tiempo promedio.

Benchmark de multiplicación de matrices en Java
Cargando matrices de dimensión 500 desde el dataset...
Ejecutando benchmark con 10 iteraciones...
Tiempos (segundos): [0.112016, 0.107376, 0.103522, 0.105495, 0.100741, 0.101784, 0.101396, 0.100746, 0.100676, 0.100635]
Tiempo promedio: 0.103439 segundos
Resultados registrados correctamente en 'results/benchmark_java_results.csv'.
