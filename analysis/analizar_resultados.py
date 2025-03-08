import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def analizar_resultados_benchmark():
    """
    Analiza los resultados de benchmark de multiplicación de matrices
    de diferentes lenguajes de programación.
    """
    print("Analizando resultados de benchmark...")
    
    # Obtener todos los archivos CSV del directorio results
    csv_files = glob.glob('../results/benchmark_*_results.csv')
    
    if not csv_files:
        print("No se encontraron archivos CSV en el directorio 'results'.")
        return
    
    # Crear directorio para guardar los resultados del análisis
    results_dir = 'resultados_analisis'
    os.makedirs(results_dir, exist_ok=True)
    
    # Dataframe para almacenar todos los resultados combinados
    all_results = pd.DataFrame()
    
    # Procesar cada archivo CSV
    for csv_file in csv_files:
        language = os.path.basename(csv_file).split('_')[1]  # Extraer nombre del lenguaje
        
        try:
            # Leer el archivo CSV
            df = pd.read_csv(csv_file)
            
            # Procesar los tiempos individuales (convertir de string a lista)
            if 'individual_times' in df.columns:
                df['individual_times'] = df['individual_times'].apply(lambda x: [float(t) for t in x.split()])
                
                # Calcular métricas adicionales
                df['min_time'] = df['individual_times'].apply(min)
                df['max_time'] = df['individual_times'].apply(max)
                df['std_dev'] = df['individual_times'].apply(np.std)
                
                # Si el formato no incluye average_time, calcularlo
                if 'average_time' not in df.columns:
                    df['average_time'] = df['individual_times'].apply(np.mean)
            
            # Añadir columna de lenguaje si no existe
            if 'language' not in df.columns:
                df['language'] = language
            
            # Añadir al dataframe combinado
            all_results = pd.concat([all_results, df])
            
        except Exception as e:
            print(f"Error al procesar el archivo {csv_file}: {e}")
    
    # Reiniciar el índice del dataframe combinado
    all_results = all_results.reset_index(drop=True)
    
    # Si no hay datos, terminar
    if all_results.empty:
        print("No se pudieron procesar los datos de los archivos CSV.")
        return
    
    # Calcular rendimiento relativo
    # Para cada tamaño de matriz, encontrar el tiempo promedio más rápido
    size_fastest = all_results.groupby('matrix_size')['average_time'].min().reset_index()
    size_fastest.rename(columns={'average_time': 'fastest_time'}, inplace=True)
    
    # Unir con el dataframe principal
    all_results = pd.merge(all_results, size_fastest, on='matrix_size')
    
    # Calcular rendimiento relativo (qué tan lento es en comparación con el más rápido)
    all_results['relative_performance'] = all_results['average_time'] / all_results['fastest_time']
    
    # Guardar dataframe combinado para análisis posteriores
    all_results.to_csv(os.path.join(results_dir, 'combined_results.csv'), index=False)
    
    # Generar análisis y visualizaciones
    generar_informe_general(all_results, results_dir)
    generar_visualizaciones(all_results, results_dir)
    analizar_escalabilidad(all_results, results_dir)
    
    print(f"Análisis completado. Los resultados se encuentran en el directorio '{results_dir}'.")
    
def generar_informe_general(df, results_dir):
    """
    Genera un informe general con las métricas principales para cada lenguaje y tamaño.
    """
    # Crear un resumen con las métricas principales
    metrics = df.groupby(['language', 'matrix_size']).agg({
        'average_time': 'mean',
        'min_time': 'min',
        'max_time': 'max',
        'std_dev': 'mean',
        'relative_performance': 'mean'
    }).reset_index()
    
    # Ordenar por tamaño de matriz y luego por tiempo promedio
    metrics = metrics.sort_values(['matrix_size', 'average_time'])
    
    # Guardar el informe como CSV
    metrics.to_csv(os.path.join(results_dir, 'metrics_summary.csv'), index=False)
    
    # Generar informe en formato texto
    with open(os.path.join(results_dir, 'benchmark_report.txt'), 'w') as f:
        f.write("INFORME DE BENCHMARK DE MULTIPLICACIÓN DE MATRICES\n")
        f.write("=" * 60 + "\n\n")
        
        # Para cada tamaño de matriz
        for size in sorted(df['matrix_size'].unique()):
            f.write(f"MATRICES DE TAMAÑO {size}x{size}\n")
            f.write("-" * 60 + "\n")
            
            size_metrics = metrics[metrics['matrix_size'] == size].sort_values('average_time')
            
            # El lenguaje más rápido
            fastest = size_metrics.iloc[0]
            f.write(f"Lenguaje más rápido: {fastest['language']} (Tiempo promedio: {fastest['average_time']:.6f} segundos)\n\n")
            
            f.write("Clasificación de rendimiento:\n")
            f.write(f"{'Posición':<10}{'Lenguaje':<15}{'Tiempo Prom.':<15}{'Tiempo Min.':<15}{'Tiempo Max.':<15}{'Desv. Est.':<15}{'Rend. Relativo':<15}\n")
            
            for i, (_, row) in enumerate(size_metrics.iterrows(), 1):
                f.write(f"{i:<10}{row['language']:<15}{row['average_time']:<15.6f}{row['min_time']:<15.6f}{row['max_time']:<15.6f}{row['std_dev']:<15.6f}{row['relative_performance']:<15.2f}x\n")
            
            f.write("\n\n")
    
def generar_visualizaciones(df, results_dir):
    """
    Genera visualizaciones para facilitar la comparación entre lenguajes.
    """
    # Configuración estética para los gráficos
    plt.style.use('ggplot')
    sns.set_palette("tab10")
    
    # 1. Gráfico de barras de tiempo promedio por lenguaje para cada tamaño de matriz
    plt.figure(figsize=(15, 10))
    
    for i, size in enumerate(sorted(df['matrix_size'].unique())):
        plt.subplot(2, 3, i+1)
        size_data = df[df['matrix_size'] == size]
        
        sns.barplot(x='language', y='average_time', data=size_data.sort_values('average_time'))
        plt.title(f'Tiempo promedio para matrices {size}x{size}')
        plt.ylabel('Tiempo (segundos)')
        plt.xlabel('Lenguaje')
        plt.xticks(rotation=45)
        plt.tight_layout()
    
    plt.savefig(os.path.join(results_dir, 'avg_time_by_language.png'))
    
    # 2. Gráfico de rendimiento relativo
    plt.figure(figsize=(15, 10))
    
    for i, size in enumerate(sorted(df['matrix_size'].unique())):
        plt.subplot(2, 3, i+1)
        size_data = df[df['matrix_size'] == size]
        
        sns.barplot(x='language', y='relative_performance', data=size_data.sort_values('relative_performance'))
        plt.title(f'Rendimiento relativo para matrices {size}x{size}')
        plt.ylabel('Veces más lento que el mejor')
        plt.xlabel('Lenguaje')
        plt.xticks(rotation=45)
        plt.tight_layout()
    
    plt.savefig(os.path.join(results_dir, 'relative_performance.png'))
    
    # 3. Gráfico de tiempos mínimos, promedio y máximos
    plt.figure(figsize=(15, 10))
    
    for i, size in enumerate(sorted(df['matrix_size'].unique())):
        plt.subplot(2, 3, i+1)
        size_data = df[df['matrix_size'] == size].sort_values('average_time')
        
        languages = size_data['language']
        avgs = size_data['average_time']
        mins = size_data['min_time']
        maxs = size_data['max_time']
        
        plt.errorbar(languages, avgs, yerr=[avgs-mins, maxs-avgs], fmt='o', capsize=5)
        plt.title(f'Variación de tiempo para matrices {size}x{size}')
        plt.ylabel('Tiempo (segundos)')
        plt.xlabel('Lenguaje')
        plt.xticks(rotation=45)
        plt.tight_layout()
    
    plt.savefig(os.path.join(results_dir, 'time_variation.png'))
    
    # 4. Gráfico de desviación estándar
    plt.figure(figsize=(15, 10))
    
    for i, size in enumerate(sorted(df['matrix_size'].unique())):
        plt.subplot(2, 3, i+1)
        size_data = df[df['matrix_size'] == size]
        
        sns.barplot(x='language', y='std_dev', data=size_data.sort_values('std_dev'))
        plt.title(f'Desviación estándar para matrices {size}x{size}')
        plt.ylabel('Desviación estándar (segundos)')
        plt.xlabel('Lenguaje')
        plt.xticks(rotation=45)
        plt.tight_layout()
    
    plt.savefig(os.path.join(results_dir, 'std_deviation.png'))
    
def analizar_escalabilidad(df, results_dir):
    """
    Analiza cómo escala cada lenguaje al aumentar el tamaño de la matriz.
    """
    plt.figure(figsize=(12, 8))
    
    # Obtener lenguajes únicos
    languages = sorted(df['language'].unique())
    
    # Para cada lenguaje, graficar tiempo vs tamaño de matriz
    for language in languages:
        language_data = df[df['language'] == language]
        language_data = language_data.sort_values('matrix_size')
        
        plt.plot(language_data['matrix_size'], language_data['average_time'], marker='o', label=language)
    
    plt.title('Escalabilidad: Tiempo vs Tamaño de Matriz')
    plt.xlabel('Tamaño de Matriz (n)')
    plt.ylabel('Tiempo Promedio (segundos)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    plt.savefig(os.path.join(results_dir, 'scalability_linear.png'))
    
    # También mostrar en escala logarítmica para mejor visualización
    plt.figure(figsize=(12, 8))
    
    for language in languages:
        language_data = df[df['language'] == language]
        language_data = language_data.sort_values('matrix_size')
        
        plt.plot(language_data['matrix_size'], language_data['average_time'], marker='o', label=language)
    
    plt.title('Escalabilidad: Tiempo vs Tamaño de Matriz (Escala Log)')
    plt.xlabel('Tamaño de Matriz (n)')
    plt.ylabel('Tiempo Promedio (segundos)')
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    plt.savefig(os.path.join(results_dir, 'scalability_log.png'))
    
    # Análisis de complejidad
    # Para cada lenguaje, intentar ajustar una curva cúbica (O(n³))
    # y verificar qué tan bien se ajusta
    plt.figure(figsize=(15, 10))
    
    for i, language in enumerate(languages):
        language_data = df[df['language'] == language]
        if len(language_data) < 3:  # Necesitamos al menos 3 puntos para ajustar una curva cúbica
            continue
            
        sizes = language_data['matrix_size'].values
        times = language_data['average_time'].values
        
        # Normalizar tamaños para mejor condicionamiento
        sizes_norm = sizes / np.max(sizes)
        
        try:
            # Ajustar curva cúbica con datos normalizados
            coeffs = np.polyfit(sizes_norm, times, 3)
            poly = np.poly1d(coeffs)
            
            # Función para evaluar en tamaños originales
            def poly_original(x):
                return poly(x / np.max(sizes))
            
            # Calcular R²
            y_pred = np.array([poly_original(s) for s in sizes])
            y_mean = np.mean(times)
            ss_tot = np.sum((times - y_mean) ** 2)
            ss_res = np.sum((times - y_pred) ** 2)
            r_squared = 1 - (ss_res / ss_tot)
            
            # Graficar resultados
            plt.subplot(3, 3, i+1)
            plt.scatter(sizes, times, label='Datos reales')
            
            # Crear puntos x más suaves para la curva
            x_smooth = np.linspace(min(sizes), max(sizes), 100)
            plt.plot(x_smooth, [poly_original(x) for x in x_smooth], 'r-', 
                     label=f'Ajuste O(n³): R²={r_squared:.4f}')
            
            plt.title(f'Análisis de Complejidad para {language}')
            plt.xlabel('Tamaño de Matriz (n)')
            plt.ylabel('Tiempo (segundos)')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
        except Exception as e:
            print(f"Error en el análisis de complejidad para {language}: {str(e)}")
    
    plt.savefig(os.path.join(results_dir, 'complexity_analysis.png'))
    
    # Guardar los coeficientes de complejidad para cada lenguaje
    complexity_data = []
    
    for language in languages:
        language_data = df[df['language'] == language]
        if len(language_data) < 3:
            continue
            
        sizes = language_data['matrix_size'].values
        times = language_data['average_time'].values
        
        # Ajustar varios modelos
        models = {
            'lineal': 1,     # O(n)
            'cuadrático': 2, # O(n²)
            'cúbico': 3      # O(n³)
        }
        
        results = {}
        
        for name, degree in models.items():
            coeffs = np.polyfit(sizes, times, degree)
            p = np.poly1d(coeffs)
            y_pred = p(sizes)
            
            ss_tot = np.sum((times - np.mean(times)) ** 2)
            ss_res = np.sum((times - y_pred) ** 2)
            r_squared = 1 - (ss_res / ss_tot)
            
            results[name] = {
                'coeffs': coeffs,
                'r_squared': r_squared
            }
        
        # Determinar el mejor modelo
        best_model = max(results.items(), key=lambda x: x[1]['r_squared'])
        
        complexity_data.append({
            'language': language,
            'best_model': best_model[0],
            'r_squared': best_model[1]['r_squared'],
            'coeficientes': str(best_model[1]['coeffs'])
        })
    
    # Guardar resultados del análisis de complejidad
    complexity_df = pd.DataFrame(complexity_data)
    complexity_df.to_csv(os.path.join(results_dir, 'complexity_results.csv'), index=False)

if __name__ == "__main__":
    analizar_resultados_benchmark()