#!/bin/bash

# Script para ejecutar todos los benchmarks de multiplicación de matrices
# y posteriormente analizar los resultados

# Colores para la salida
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Directorio raíz del proyecto
PROJECT_ROOT=$(pwd)

# Parámetros por defecto
ITERATIONS=10
MATRIX_SIZES=(100 250 500 750 1000)

# Función para mostrar ayuda
show_help() {
    echo "Uso: $0 [opciones]"
    echo "Opciones:"
    echo "  -h, --help             Muestra esta ayuda"
    echo "  -i, --iterations NUM   Establece el número de iteraciones (por defecto: 10)"
    echo "  -s, --sizes SIZES      Establece los tamaños de matriz separados por comas (por defecto: 100,250,500,750,1000)"
    echo "  -g, --generate         Genera nuevas matrices antes de ejecutar los benchmarks"
    echo "  --no-cpp               Omite el benchmark de C++"
    echo "  --no-csharp            Omite el benchmark de C#"
    echo "  --no-go                Omite el benchmark de Go"
    echo "  --no-java              Omite el benchmark de Java"
    echo "  --no-kotlin            Omite el benchmark de Kotlin"
    echo "  --no-nodejs            Omite el benchmark de Node.js"
    echo "  --no-python            Omite el benchmark de Python"
    echo "  --no-swift             Omite el benchmark de Swift"
    echo "  --no-analysis          Omite el análisis final de resultados"
}

# Parseo de argumentos
GENERATE_DATASETS=false
RUN_CPP=true
RUN_CSHARP=true
RUN_GO=true
RUN_JAVA=true
RUN_KOTLIN=true
RUN_NODEJS=true
RUN_PYTHON=true
RUN_SWIFT=true
RUN_ANALYSIS=true

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -i|--iterations)
            ITERATIONS="$2"
            shift 2
            ;;
        -s|--sizes)
            IFS=',' read -ra MATRIX_SIZES <<< "$2"
            shift 2
            ;;
        -g|--generate)
            GENERATE_DATASETS=true
            shift
            ;;
        --no-cpp)
            RUN_CPP=false
            shift
            ;;
        --no-csharp)
            RUN_CSHARP=false
            shift
            ;;
        --no-go)
            RUN_GO=false
            shift
            ;;
        --no-java)
            RUN_JAVA=false
            shift
            ;;
        --no-kotlin)
            RUN_KOTLIN=false
            shift
            ;;
        --no-nodejs)
            RUN_NODEJS=false
            shift
            ;;
        --no-python)
            RUN_PYTHON=false
            shift
            ;;
        --no-swift)
            RUN_SWIFT=false
            shift
            ;;
        --no-analysis)
            RUN_ANALYSIS=false
            shift
            ;;
        *)
            echo "Opción desconocida: $1"
            show_help
            exit 1
            ;;
    esac
done

# Función para verificar si un directorio existe (solo muestra advertencia)
verify_dir() {
    if [ ! -d "$1" ]; then
        echo -e "${YELLOW}Advertencia: El directorio '$1' no existe.${NC}"
        return 1
    fi
    return 0
}

# Función para verificar si un comando está disponible
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Generar datasets si se solicita
if [ "$GENERATE_DATASETS" = true ]; then
    echo -e "${BLUE}=== Generando datasets ===${NC}"
    if verify_dir "${PROJECT_ROOT}/dataset"; then
        cd "${PROJECT_ROOT}/dataset"
        python generar_dataset.py
        if [ $? -ne 0 ]; then
            echo -e "${RED}Error al generar datasets.${NC}"
            # No detenemos la ejecución, continuamos con los datasets existentes
        fi
        cd "${PROJECT_ROOT}"
    else
        echo -e "${YELLOW}No se pudieron generar nuevos datasets. Continuando con datasets existentes.${NC}"
    fi
fi

# Verificar que exista el directorio de resultados o crearlo
if [ ! -d "${PROJECT_ROOT}/results" ]; then
    mkdir -p "${PROJECT_ROOT}/results"
    echo -e "${BLUE}Directorio de resultados creado.${NC}"
fi

# Función para ejecutar un benchmark
run_benchmark() {
    local language=$1
    local command=$2
    local size=$3
    
    echo -e "${YELLOW}Ejecutando benchmark de $language (tamaño=$size, iteraciones=$ITERATIONS)...${NC}"
    eval "$command"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Benchmark de $language completado con éxito para tamaño $size.${NC}"
    else
        echo -e "${RED}Error al ejecutar el benchmark de $language para tamaño $size.${NC}"
    fi
    echo ""
}

# Ejecutar benchmarks para cada tamaño de matriz
for size in "${MATRIX_SIZES[@]}"; do
    echo -e "${BLUE}=== Ejecutando benchmarks para matrices de tamaño ${size}x${size} ===${NC}"
    
    # C++
    if [ "$RUN_CPP" = true ]; then
        if verify_dir "${PROJECT_ROOT}/cpp"; then
            cd "${PROJECT_ROOT}/cpp"
            if [ ! -f "matrix_benchmark" ]; then
                echo -e "${BLUE}Compilando benchmark de C++...${NC}"
                g++ -std=c++11 -O3 main.cpp -o matrix_benchmark
            fi
            if [ -f "matrix_benchmark" ]; then
                run_benchmark "C++" "./matrix_benchmark --n $size --iterations $ITERATIONS" "$size"
            else
                echo -e "${RED}No se pudo compilar el benchmark de C++.${NC}"
            fi
            cd "${PROJECT_ROOT}"
        fi
    fi
    
    # C#
    if [ "$RUN_CSHARP" = true ]; then
        if verify_dir "${PROJECT_ROOT}/csharp"; then
            cd "${PROJECT_ROOT}/csharp"
            run_benchmark "C#" "dotnet run --n $size --iterations $ITERATIONS" "$size"
            cd "${PROJECT_ROOT}"
        fi
    fi
    
    # Go
    if [ "$RUN_GO" = true ]; then
        if verify_dir "${PROJECT_ROOT}/go"; then
            cd "${PROJECT_ROOT}/go"
            if [ ! -f "matrix_benchmark" ]; then
                echo -e "${BLUE}Compilando benchmark de Go...${NC}"
                go build -o matrix_benchmark
            fi
            if [ -f "matrix_benchmark" ]; then
                run_benchmark "Go" "./matrix_benchmark -n $size -iterations $ITERATIONS" "$size"
            else
                echo -e "${RED}No se pudo compilar el benchmark de Go.${NC}"
            fi
            cd "${PROJECT_ROOT}"
        fi
    fi
    
    # Java
    if [ "$RUN_JAVA" = true ]; then
        if verify_dir "${PROJECT_ROOT}/java"; then
            cd "${PROJECT_ROOT}/java"
            if [ ! -f "target/benchmark.jar" ]; then
                echo -e "${BLUE}Compilando benchmark de Java...${NC}"
                ./compile.sh
            fi
            if [ -f "target/benchmark.jar" ]; then
                run_benchmark "Java" "java -jar target/benchmark.jar --n $size --iterations $ITERATIONS" "$size"
            else
                echo -e "${RED}No se pudo compilar el benchmark de Java.${NC}"
            fi
            cd "${PROJECT_ROOT}"
        fi
    fi
    
    # Kotlin
    if [ "$RUN_KOTLIN" = true ]; then
        if verify_dir "${PROJECT_ROOT}/kotlin"; then
            cd "${PROJECT_ROOT}/kotlin"
            
            # Verificar si existe gradlew o gradle
            KOTLIN_CMD=""
            if [ -f "./gradlew" ] && [ -x "./gradlew" ]; then
                KOTLIN_CMD="./gradlew run --args=\"--n $size --iterations $ITERATIONS\""
            elif command_exists gradle; then
                echo -e "${YELLOW}Usando el comando 'gradle' del sistema en lugar de './gradlew'${NC}"
                KOTLIN_CMD="gradle run --args=\"--n $size --iterations $ITERATIONS\""
            elif [ -f "./gradlew" ] && [ ! -x "./gradlew" ]; then
                echo -e "${YELLOW}El archivo './gradlew' existe pero no tiene permisos de ejecución. Añadiendo permisos...${NC}"
                chmod +x ./gradlew
                KOTLIN_CMD="./gradlew run --args=\"--n $size --iterations $ITERATIONS\""
            else
                echo -e "${RED}No se encontró ni './gradlew' ni 'gradle'. Intentando generar el wrapper...${NC}"
                if command_exists gradle; then
                    echo -e "${YELLOW}Generando Gradle Wrapper...${NC}"
                    gradle wrapper
                    if [ -f "./gradlew" ]; then
                        KOTLIN_CMD="./gradlew run --args=\"--n $size --iterations $ITERATIONS\""
                    else
                        echo -e "${RED}No se pudo generar el Gradle Wrapper.${NC}"
                    fi
                else
                    echo -e "${RED}No se puede ejecutar el benchmark de Kotlin porque no se encontró Gradle.${NC}"
                fi
            fi
            
            if [ -n "$KOTLIN_CMD" ]; then
                run_benchmark "Kotlin" "$KOTLIN_CMD" "$size"
            else
                echo -e "${RED}No se pudo ejecutar el benchmark de Kotlin.${NC}"
            fi
            
            cd "${PROJECT_ROOT}"
        fi
    fi
    
    # Node.js
    if [ "$RUN_NODEJS" = true ]; then
        if verify_dir "${PROJECT_ROOT}/nodejs"; then
            cd "${PROJECT_ROOT}/nodejs"
            run_benchmark "Node.js" "node main.js -n $size -i $ITERATIONS" "$size"
            cd "${PROJECT_ROOT}"
        fi
    fi
    
    # Python
    if [ "$RUN_PYTHON" = true ]; then
        if verify_dir "${PROJECT_ROOT}/python"; then
            cd "${PROJECT_ROOT}/python"
            run_benchmark "Python" "python main.py --n $size --iterations $ITERATIONS" "$size"
            cd "${PROJECT_ROOT}"
        fi
    fi
    
    # Swift
    if [ "$RUN_SWIFT" = true ]; then
        if verify_dir "${PROJECT_ROOT}/swift"; then
            cd "${PROJECT_ROOT}/swift"
            run_benchmark "Swift" "swift run -c release benchmark -- --n $size --iterations $ITERATIONS" "$size"
            cd "${PROJECT_ROOT}"
        fi
    fi
done

# Ejecutar análisis
if [ "$RUN_ANALYSIS" = true ]; then
    echo -e "${BLUE}=== Ejecutando análisis de resultados ===${NC}"
    if verify_dir "${PROJECT_ROOT}/analysis"; then
        cd "${PROJECT_ROOT}/analysis"
        ./ejecutar_analisis.sh
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}Análisis completado con éxito.${NC}"
        else
            echo -e "${RED}Error al ejecutar el análisis.${NC}"
        fi
    fi
fi

echo -e "${GREEN}¡Todos los benchmarks han sido ejecutados!${NC}" 