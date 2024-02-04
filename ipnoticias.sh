#!/bin/bash

set -x  # Habilita la depuración

# Parte 1: Activar canales
# URL de la página web para activar
url="https://tv.teleclub.xyz/activar"

# User-Agent de Chrome
user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"

# Datos a enviar en la solicitud POST
post_data="submit=ACTIVAR+AHORA%21"

# Archivo de registro
log_file="canales.log"

# Realiza una solicitud POST utilizando wget con el User-Agent de Chrome y datos en el cuerpo de la solicitud
wget --no-check-certificate --user-agent="$user_agent" --post-data="$post_data" "$url" -O response.html >> "$log_file" 2>&1

# Verifica si la respuesta contiene información relevante
if grep -q "ACTIVADO" response.html; then
    echo "La solicitud POST se ha completado con éxito."
else
    echo "No se pudo completar la solicitud POST."
fi

# Limpia el archivo de respuesta
rm response.html

# Parte 2: Generar el archivo M3U8
# Asegura la instalación de requests si es necesario
python3 -m pip install requests

# Cambia al directorio del script de Python
cd $(dirname $0)/scripts/

# Ejecuta el script de Python y guarda la salida en un archivo M3U8
python3 ipnoticias.py > ../ipnoticias.m3u8

echo "m3u8 grabbed"

# Deshabilita la depuración
set +x
