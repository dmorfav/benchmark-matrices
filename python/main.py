#!/usr/bin/env python3
"""
Implementación naïve de la multiplicación de matrices en Python.
Carga las matrices desde archivos JSON, mide el tiempo de ejecución y registra los resultados.
"""

import json
import time
import argparse
import os
import csv
from typing import List, Tuple

def load_matrix(file_path: str) -> List[List[float]]:
    """Carga una matriz desde un archivo JSON."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no existe.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: El archivo '{file_path}' no contiene JSON válido.")
        exit(1)

def multiply_matrices(matrix_a: List[List[float]], matrix_b: List[List[float]]) -> List[List[float]]:
    """
    Multiplica dos matrices cuadradas matrix_a y matrix_b utilizando el algoritmo naïve.
    
    Args:
        matrix_a: Primera matriz de dimensión n x n.
        matrix_b: Segunda matriz de dimensión n x n.
    
    Returns:
        Matriz resultante C de la multiplicación.
    """
    n = len(matrix_a)
    # Inicializa la matriz resultado con ceros.
    C = [[0.0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            s = 0.0
            for k in range(n):
                s += matrix_a[i][k] * matrix_b[k][j]
            C[i][j] = s
    return C

def measure_multiplication(matrix_a: List[List[float]], matrix_b: List[List[float]], iterations: int) -> Tuple[float, List[float]]:
    """
    Realiza la multiplicación de matrices repetidamente y mide el tiempo promedio.
    
    Args:
        matrix_a: Primera matriz.
        matrix_b: Segunda matriz.
        iterations: Número de iteraciones a ejecutar.
        
    Returns:
        Tupla (tiempo_promedio, lista_de_tiempos).
    """
    times = []
    
    # Calcular el incremento del 20%
    progress_step = max(1, iterations // 5)
    print(f"Iniciando multiplicación de matrices ({iterations} iteraciones)...")
    
    for i in range(iterations):
        # Mostrar progreso cada 20% o si es la última iteración
        if i % progress_step == 0 or i == iterations - 1:
            progress_percent = (i / iterations) * 100.0
            print(f"Progreso: Iteración {i + 1}/{iterations} ({progress_percent:.1f}%)")
        
        start_time = time.time()
        multiply_matrices(matrix_a, matrix_b)
        end_time = time.time()
        times.append(end_time - start_time)
    
    print("Multiplicación de matrices completada (100%).")
    
    average_time = sum(times) / len(times)
    return average_time, times

def registrar_resultados(matrix_size: int, iterations: int, times: List[float], average_time: float) -> None:
    """
    Registra los resultados en un archivo CSV dentro de la carpeta 'results'.
    
    Se crea (o se actualiza) el archivo 'benchmark_python_results.csv' con los siguientes campos:
    language, matrix_size, iterations, individual_times, average_time.
    """
    # Determinar la ruta del directorio results relativo al script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(current_dir, "..", "results")
    os.makedirs(results_dir, exist_ok=True)
    results_file = os.path.join(results_dir, "benchmark_python_results.csv")
    
    # Verifica si el archivo ya existe para incluir cabecera
    file_exists = os.path.isfile(results_file)
    
    with open(results_file, 'a', newline='') as csvfile:
        fieldnames = ["language", "matrix_size", "iterations", "individual_times", "average_time"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            "language": "Python",
            "matrix_size": matrix_size,
            "iterations": iterations,
            "individual_times": " ".join([f"{t:.6f}" for t in times]),
            "average_time": f"{average_time:.6f}"
        })

def main():
    parser = argparse.ArgumentParser(
        description="Benchmark naïve de multiplicación de matrices en Python"
    )
    parser.add_argument(
        "--n", type=int, default=500,
        help="Dimensión de las matrices cuadradas (default: 500)"
    )
    parser.add_argument(
        "--iterations", type=int, default=10,
        help="Número de iteraciones para medir el tiempo promedio (default: 10)"
    )
    args = parser.parse_args()

    # Construir rutas relativas para acceder a los datasets
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "..", "data")
    
    # Verificar si el directorio de datos existe
    if not os.path.exists(data_dir):
        print(f"Error: El directorio de datos '{data_dir}' no existe.")
        exit(1)
    
    matrix_a_file = os.path.join(data_dir, f"matrix_A_{args.n}.json")
    matrix_b_file = os.path.join(data_dir, f"matrix_B_{args.n}.json")
    
    print(f"Cargando matrices de dimensión {args.n} desde el dataset...")
    
    # La función load_matrix ahora maneja internamente el caso cuando los archivos no existen
    matrix_a = load_matrix(matrix_a_file)
    matrix_b = load_matrix(matrix_b_file)
    
    print(f"Ejecutando benchmark con {args.iterations} iteraciones...")
    average_time, times = measure_multiplication(matrix_a, matrix_b, args.iterations)
    
    print("Tiempos de cada iteración (en segundos):")
    for t in times:
        print(f"{t:.6f}")
    print(f"Tiempo promedio: {average_time:.6f} segundos")
    
    # Registrar resultados para su posterior comparación
    registrar_resultados(args.n, args.iterations, times, average_time)
    print("Resultados registrados correctamente en 'results/benchmark_python_results.csv'.")

if __name__ == "__main__":
    main()
