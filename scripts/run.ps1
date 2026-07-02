$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir

$Python = Join-Path $ProjectDir "venv\Scripts\python.exe"

Write-Host "Iniciando Sibyl..."
Write-Host ""

if (-not (Test-Path $Python)) {
    Write-Host "Erro: ambiente virtual nao encontrado em $ProjectDir\venv"
    Write-Host "Crie o ambiente e instale as dependencias:"
    Write-Host "  python -m venv venv"
    Write-Host "  pip install -r requirements.txt"
    exit 1
}

Set-Location $ProjectDir

Write-Host "Aplicando migrations..."
& $Python manage.py migrate
Write-Host ""

Write-Host "Inicializando servidor..."
Write-Host ""
Write-Host "Sibyl disponivel em:"
Write-Host "http://127.0.0.1:8000"
Write-Host ""

& $Python manage.py runserver
