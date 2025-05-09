# Obtener el directorio del script actual
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Establecer el directorio del archivo docker-compose.yml
$ComposeDir = $ScriptDir

# Cambiar al directorio de trabajo
Set-Location -Path $ComposeDir

# Función para detener los contenedores
function Cleanup {
    Write-Host "`nDeteniendo contenedores..."
    docker compose stop
}

# Construir y levantar los contenedores
docker compose up --build -d

# Iniciar seguimiento de logs en un job
$logsJob = Start-Job -ScriptBlock { docker compose logs -f }

try {
    # Mantener el script corriendo indefinidamente hasta interrupción
    while ($true) {
        Start-Sleep -Seconds 1
    }
}
finally {
    # Cuando se interrumpe (Ctrl+C), ejecutar limpieza
    Cleanup
    # Detener el job de logs si sigue activo
    if ($logsJob.State -eq 'Running') {
        Stop-Job $logsJob
        Remove-Job $logsJob
    }
}
