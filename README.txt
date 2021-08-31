pasos para el deploy de la aplicacion

1. pasarse al entorno conda
2. instalar pyinstaller
3. ejecutar el comando: pyinstaller --onefile -w main.py
5. ubicar el archivo main.exe que se encuentra en el directorio dist
6. en la misma ubicacion del archivo crear una carpeta con la siguiente estructura
    datos/
        [fecha]/
            [temperatura]/
                file.txt o file.csv
                ...