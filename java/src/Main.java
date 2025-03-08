import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

/**
 * Implementación naïve de la multiplicación de matrices en Java.
 * Carga las matrices desde archivos JSON, mide el tiempo de ejecución y registra los resultados.
 * Usa solo funcionalidades nativas de Java, sin bibliotecas externas.
 */
public class Main {
    /**
     * Carga una matriz desde un archivo JSON usando solo funciones nativas.
     * 
     * @param filePath Ruta al archivo JSON
     * @return Matriz de dobles
     */
    public static double[][] loadMatrix(String filePath) {
        try {
            // Leer todo el contenido del archivo
            String jsonContent = Files.readString(Path.of(filePath));
            
            // Limpiar espacios en blanco innecesarios
            jsonContent = jsonContent.trim();
            
            // Lista para almacenar filas de la matriz
            List<List<Double>> matrix = new ArrayList<>();
            
            // Analizamos el JSON manualmente para extraer los números
            boolean inArray = false;
            boolean inNumber = false;
            StringBuilder currentNumber = new StringBuilder();
            List<Double> currentRow = new ArrayList<>();
            
            for (int i = 0; i < jsonContent.length(); i++) {
                char c = jsonContent.charAt(i);
                
                if (c == '[') {
                    if (inArray) {
                        // Inicio de una nueva fila
                        currentRow = new ArrayList<>();
                    }
                    inArray = true;
                } else if (c == ']') {
                    // Fin de número si estamos en uno
                    if (inNumber) {
                        currentRow.add(Double.parseDouble(currentNumber.toString()));
                        currentNumber = new StringBuilder();
                        inNumber = false;
                    }
                    
                    // Si la fila no está vacía, la añadimos a la matriz
                    if (!currentRow.isEmpty()) {
                        matrix.add(currentRow);
                        currentRow = new ArrayList<>();
                    }
                } else if (c == ',') {
                    // Fin de número si estamos en uno
                    if (inNumber) {
                        currentRow.add(Double.parseDouble(currentNumber.toString()));
                        currentNumber = new StringBuilder();
                        inNumber = false;
                    }
                } else if (Character.isDigit(c) || c == '.' || c == '-' || c == 'E' || c == 'e' || c == '+') {
                    // Parte de un número
                    if (!inNumber) {
                        inNumber = true;
                        currentNumber = new StringBuilder();
                    }
                    currentNumber.append(c);
                }
                // Ignoramos espacios y otros caracteres
            }
            
            // Convertir a array de double[][]
            double[][] result = new double[matrix.size()][];
            for (int i = 0; i < matrix.size(); i++) {
                List<Double> row = matrix.get(i);
                result[i] = new double[row.size()];
                for (int j = 0; j < row.size(); j++) {
                    result[i][j] = row.get(j);
                }
            }
            
            return result;
        } catch (IOException e) {
            System.out.println("Error: El archivo '" + filePath + "' no existe.");
            System.exit(1);
        } catch (NumberFormatException e) {
            System.out.println("Error: El archivo contiene valores no numéricos: " + e.getMessage());
            System.exit(1);
        } catch (Exception e) {
            System.out.println("Error al procesar el archivo JSON: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
        return null;
    }

    /**
     * Multiplica dos matrices cuadradas A y B utilizando el algoritmo naïve.
     * 
     * @param matrixA Primera matriz de dimensión n x n
     * @param matrixB Segunda matriz de dimensión n x n
     * @return Matriz resultante C de la multiplicación
     */
    public static double[][] multiplyMatrices(double[][] matrixA, double[][] matrixB) {
        int n = matrixA.length;
        double[][] C = new double[n][n];
        
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                double s = 0.0;
                for (int k = 0; k < n; k++) {
                    s += matrixA[i][k] * matrixB[k][j];
                }
                C[i][j] = s;
            }
        }
        return C;
    }

    /**
     * Realiza la multiplicación de matrices repetidamente y mide el tiempo promedio.
     * 
     * @param matrixA Primera matriz
     * @param matrixB Segunda matriz
     * @param iterations Número de iteraciones a ejecutar
     * @return Un objeto con el tiempo promedio y la lista de tiempos
     */
    public static MeasurementResult measureMultiplication(double[][] matrixA, double[][] matrixB, int iterations) {
        List<Double> times = new ArrayList<>();
        
        for (int i = 0; i < iterations; i++) {
            long startTime = System.nanoTime();
            multiplyMatrices(matrixA, matrixB);
            long endTime = System.nanoTime();
            double elapsedTimeInSeconds = (endTime - startTime) / 1_000_000_000.0;
            times.add(elapsedTimeInSeconds);
        }
        
        double averageTime = 0;
        for (Double time : times) {
            averageTime += time;
        }
        averageTime /= times.size();
        return new MeasurementResult(averageTime, times);
    }

    /**
     * Registra los resultados en un archivo CSV dentro de la carpeta 'results'.
     * 
     * @param matrixSize Tamaño de la matriz
     * @param iterations Número de iteraciones
     * @param times Lista de tiempos individuales
     * @param averageTime Tiempo promedio
     */
    public static void registrarResultados(int matrixSize, int iterations, List<Double> times, double averageTime) throws IOException {
        // Determinar la ruta del directorio results relativo al script
        String currentDir = new File(".").getCanonicalPath();
        Path resultsDir = Paths.get(currentDir, "../results");
        Files.createDirectories(resultsDir);
        File resultsFile = new File(resultsDir.toString(), "benchmark_java_results.csv");
        
        boolean fileExists = resultsFile.exists();
        
        try (FileWriter writer = new FileWriter(resultsFile, true)) {
            if (!fileExists) {
                writer.write("language,matrix_size,iterations,individual_times,average_time\n");
            }
            
            StringBuilder timesBuilder = new StringBuilder();
            for (Double time : times) {
                if (timesBuilder.length() > 0) {
                    timesBuilder.append(" ");
                }
                timesBuilder.append(String.format("%.6f", time));
            }
            
            writer.write(String.format("Java,%d,%d,%s,%.6f\n", 
                                     matrixSize, 
                                     iterations, 
                                     timesBuilder.toString(), 
                                     averageTime));
        }
    }

    /**
     * Método principal que ejecuta el benchmark.
     */
    public static void main(String[] args) {
        int n = 500;  // Valor por defecto
        int iterations = 10;  // Valor por defecto
        
        // Procesar argumentos de línea de comandos
        for (int i = 0; i < args.length; i++) {
            if (args[i].equals("--n") && i + 1 < args.length) {
                n = Integer.parseInt(args[i + 1]);
                i++;
            } else if (args[i].equals("--iterations") && i + 1 < args.length) {
                iterations = Integer.parseInt(args[i + 1]);
                i++;
            }
        }
        
        System.out.println("Benchmark de multiplicación de matrices en Java");
        
        try {
            // Construir rutas relativas para acceder a los datasets
            String currentDir = new File(".").getCanonicalPath();
            File dataDir = new File(currentDir, "../data");
            
            // Verificar si el directorio de datos existe
            if (!dataDir.exists()) {
                System.out.println("Error: El directorio de datos '" + dataDir.getPath() + "' no existe.");
                System.exit(1);
            }
            
            String matrixAFile = new File(dataDir, "matrix_A_" + n + ".json").getPath();
            String matrixBFile = new File(dataDir, "matrix_B_" + n + ".json").getPath();
            
            System.out.println("Cargando matrices de dimensión " + n + " desde el dataset...");
            
            double[][] matrixA = loadMatrix(matrixAFile);
            double[][] matrixB = loadMatrix(matrixBFile);
            
            System.out.println("Ejecutando benchmark con " + iterations + " iteraciones...");
            MeasurementResult result = measureMultiplication(matrixA, matrixB, iterations);
            
            System.out.println("Tiempos de cada iteración (en segundos):");
            for (double t : result.times) {
                System.out.printf("%.6f%n", t);
            }
            System.out.printf("Tiempo promedio: %.6f segundos%n", result.averageTime);
            
            // Registrar resultados para su posterior comparación
            registrarResultados(n, iterations, result.times, result.averageTime);
            System.out.println("Resultados registrados correctamente en 'results/benchmark_java_results.csv'.");
            
        } catch (IOException e) {
            System.out.println("Error: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    /**
     * Clase auxiliar para almacenar los resultados de la medición.
     */
    static class MeasurementResult {
        public double averageTime;
        public List<Double> times;
        
        public MeasurementResult(double averageTime, List<Double> times) {
            this.averageTime = averageTime;
            this.times = times;
        }
    }
}
