# Run Alembic migrations (Windows PowerShell)
# Usage: .\scripts\migrate.ps1 [revision_message]

param(
    [string]$Message = "autogenerate"
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

if (-not (Test-Path ".venv")) {
    Write-Error "Virtual environment not found. Run: python -m venv .venv"
}

.\.venv\Scripts\Activate.ps1

if ($Message -eq "upgrade") {
    alembic upgrade head
} else {
    alembic revision --autogenerate -m $Message
    Write-Host "Review the new file in alembic/versions/, then run: alembic upgrade head"
}
