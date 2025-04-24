#!/bin/bash

# Función que se ejecuta al recibir una señal de terminación
cleanup() {
    echo "Deteniendo contenedores..."
    docker-compose stop
    exit 0
}

# Capturar señales de interrupción (SIGINT) y terminación (SIGTERM)
trap cleanup SIGINT SIGTERM

# Directorio donde se encuentra el script run.sh
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Directorio donde se encuentra docker-compose.yml
COMPOSE_DIR="$SCRIPT_DIR"

# Cambiar al directorio que contiene docker-compose.yml
cd "$COMPOSE_DIR"

# Construir y levantar los contenedores
docker-compose up --build -d

# Seguir los logs de los contenedores
docker-compose logs -f &

# Esperar a que se reciba una señal de terminación
wait