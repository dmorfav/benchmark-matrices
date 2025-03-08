/**
 * Implementación naïve de la multiplicación de matrices en C++.
 * Carga las matrices desde archivos JSON, mide el tiempo de ejecución y registra los resultados.
 */

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <chrono>
#include <numeric>
#include <cstdlib>
#include <sstream>
#include <iomanip>

// Tipo para representar matrices como vectores bidimensionales
using Matrix = std::vector<std::vector<double>>;

/**
 * Carga una matriz desde un archivo JSON.
 * Implementación simple de parser JSON para matrices 2D.
 * 
 * @param file_path Ruta del archivo JSON
 * @return Matriz cargada desde el archivo
 */
Matrix load_matrix(const std::string& file_path) {
    try {
        std::ifstream file(file_path);
        if (!file.is_open()) {
            std::cerr << "Error: El archivo '" << file_path << "' no existe." << std::endl;
            exit(1);
        }
        
        // Leer todo el contenido del archivo
        std::stringstream buffer;
        buffer << file.rdbuf();
        std::string content = buffer.str();
        
        // Parsear JSON manualmente (versión mejorada)
        Matrix matrix;
        
        // Buscar el inicio del array de arrays
        size_t pos = content.find('[');
        if (pos == std::string::npos) {
            throw std::runtime_error("Formato JSON no válido: no se encontró el inicio del array.");
        }
        pos++; // Saltar el primer '['
        
        // Parsear cada fila
        while (pos < content.size()) {
            // Buscar el inicio de una fila
            pos = content.find('[', pos);
            if (pos == std::string::npos) break;
            pos++; // Saltar '['
            
            std::vector<double> row;
            
            // Parsear los valores de la fila
            while (pos < content.size() && content[pos] != ']') {
                // Saltar espacios y comas
                while (pos < content.size() && (content[pos] == ' ' || content[pos] == ',' || content[pos] == '\n' || content[pos] == '\r' || content[pos] == '\t')) {
                    pos++;
                }
                
                if (content[pos] == ']') break;
                
                // Leer un número
                try {
                    // Extraer la subcadena que podría ser un número
                    std::string numStr;
                    size_t i = pos;
                    while (i < content.size() && 
                           (std::isdigit(content[i]) || content[i] == '.' || content[i] == '-' || content[i] == '+' || 
                            content[i] == 'e' || content[i] == 'E')) {
                        numStr += content[i];
                        i++;
                    }
                    
                    if (numStr.empty()) {
                        std::cerr << "Caracter inesperado en posición " << pos << ": '" << content[pos] << "'" << std::endl;
                        pos++; // Intentar saltar el caracter problemático
                        continue;
                    }
                    
                    size_t end_pos;
                    double value = std::stod(numStr, &end_pos);
                    
                    if (end_pos == 0) {
                        throw std::runtime_error("No se pudo convertir a número: " + numStr);
                    }
                    
                    row.push_back(value);
                    pos += end_pos;
                } catch (const std::exception& e) {
                    // Mostrar contexto del error
                    size_t context_start = (pos > 10) ? pos - 10 : 0;
                    size_t context_length = (content.size() - context_start > 20) ? 20 : content.size() - context_start;
                    std::string context = content.substr(context_start, context_length);
                    
                    throw std::runtime_error(std::string("Error en posición ") + 
                                             std::to_string(pos) + ": " + e.what() + 
                                             "\nContexto: \"" + context + "\"");
                }
            }
            
            if (row.size() > 0) {
                matrix.push_back(row);
            }
            
            size_t end_bracket = content.find(']', pos);
            if (end_bracket == std::string::npos) {
                throw std::runtime_error("No se encontró el cierre de corchete ']' para una fila");
            }
            pos = end_bracket + 1; // Saltar al final de la fila
        }
        
        return matrix;
    } catch (const std::exception& e) {
        std::cerr << "Error al leer el archivo JSON: " << e.what() << std::endl;
        exit(1);
    }
}

/**
 * Multiplica dos matrices cuadradas utilizando el algoritmo naïve.
 * 
 * @param matrix_a Primera matriz de dimensión n x n
 * @param matrix_b Segunda matriz de dimensión n x n
 * @return Matriz resultante de la multiplicación
 */
Matrix multiply_matrices(const Matrix& matrix_a, const Matrix& matrix_b) {
    int n = matrix_a.size();
    
    // Inicializa la matriz resultado con ceros
    Matrix C(n, std::vector<double>(n, 0.0));
    
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            double s = 0.0;
            for (int k = 0; k < n; k++) {
                s += matrix_a[i][k] * matrix_b[k][j];
            }
            C[i][j] = s;
        }
    }
    
    return C;
}

/**
 * Realiza la multiplicación de matrices repetidamente y mide el tiempo promedio.
 * 
 * @param matrix_a Primera matriz
 * @param matrix_b Segunda matriz
 * @param iterations Número de iteraciones a ejecutar
 * @return Par (tiempo_promedio, lista_de_tiempos)
 */
std::pair<double, std::vector<double>> measure_multiplication(
    const Matrix& matrix_a, 
    const Matrix& matrix_b, 
    int iterations
) {
    std::vector<double> times;
    
    for (int i = 0; i < iterations; i++) {
        auto start_time = std::chrono::high_resolution_clock::now();
        multiply_matrices(matrix_a, matrix_b);
        auto end_time = std::chrono::high_resolution_clock::now();
        
        // Calcular duración en segundos
        std::chrono::duration<double> elapsed = end_time - start_time;
        times.push_back(elapsed.count());
    }
    
    // Calcular tiempo promedio
    double average_time = std::accumulate(times.begin(), times.end(), 0.0) / times.size();
    
    return std::make_pair(average_time, times);
}

/**
 * Crea un directorio si no existe
 * 
 * @param path Ruta del directorio a crear
 * @return true si se creó con éxito o ya existía, false en caso de error
 */
bool create_directory(const std::string& path) {
    #ifdef _WIN32
    // Windows
    int result = system(("mkdir \"" + path + "\" 2> nul").c_str());
    return result == 0 || result == 1;
    #else
    // Unix/Linux/macOS
    int result = system(("mkdir -p \"" + path + "\" 2>/dev/null").c_str());
    return result == 0;
    #endif
}

/**
 * Comprueba si un archivo existe
 * 
 * @param file_path Ruta del archivo
 * @return true si el archivo existe, false en caso contrario
 */
bool file_exists(const std::string& file_path) {
    std::ifstream file(file_path);
    return file.good();
}

/**
 * Registra los resultados en un archivo CSV dentro de la carpeta 'results'.
 * 
 * @param matrix_size Tamaño de la matriz
 * @param iterations Número de iteraciones
 * @param times Lista de tiempos individuales
 * @param average_time Tiempo promedio
 */
void registrar_resultados(
    int matrix_size, 
    int iterations, 
    const std::vector<double>& times, 
    double average_time
) {
    // Determinar la ruta del directorio results relativo al ejecutable
    std::string results_dir = "../results";
    
    // Crear el directorio si no existe
    if (!create_directory(results_dir)) {
        std::cerr << "Error al crear el directorio de resultados." << std::endl;
        return;
    }
    
    std::string results_file = results_dir + "/benchmark_cpp_results.csv";
    
    // Verificar si el archivo ya existe
    bool file_exists_flag = file_exists(results_file);
    
    // Abrir archivo en modo append
    std::ofstream csvfile(results_file, std::ios::app);
    
    if (!csvfile.is_open()) {
        std::cerr << "Error al abrir el archivo CSV para escribir resultados." << std::endl;
        return;
    }
    
    // Escribir cabecera si el archivo es nuevo
    if (!file_exists_flag) {
        csvfile << "language,matrix_size,iterations,individual_times,average_time" << std::endl;
    }
    
    // Escribir datos
    csvfile << "C++," << matrix_size << "," << iterations << ",";
    
    // Escribir tiempos individuales
    for (size_t i = 0; i < times.size(); ++i) {
        csvfile << std::fixed << std::setprecision(6) << times[i];
        if (i < times.size() - 1) {
            csvfile << " ";
        }
    }
    
    csvfile << "," << std::fixed << std::setprecision(6) << average_time << std::endl;
    
    csvfile.close();
}

int main(int argc, char* argv[]) {
    // Valores por defecto
    int n = 500;
    int iterations = 10;
    
    // Parsear argumentos de línea de comandos manualmente
    for (int i = 1; i < argc; i++) {
        std::string arg = argv[i];
        
        if (arg == "--n" && i + 1 < argc) {
            n = std::stoi(argv[++i]);
        } else if (arg == "--iterations" && i + 1 < argc) {
            iterations = std::stoi(argv[++i]);
        } else if (arg == "--help" || arg == "-h") {
            std::cout << "Uso: " << argv[0] << " [opciones]" << std::endl;
            std::cout << "Opciones:" << std::endl;
            std::cout << "  --n <valor>         Dimensión de las matrices cuadradas (default: 500)" << std::endl;
            std::cout << "  --iterations <valor> Número de iteraciones para medir el tiempo promedio (default: 10)" << std::endl;
            std::cout << "  --help, -h          Muestra este mensaje de ayuda" << std::endl;
            return 0;
        }
    }
    
    // Construir rutas relativas para acceder a los datasets
    std::string data_dir = "../data";
    
    std::string matrix_a_file = data_dir + "/matrix_A_" + std::to_string(n) + ".json";
    std::string matrix_b_file = data_dir + "/matrix_B_" + std::to_string(n) + ".json";
    
    std::cout << "Cargando matrices de dimensión " << n << " desde el dataset..." << std::endl;
    
    // Cargar matrices
    Matrix matrix_a = load_matrix(matrix_a_file);
    Matrix matrix_b = load_matrix(matrix_b_file);
    
    std::cout << "Ejecutando benchmark con " << iterations << " iteraciones..." << std::endl;
    
    std::pair<double, std::vector<double>> result = measure_multiplication(matrix_a, matrix_b, iterations);
    double average_time = result.first;
    std::vector<double> times = result.second;
    
    std::cout << "Tiempos de cada iteración (en segundos):" << std::endl;
    for (double t : times) {
        std::cout << std::fixed << std::setprecision(6) << t << std::endl;
    }
    
    std::cout << "Tiempo promedio: " << std::fixed << std::setprecision(6) << average_time << " segundos" << std::endl;
    
    // Registrar resultados para su posterior comparación
    registrar_resultados(n, iterations, times, average_time);
    std::cout << "Resultados registrados correctamente en 'results/benchmark_cpp_results.csv'." << std::endl;
    
    return 0;
}
