# Benchmark de Multiplicación de Matrices

## Descripción

Este proyecto realiza un benchmark de la multiplicación de matrices utilizando diferentes lenguajes de programación. Incluye implementaciones en C++, Go, Java, Kotlin y Python.

## Estructura del Proyecto

```
benchmark-matrices/
├─ cpp/
│  ├─ main.cpp
│  └─ README.md
├─ data/
│  ├─ matrix_A_1000.json
│  ├─ matrix_A_500.json
│  ├─ matrix_B_1000.json
│  └─ matrix_B_500.json
├─ dataset/
│  └─ generar_dataset.py
├─ go/
│  ├─ go.mod
│  ├─ main.go
│  ├─ matrix_benchmark
│  └─ README.md
├─ java/
│  ├─ src/
│  │  └─ Main.java
│  ├─ compile.sh
│  ├─ pom.xml
│  └─ README.md
├─ kotlin/
│  ├─ src/
│  │  └─ Main.kt
│  ├─ build.gradle.kts
│  └─ README.md
├─ nodejs/
│  ├─ main.js
│  └─ README.md
├─ python/
│  ├─ main.py
│  └─ README.md
├─ results/
│  ├─ benchmark_go_results.csv
│  └─ benchmark_python_results.csv
├─ swift/
│  ├─ main.swift
│  ├─ Package.swift
│  └─ README.md
├─ .gitignore
├─ LICENSE
└─ README.md
```

## Requisitos

- Python 3.x
- Go 1.x
- Java 11+
- Kotlin 1.5+
- Node.js 14+
- Swift 5+

## Instalación

### Python

```bash
pip install -r requirements.txt
```

### Go

```bash
go mod tidy
```

### Java

```bash
mvn clean install
```

### Kotlin

```bash
./gradlew build
```

### Node.js

```bash
npm install
```

### Swift

```bash
swift build
```

## Ejecución

### Python

```bash
python main.py
```

### Go

```bash
go run main.go
```

### Java

```bash
java -jar target/benchmark.jar
```

### Kotlin

```bash
./gradlew run
```

### Node.js

```bash
node main.js
```

### Swift

```bash
swift run
```

## Resultados

Los resultados se guardan en el archivo `results/benchmark_results.csv`.

## Contribución

Para contribuir al proyecto, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama para tu cambio.
3. Realiza tus cambios y haz commit.
4. Haz push a tu rama.
5. Crea un Pull Request.

## Licencia

Este proyecto está bajo la Licencia MIT.






