@echo off
echo Creando entorno virtual...
python -m venv env

echo Activando entorno virtual...
call env\Scripts\activate.bat

echo Actualizando pip y herramientas basicas...
pip install --upgrade pip setuptools wheel

echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo Entorno configurado correctamente. Para activar el entorno ejecuta:
echo env\Scripts\activate.bat
echo.
echo Para ejecutar el script de analisis:
echo python analizar_resultados.py 