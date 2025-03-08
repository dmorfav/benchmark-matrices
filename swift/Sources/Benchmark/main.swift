print("Benchmark de multiplicación de matrices en Swift")

import Foundation

// MARK: - Estructuras de datos y funciones
typealias Matrix = [[Double]]

/// Función para cargar una matriz desde un archivo JSON
func loadMatrix(filePath: String) -> Matrix {
    let fileManager = FileManager.default
    
    guard fileManager.fileExists(atPath: filePath) else {
        print("Error: El archivo '\(filePath)' no existe.")
        exit(1)
    }
    
    do {
        let data = try Data(contentsOf: URL(fileURLWithPath: filePath))
        let matrix = try JSONDecoder().decode(Matrix.self, from: data)
        return matrix
    } catch {
        print("Error al cargar la matriz desde \(filePath): \(error)")
        exit(1)
    }
}

/// Función para multiplicar dos matrices cuadradas
func multiplyMatrices(matrixA: Matrix, matrixB: Matrix) -> Matrix {
    let n = matrixA.count
    // Inicializar matriz resultado con ceros
    var result = Array(repeating: Array(repeating: 0.0, count: n), count: n)
    
    for i in 0..<n {
        for j in 0..<n {
            var sum = 0.0
            for k in 0..<n {
                sum += matrixA[i][k] * matrixB[k][j]
            }
            result[i][j] = sum
        }
    }
    
    return result
}

/// Función para medir el tiempo de ejecución de la multiplicación de matrices
func measureMultiplication(matrixA: Matrix, matrixB: Matrix, iterations: Int) -> (averageTime: Double, times: [Double]) {
    var times = [Double]()
    
    for _ in 0..<iterations {
        let startTime = Date()
        _ = multiplyMatrices(matrixA: matrixA, matrixB: matrixB)
        let endTime = Date()
        let timeInterval = endTime.timeIntervalSince(startTime)
        times.append(timeInterval)
    }
    
    let averageTime = times.reduce(0, +) / Double(times.count)
    return (averageTime, times)
}

/// Función para registrar los resultados en un archivo CSV
func registerResults(matrixSize: Int, iterations: Int, times: [Double], averageTime: Double) {
    // Determinar la ruta del directorio results
    let currentDirectory = FileManager.default.currentDirectoryPath
    let resultsDirectory = "\(currentDirectory)/../results"
    let resultsFile = "\(resultsDirectory)/benchmark_swift_results.csv"
    
    // Crear el directorio si no existe
    do {
        try FileManager.default.createDirectory(atPath: resultsDirectory, withIntermediateDirectories: true)
    } catch {
        print("Error al crear el directorio de resultados: \(error)")
        return
    }
    
    // Comprobar si el archivo existe
    let fileExists = FileManager.default.fileExists(atPath: resultsFile)
    
    // Preparar los datos para el CSV
    let header = "language,matrix_size,iterations,individual_times,average_time\n"
    let individualTimesString = times.map { String(format: "%.6f", $0) }.joined(separator: " ")
    let row = "Swift,\(matrixSize),\(iterations),\"\(individualTimesString)\",\(String(format: "%.6f", averageTime))\n"
    
    do {
        if fileExists {
            // Agregar una nueva fila al archivo existente
            let fileHandle = try FileHandle(forWritingTo: URL(fileURLWithPath: resultsFile))
            fileHandle.seekToEndOfFile()
            if let data = row.data(using: .utf8) {
                fileHandle.write(data)
            }
            fileHandle.closeFile()
        } else {
            // Crear un nuevo archivo con encabezado y datos
            let content = header + row
            try content.write(toFile: resultsFile, atomically: true, encoding: .utf8)
        }
    } catch {
        print("Error al escribir en el archivo de resultados: \(error)")
    }
}

// MARK: - Función principal
func main() {
    // Parseo de argumentos
    var n = 500
    var iterations = 10
    
    if CommandLine.arguments.count > 1 {
        for i in 1..<CommandLine.arguments.count {
            let arg = CommandLine.arguments[i]
            if arg == "--n", i + 1 < CommandLine.arguments.count, let value = Int(CommandLine.arguments[i + 1]) {
                n = value
            } else if arg == "--iterations", i + 1 < CommandLine.arguments.count, let value = Int(CommandLine.arguments[i + 1]) {
                iterations = value
            }
        }
    }
    
    // Construir rutas relativas para acceder a los datasets
    let currentDirectory = FileManager.default.currentDirectoryPath
    let dataDirectory = "\(currentDirectory)/../data"
    
    // Verificar si el directorio de datos existe
    guard FileManager.default.fileExists(atPath: dataDirectory) else {
        print("Error: El directorio de datos '\(dataDirectory)' no existe.")
        exit(1)
    }
    
    let matrixAFile = "\(dataDirectory)/matrix_A_\(n).json"
    let matrixBFile = "\(dataDirectory)/matrix_B_\(n).json"
    
    print("Cargando matrices de dimensión \(n) desde el dataset...")
    
    let matrixA = loadMatrix(filePath: matrixAFile)
    let matrixB = loadMatrix(filePath: matrixBFile)
    
    print("Ejecutando benchmark con \(iterations) iteraciones...")
    let (averageTime, times) = measureMultiplication(matrixA: matrixA, matrixB: matrixB, iterations: iterations)
    
    print("Tiempos de cada iteración (en segundos):")
    for t in times {
        print(String(format: "%.6f", t))
    }
    print("Tiempo promedio: \(String(format: "%.6f", averageTime)) segundos")
    
    // Registrar resultados para su posterior comparación
    registerResults(matrixSize: n, iterations: iterations, times: times, averageTime: averageTime)
    print("Resultados registrados correctamente en 'results/benchmark_swift_results.csv'.")
}

// MARK: - Ejecución
main()
