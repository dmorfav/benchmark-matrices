using System;
using System.IO;
using System.Text.Json;
using System.Diagnostics;
using System.Collections.Generic;
using System.Linq;
using System.Globalization;

namespace MatrixBenchmark
{
    class Program
    {
        /// <summary>
        /// Carga una matriz desde un archivo JSON.
        /// </summary>
        /// <exception cref="FileNotFoundException">Se lanza cuando el archivo no existe.</exception>
        /// <exception cref="JsonException">Se lanza cuando el archivo no contiene JSON válido.</exception>
        static List<List<double>> LoadMatrix(string filePath)
        {
            try
            {
                string jsonString = File.ReadAllText(filePath);
                var matrix = JsonSerializer.Deserialize<List<List<double>>>(jsonString);
                if (matrix == null)
                {
                    throw new JsonException($"Error al deserializar el archivo '{filePath}': el resultado es nulo");
                }
                return matrix;
            }
            catch (FileNotFoundException ex)
            {
                Console.WriteLine($"Error: El archivo '{filePath}' no existe. Detalles: {ex.Message}");
                throw; // Relanza la excepción original
            }
            catch (JsonException ex)
            {
                Console.WriteLine($"Error: El archivo '{filePath}' no contiene JSON válido. Detalles: {ex.Message}");
                throw; // Relanza la excepción original
            }
        }

        /// <summary>
        /// Multiplica dos matrices cuadradas utilizando el algoritmo naïve.
        /// </summary>
        static List<List<double>> MultiplyMatrices(List<List<double>> matrixA, List<List<double>> matrixB)
        {
            int n = matrixA.Count;
            var result = new List<List<double>>();
            
            // Inicializar la matriz resultado con ceros
            for (int i = 0; i < n; i++)
            {
                var row = new List<double>();
                for (int j = 0; j < n; j++)
                {
                    row.Add(0.0);
                }
                result.Add(row);
            }
            
            // Realizar la multiplicación
            for (int i = 0; i < n; i++)
            {
                for (int j = 0; j < n; j++)
                {
                    double sum = 0.0;
                    for (int k = 0; k < n; k++)
                    {
                        sum += matrixA[i][k] * matrixB[k][j];
                    }
                    result[i][j] = sum;
                }
            }
            
            return result;
        }

        /// <summary>
        /// Realiza la multiplicación de matrices repetidamente y mide el tiempo promedio.
        /// </summary>
        static (double AverageTime, List<double> Times) MeasureMultiplication(List<List<double>> matrixA, List<List<double>> matrixB, int iterations)
        {
            var times = new List<double>();
            var stopwatch = new Stopwatch();
            
            for (int i = 0; i < iterations; i++)
            {
                stopwatch.Restart();
                MultiplyMatrices(matrixA, matrixB);
                stopwatch.Stop();
                times.Add(stopwatch.Elapsed.TotalSeconds);
            }
            
            double averageTime = times.Average();
            return (averageTime, times);
        }

        /// <summary>
        /// Registra los resultados en un archivo CSV dentro de la carpeta 'results'.
        /// </summary>
        /// <exception cref="IOException">Se lanza cuando hay un error al escribir en el archivo.</exception>
        static void RegistrarResultados(int matrixSize, int iterations, List<double> times, double averageTime)
        {
            try
            {
                // Determinar la ruta del directorio results relativo al ejecutable
                string currentDir = AppDomain.CurrentDomain.BaseDirectory;
                string resultsDir = Path.Combine(currentDir, "..", "..", "..", "..", "results");
                Directory.CreateDirectory(resultsDir);
                string resultsFile = Path.Combine(resultsDir, "benchmark_csharp_results.csv");
                
                bool fileExists = File.Exists(resultsFile);
                
                using (var writer = new StreamWriter(resultsFile, append: true))
                {
                    if (!fileExists)
                    {
                        writer.WriteLine("language,matrix_size,iterations,individual_times,average_time");
                    }
                    
                    string individualTimes = string.Join(" ", times.Select(t => t.ToString("F6", CultureInfo.InvariantCulture)));
                    writer.WriteLine($"C#,{matrixSize},{iterations},{individualTimes},{averageTime.ToString("F6", CultureInfo.InvariantCulture)}");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error al registrar resultados: {ex.Message}");
                throw; // Relanza la excepción para que sea manejada por el llamador
            }
        }

        static void Main(string[] args)
        {
            try
            {
                int matrixSize = 500;
                int iterations = 10;
                
                // Procesar argumentos de línea de comando
                for (int i = 0; i < args.Length; i++)
                {
                    if (args[i] == "--n" && i + 1 < args.Length)
                    {
                        if (int.TryParse(args[i + 1], out int n))
                        {
                            matrixSize = n;
                        }
                    }
                    else if (args[i] == "--iterations" && i + 1 < args.Length)
                    {
                        if (int.TryParse(args[i + 1], out int iter))
                        {
                            iterations = iter;
                        }
                    }
                }
                
                // Construir rutas relativas para acceder a los datasets
                string currentDir = AppDomain.CurrentDomain.BaseDirectory;
                string dataDir = Path.Combine(currentDir, "..", "..", "..", "..", "data");
                
                // Verificar si el directorio de datos existe
                if (!Directory.Exists(dataDir))
                {
                    Console.WriteLine($"Error: El directorio de datos '{dataDir}' no existe.");
                    Environment.Exit(1);
                }
                
                string matrixAFile = Path.Combine(dataDir, $"matrix_A_{matrixSize}.json");
                string matrixBFile = Path.Combine(dataDir, $"matrix_B_{matrixSize}.json");
                
                Console.WriteLine($"Cargando matrices de dimensión {matrixSize} desde el dataset...");
                
                var matrixA = LoadMatrix(matrixAFile);
                var matrixB = LoadMatrix(matrixBFile);
                
                Console.WriteLine($"Ejecutando benchmark con {iterations} iteraciones...");
                var (averageTime, times) = MeasureMultiplication(matrixA, matrixB, iterations);
                
                Console.WriteLine("Tiempos de cada iteración (en segundos):");
                foreach (var time in times)
                {
                    Console.WriteLine($"{time:F6}");
                }
                Console.WriteLine($"Tiempo promedio: {averageTime:F6} segundos");
                
                // Registrar resultados para su posterior comparación
                RegistrarResultados(matrixSize, iterations, times, averageTime);
                Console.WriteLine("Resultados registrados correctamente en 'results/benchmark_csharp_results.csv'.");
            }
            catch (FileNotFoundException ex)
            {
                Console.WriteLine($"Error fatal: {ex.Message}");
                Environment.Exit(1);
            }
            catch (JsonException ex)
            {
                Console.WriteLine($"Error fatal: {ex.Message}");
                Environment.Exit(1);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error inesperado: {ex.Message}");
                Environment.Exit(1);
            }
        }
    }
}
