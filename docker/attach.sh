#!/bin/bash

# Verifica si docker-compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "docker-compose no está instalado. Por favor, instálalo para continuar."
    exit 1
fi

# Obtén el nombre del proyecto desde el directorio actual
PROYECTO=$(basename "$(pwd)" | tr '[:upper:]' '[:lower:]' | tr -cd 'a-z0-9_')

# Verifica si se ha obtenido un nombre de proyecto
if [ -z "$PROYECTO" ]; then
    echo "No se pudo obtener el nombre del proyecto."
    exit 1
fi

# Obtiene el ID del contenedor correspondiente al proyecto
CONTENEDOR_ID=$(docker ps -qf "name=$PROYECTO")

# Verifica si se obtuvo un ID de contenedor
if [ -z "$CONTENEDOR_ID" ]; then
    echo "No se pudo obtener el ID del contenedor para el proyecto '$PROYECTO'."
    exit 1
fi

# Verifica si el contenedor está en ejecución
if docker ps -q -f id="$CONTENEDOR_ID" -f status=running &> /dev/null; then
    echo "Conectando al contenedor $PROYECTO con id $CONTENEDOR_ID..."
    docker attach "$CONTENEDOR_ID"
else
    echo "El contenedor $CONTENEDOR_ID no está en ejecución o no existe."
    exit 1
fi