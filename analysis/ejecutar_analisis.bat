@echo off
:: Activar entorno virtual
call env\Scripts\activate.bat

:: Ejecutar script de análisis
python analizar_resultados.py

echo.
echo Analisis completado. Revisa la carpeta 'analysis' para ver los resultados.
pause 