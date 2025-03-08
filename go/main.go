package main

import (
	"encoding/csv"
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"
)

// Carga una matriz desde un archivo JSON
func loadMatrix(filePath string) ([][]float64, error) {
	file, err := os.Open(filePath)
	if err != nil {
		if os.IsNotExist(err) {
			return nil, fmt.Errorf("el archivo '%s' no existe", filePath)
		}
		return nil, fmt.Errorf("error al abrir el archivo '%s': %v", filePath, err)
	}
	defer file.Close()

	var matrix [][]float64
	decoder := json.NewDecoder(file)
	if err := decoder.Decode(&matrix); err != nil {
		return nil, fmt.Errorf("el archivo '%s' no contiene JSON válido: %v", filePath, err)
	}
	return matrix, nil
}

// Multiplica dos matrices cuadradas A y B utilizando el algoritmo naïve
func multiplyMatrices(A, B [][]float64) [][]float64 {
	n := len(A)
	// Inicializa la matriz resultado con ceros
	C := make([][]float64, n)
	for i := range C {
		C[i] = make([]float64, n)
	}

	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			s := 0.0
			for k := 0; k < n; k++ {
				s += A[i][k] * B[k][j]
			}
			C[i][j] = s
		}
	}
	return C
}

// Mide el tiempo de ejecución de la multiplicación de matrices en varias iteraciones
func measureMultiplication(A, B [][]float64, iterations int) (float64, []float64) {
	times := make([]float64, iterations)
	var totalTime float64

	for i := 0; i < iterations; i++ {
		start := time.Now()
		_ = multiplyMatrices(A, B)
		elapsed := time.Since(start).Seconds()
		times[i] = elapsed
		totalTime += elapsed
	}

	averageTime := totalTime / float64(iterations)
	return averageTime, times
}

// Registra los resultados en un archivo CSV dentro de la carpeta 'results'
func registrarResultados(matrixSize, iterations int, times []float64, averageTime float64) error {
	// Determinar la ruta del directorio results relativo al script
	currentDir, err := os.Getwd()
	if err != nil {
		return err
	}

	resultsDir := filepath.Join(currentDir, "..", "results")

	// Asegurarse de que el directorio results exista
	if err := os.MkdirAll(resultsDir, 0755); err != nil {
		return err
	}

	resultsFile := filepath.Join(resultsDir, "benchmark_go_results.csv")

	// Verifica si el archivo ya existe para incluir cabecera
	fileExists := false
	if _, err := os.Stat(resultsFile); err == nil {
		fileExists = true
	}

	file, err := os.OpenFile(resultsFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return err
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	if !fileExists {
		if err := writer.Write([]string{"language", "matrix_size", "iterations", "individual_times", "average_time"}); err != nil {
			return err
		}
	}

	// Formatear tiempos individuales
	individualTimesStr := make([]string, len(times))
	for i, t := range times {
		individualTimesStr[i] = fmt.Sprintf("%.6f", t)
	}

	if err := writer.Write([]string{
		"Go",
		fmt.Sprintf("%d", matrixSize),
		fmt.Sprintf("%d", iterations),
		strings.Join(individualTimesStr, " "),
		fmt.Sprintf("%.6f", averageTime),
	}); err != nil {
		return err
	}

	return nil
}

func main() {
	// Parseo de argumentos de la línea de comandos
	nFlag := flag.Int("n", 500, "Dimensión de las matrices cuadradas (default: 500)")
	iterationsFlag := flag.Int("iterations", 10, "Número de iteraciones para medir el tiempo promedio (default: 10)")
	flag.Parse()

	n := *nFlag
	iterations := *iterationsFlag

	// Construir rutas relativas para acceder a los datasets
	currentDir, err := os.Getwd()
	if err != nil {
		fmt.Printf("Error al obtener el directorio actual: %v\n", err)
		os.Exit(1)
	}

	dataDir := filepath.Join(currentDir, "..", "data")

	// Verificar si el directorio de datos existe
	if _, err := os.Stat(dataDir); os.IsNotExist(err) {
		fmt.Printf("Error: El directorio de datos '%s' no existe.\n", dataDir)
		os.Exit(1)
	}

	matrixAFile := filepath.Join(dataDir, fmt.Sprintf("matrix_A_%d.json", n))
	matrixBFile := filepath.Join(dataDir, fmt.Sprintf("matrix_B_%d.json", n))

	fmt.Printf("Cargando matrices de dimensión %d desde el dataset...\n", n)
	A, err := loadMatrix(matrixAFile)
	if err != nil {
		fmt.Printf("Error al cargar la matriz A: %v\n", err)
		os.Exit(1)
	}

	B, err := loadMatrix(matrixBFile)
	if err != nil {
		fmt.Printf("Error al cargar la matriz B: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("Ejecutando benchmark con %d iteraciones...\n", iterations)
	averageTime, times := measureMultiplication(A, B, iterations)

	fmt.Println("Tiempos de cada iteración (en segundos):")
	for _, t := range times {
		fmt.Printf("%.6f\n", t)
	}
	fmt.Printf("Tiempo promedio: %.6f segundos\n", averageTime)

	// Registrar resultados para su posterior comparación
	if err := registrarResultados(n, iterations, times, averageTime); err != nil {
		fmt.Printf("Error al registrar resultados: %v\n", err)
		os.Exit(1)
	}

	fmt.Println("Resultados registrados correctamente en 'results/benchmark_go_results.csv'.")
}
