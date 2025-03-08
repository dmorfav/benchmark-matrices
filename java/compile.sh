#!/bin/bash
# Script para compilar y ejecutar el benchmark de matrices en Java sin necesidad de Maven

echo "Compilando el proyecto Java..."

# Crear directorio de salida si no existe
mkdir -p target/classes

# Compilar el código fuente
javac -d target/classes src/Main.java

if [ $? -eq 0 ]; then
    echo "Compilación exitosa"
    
    # Crear un JAR ejecutable
    cd target/classes
    jar cvfe ../benchmark.jar Main *.class
    cd ../..
    
    echo ""
    echo "Ejecutable JAR creado en target/benchmark.jar"
    echo ""
    echo "Para ejecutar el benchmark, usa:"
    echo "java -jar target/benchmark.jar"
    echo ""
    echo "Para especificar parámetros:"
    echo "java -jar target/benchmark.jar --n 500 --iterations 10"
else
    echo "Error en la compilación"
fi 