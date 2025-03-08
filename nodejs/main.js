#!/usr/bin/env node
/**
 * Implementación naïve de la multiplicación de matrices en Node.js.
 * Carga las matrices desde archivos JSON, mide el tiempo de ejecución y registra los resultados.
 */

const fs = require('fs');
const path = require('path');
const { performance } = require('perf_hooks');
const { program } = require('commander');

/**
 * Carga una matriz desde un archivo JSON.
 * @param {string} filePath - Ruta al archivo JSON.
 * @returns {Array<Array<number>>} - Matriz cargada.
 */
function loadMatrix(filePath) {
    try {
        const data = fs.readFileSync(filePath, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        if (error.code === 'ENOENT') {
            console.error(`Error: El archivo '${filePath}' no existe.`);
            process.exit(1);
        } else if (error instanceof SyntaxError) {
            console.error(`Error: El archivo '${filePath}' no contiene JSON válido.`);
            process.exit(1);
        } else {
            console.error(`Error inesperado: ${error.message}`);
            process.exit(1);
        }
    }
}

/**
 * Multiplica dos matrices cuadradas utilizando el algoritmo naïve.
 * @param {Array<Array<number>>} matrixA - Primera matriz de dimensión n x n.
 * @param {Array<Array<number>>} matrixB - Segunda matriz de dimensión n x n.
 * @returns {Array<Array<number>>} - Matriz resultante C de la multiplicación.
 */
function multiplyMatrices(matrixA, matrixB) {
    const n = matrixA.length;
    // Inicializa la matriz resultado con ceros.
    const C = Array(n).fill().map(() => Array(n).fill(0.0));
    
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            let s = 0.0;
            for (let k = 0; k < n; k++) {
                s += matrixA[i][k] * matrixB[k][j];
            }
            C[i][j] = s;
        }
    }
    return C;
}

/**
 * Realiza la multiplicación de matrices repetidamente y mide el tiempo promedio.
 * @param {Array<Array<number>>} matrixA - Primera matriz.
 * @param {Array<Array<number>>} matrixB - Segunda matriz.
 * @param {number} iterations - Número de iteraciones a ejecutar.
 * @returns {[number, Array<number>]} - Tupla [tiempo_promedio, lista_de_tiempos].
 */
function measureMultiplication(matrixA, matrixB, iterations) {
    const times = [];
    
    // Calcular el incremento del 20%
    const progressStep = Math.max(1, Math.floor(iterations / 5));
    console.log(`Iniciando multiplicación de matrices (${iterations} iteraciones)...`);
    
    for (let i = 0; i < iterations; i++) {
        // Mostrar progreso cada 20% o si es la última iteración
        if (i % progressStep === 0 || i === iterations - 1) {
            const progressPercent = (i / iterations) * 100.0;
            console.log(`Progreso: Iteración ${i + 1}/${iterations} (${progressPercent.toFixed(1)}%)`);
        }
        
        const startTime = performance.now();
        multiplyMatrices(matrixA, matrixB);
        const endTime = performance.now();
        // Convertir de milisegundos a segundos
        times.push((endTime - startTime) / 1000);
    }
    
    console.log("Multiplicación de matrices completada (100%).");
    
    const averageTime = times.reduce((a, b) => a + b, 0) / times.length;
    return [averageTime, times];
}

/**
 * Registra los resultados en un archivo CSV dentro de la carpeta 'results'.
 * @param {number} matrixSize - Tamaño de la matriz.
 * @param {number} iterations - Número de iteraciones.
 * @param {Array<number>} times - Lista de tiempos individuales.
 * @param {number} averageTime - Tiempo promedio.
 */
function registrarResultados(matrixSize, iterations, times, averageTime) {
    // Determinar la ruta del directorio results relativo al script
    const currentDir = path.dirname(path.resolve(__filename));
    const resultsDir = path.join(currentDir, "..", "results");
    
    // Crear el directorio si no existe
    if (!fs.existsSync(resultsDir)) {
        fs.mkdirSync(resultsDir, { recursive: true });
    }
    
    const resultsFile = path.join(resultsDir, "benchmark_nodejs_results.csv");
    
    // Verifica si el archivo ya existe para incluir cabecera
    const fileExists = fs.existsSync(resultsFile);
    
    const header = ["language", "matrix_size", "iterations", "individual_times", "average_time"].join(",") + "\n";
    const row = [
        "Node.js",
        matrixSize,
        iterations,
        times.map(t => t.toFixed(6)).join(" "),
        averageTime.toFixed(6)
    ].join(",") + "\n";
    
    if (!fileExists) {
        fs.writeFileSync(resultsFile, header + row);
    } else {
        fs.appendFileSync(resultsFile, row);
    }
}

function main() {
    program
        .description("Benchmark naïve de multiplicación de matrices en Node.js")
        .option("-n, --dimension <n>", "Dimensión de las matrices cuadradas", 500)
        .option("-i, --iterations <count>", "Número de iteraciones para medir el tiempo promedio", 10)
        .parse(process.argv);
    
    const options = program.opts();
    
    // Asegurarse de que los valores son numéricos
    const n = parseInt(options.dimension);
    const iterations = parseInt(options.iterations);
    
    if (isNaN(n) || isNaN(iterations)) {
        console.error("Error: Los valores de dimensión e iteraciones deben ser números.");
        process.exit(1);
    }
    
    // Construir rutas relativas para acceder a los datasets
    const currentDir = path.dirname(path.resolve(__filename));
    const dataDir = path.join(currentDir, "..", "data");
    
    // Verificar si el directorio de datos existe
    if (!fs.existsSync(dataDir)) {
        console.error(`Error: El directorio de datos '${dataDir}' no existe.`);
        process.exit(1);
    }
    
    const matrixAFile = path.join(dataDir, `matrix_A_${n}.json`);
    const matrixBFile = path.join(dataDir, `matrix_B_${n}.json`);
    
    console.log(`Cargando matrices de dimensión ${n} desde el dataset...`);
    
    // La función loadMatrix ahora maneja internamente el caso cuando los archivos no existen
    const matrixA = loadMatrix(matrixAFile);
    const matrixB = loadMatrix(matrixBFile);
    
    console.log(`Ejecutando benchmark con ${iterations} iteraciones...`);
    const [averageTime, times] = measureMultiplication(matrixA, matrixB, iterations);
    
    console.log("Tiempos de cada iteración (en segundos):");
    times.forEach(t => console.log(t.toFixed(6)));
    console.log(`Tiempo promedio: ${averageTime.toFixed(6)} segundos`);
    
    // Registrar resultados para su posterior comparación
    registrarResultados(n, iterations, times, averageTime);
    console.log("Resultados registrados correctamente en 'results/benchmark_nodejs_results.csv'.");
}

if (require.main === module) {
    main();
}

module.exports = {
    loadMatrix,
    multiplyMatrices,
    measureMultiplication,
    registrarResultados
};
