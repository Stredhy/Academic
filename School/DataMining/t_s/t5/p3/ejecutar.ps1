# Construir y ejecutar el Proyecto 4 desde PowerShell.
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw 'No se encontró Docker. Instala o inicia Docker Desktop.'
}
docker info *> $null
if ($LASTEXITCODE -ne 0) { throw 'El motor de Docker no está disponible. Inicia Docker Desktop.' }
docker build -f 'Dockerfile(2)' -t proyecto4-multietapa:latest .
if ($LASTEXITCODE -ne 0) { throw 'Falló la construcción de la imagen.' }
docker run --rm proyecto4-multietapa:latest
if ($LASTEXITCODE -ne 0) { throw 'Falló la ejecución del contenedor.' }
