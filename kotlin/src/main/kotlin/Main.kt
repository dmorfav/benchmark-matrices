import java.io.File
import java.io.FileReader
import java.nio.file.Files
import java.nio.file.Paths
import kotlinx.serialization.json.*
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.encodeToString
import java.io.FileWriter
import kotlin.system.exitProcess
import kotlin.system.measureTimeMillis

/**
 * Implementación naïve de la multiplicación de matrices en Kotlin.
 * Carga las matrices desde archivos JSON, mide el tiempo de ejecución y registra los resultados.
 */

/**
 * Carga una matriz desde un archivo JSON.
 */
fun loadMatrix(filePath: String): List<List<Double>> {
    try {
        val jsonString = File(filePath).readText()
        return Json.decodeFromString<List<List<Double>>>(jsonString)
    } catch (e: Exception) {
        println("Error: El archivo '$filePath' no existe o no contiene JSON válido.")
        exitProcess(1)
    }
}

/**
 * Multiplica dos matrices cuadradas matrixA y matrixB utilizando el algoritmo naïve.
 *
 * @param matrixA Primera matriz de dimensión n x n.
 * @param matrixB Segunda matriz de dimensión n x n.
 * @return Matriz resultante C de la multiplicación.
 */
fun multiplyMatrices(matrixA: List<List<Double>>, matrixB: List<List<Double>>): List<List<Double>> {
    val n = matrixA.size
    // Inicializa la matriz resultado con ceros.
    val c = List(n) { MutableList(n) { 0.0 } }
    
    for (i in 0 until n) {
        for (j in 0 until n) {
            var s = 0.0
            for (k in 0 until n) {
                s += matrixA[i][k] * matrixB[k][j]
            }
            c[i][j] = s
        }
    }
    return c
}

/**
 * Realiza la multiplicación de matrices repetidamente y mide el tiempo promedio.
 *
 * @param matrixA Primera matriz.
 * @param matrixB Segunda matriz.
 * @param iterations Número de iteraciones a ejecutar.
 * @return Par (tiempo_promedio, lista_de_tiempos).
 */
fun measureMultiplication(matrixA: List<List<Double>>, matrixB: List<List<Double>>, iterations: Int): Pair<Double, List<Double>> {
    val times = mutableListOf<Double>()
    
    // Calcular el incremento del 20%
    val progressStep = maxOf(1, iterations / 5)
    println("Iniciando multiplicación de matrices ($iterations iteraciones)...")
    
    repeat(iterations) { i ->
        // Mostrar progreso cada 20% o si es la última iteración
        if (i % progressStep == 0 || i == iterations - 1) {
            val progressPercent = (i.toDouble() / iterations) * 100.0
            println("Progreso: Iteración ${i + 1}/$iterations (%.1f%%)".format(progressPercent))
        }
        
        val startTime = System.nanoTime()
        multiplyMatrices(matrixA, matrixB)
        val endTime = System.nanoTime()
        times.add((endTime - startTime) / 1_000_000_000.0) // Convertir nanosegundos a segundos
    }
    
    println("Multiplicación de matrices completada (100%).")
    
    val averageTime = times.average()
    return Pair(averageTime, times)
}

/**
 * Registra los resultados en un archivo CSV dentro de la carpeta 'results'.
 *
 * Se crea (o se actualiza) el archivo 'benchmark_kotlin_results.csv' con los siguientes campos:
 * language, matrix_size, iterations, individual_times, average_time.
 */
fun registrarResultados(matrixSize: Int, iterations: Int, times: List<Double>, averageTime: Double) {
    val currentDir = File("").absolutePath
    // Determinar la ruta del directorio results relativo al script
    val projectRootDir = File(currentDir).parentFile.absolutePath
    val resultsDir = File(projectRootDir, "results")
    resultsDir.mkdirs() // Crear el directorio si no existe
    
    val resultsFile = File(resultsDir, "benchmark_kotlin_results.csv")
    val fileExists = resultsFile.exists()
    
    FileWriter(resultsFile, true).use { writer ->
        if (!fileExists) {
            writer.write("language,matrix_size,iterations,individual_times,average_time\n")
        }
        
        val individualTimesStr = times.joinToString(" ") { "%.6f".format(it) }
        writer.write("Kotlin,$matrixSize,$iterations,$individualTimesStr,%.6f\n".format(averageTime))
    }
}

fun main(args: Array<String>) {
    println("Benchmark de multiplicación de matrices en Kotlin")
    
    // Procesar argumentos de línea de comandos
    var n = 500
    var iterations = 10
    
    for (i in args.indices) {
        when (args[i]) {
            "--n" -> if (i + 1 < args.size) n = args[i + 1].toIntOrNull() ?: 500
            "--iterations" -> if (i + 1 < args.size) iterations = args[i + 1].toIntOrNull() ?: 10
        }
    }
    
    // Construir rutas relativas para acceder a los datasets
    val currentDir = File("").absolutePath
    // Subir un nivel para acceder al directorio data en la raíz del proyecto
    val projectRootDir = File(currentDir).parentFile.absolutePath
    val dataDir = File(projectRootDir, "data")
    
    // Verificar si el directorio de datos existe
    if (!dataDir.exists()) {
        println("Error: El directorio de datos '${dataDir.absolutePath}' no existe.")
        exitProcess(1)
    }
    
    val matrixAFile = File(dataDir, "matrix_A_$n.json").absolutePath
    val matrixBFile = File(dataDir, "matrix_B_$n.json").absolutePath
    
    println("Cargando matrices de dimensión $n desde el dataset...")
    
    // La función loadMatrix ahora maneja internamente el caso cuando los archivos no existen
    val matrixA = loadMatrix(matrixAFile)
    val matrixB = loadMatrix(matrixBFile)
    
    println("Ejecutando benchmark con $iterations iteraciones...")
    val (averageTime, times) = measureMultiplication(matrixA, matrixB, iterations)
    
    println("Tiempos de cada iteración (en segundos):")
    times.forEach { println("%.6f".format(it)) }
    println("Tiempo promedio: %.6f segundos".format(averageTime))
    
    // Registrar resultados para su posterior comparación
    registrarResultados(n, iterations, times, averageTime)
    println("Resultados registrados correctamente en 'results/benchmark_kotlin_results.csv'.")
}
