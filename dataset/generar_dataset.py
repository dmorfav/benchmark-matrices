import json
import random
import os
from typing import List

def generar_matriz(n: int, seed: int) -> List[List[float]]:
    """Genera una matriz n x n con números flotantes aleatorios."""
    random.seed(seed)
    return [[random.uniform(0, 100) for _ in range(n)] for _ in range(n)]

def guardar_matriz(matriz: List[List[float]], nombre_archivo: str) -> None:
    """Guarda la matriz en un archivo JSON."""
    # Crear el directorio si no existe
    directorio = os.path.dirname(nombre_archivo)
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio)
        
    with open(nombre_archivo, 'w') as archivo:
        json.dump(matriz, archivo)

def generar_dataset(n_valores: List[int], semilla: int = 42) -> None:
    """
    Genera y guarda conjuntos de matrices A y B para cada dimensión especificada en n_valores.
    
    Args:
        n_valores: Lista de tamaños (n) para las matrices.
        semilla: Semilla base para la generación de números aleatorios.
    """
    for n in n_valores:
        matriz_A = generar_matriz(n, semilla)
        # Usamos una semilla diferente para B para asegurar diversidad
        matriz_B = generar_matriz(n, semilla + 1)
        
        archivo_A = f"../data/matrix_A_{n}.json"
        archivo_B = f"../data/matrix_B_{n}.json"
        
        guardar_matriz(matriz_A, archivo_A)
        guardar_matriz(matriz_B, archivo_B)
        
        print(f"Dataset generado para n={n}: {archivo_A} y {archivo_B}")

if __name__ == "__main__":
    # Ejemplo: generar datasets para matrices 100x100, 250x250, 500x500, 750x750, 1000x1000, 5000x5000 y 10000x10000
    dimensiones = [100, 250, 500, 750, 1000, 5000, 10000]
    generar_dataset(dimensiones)
