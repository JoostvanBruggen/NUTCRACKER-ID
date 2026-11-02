# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2026 Joost van Bruggen — NUTCRACKER-ID
[CmdletBinding()]
param(
    [string]$Photos = '',
    [string]$Output = '',
    [string]$PythonExecutable = '',
    [switch]$Help
)
$ErrorActionPreference = 'Stop'
$projectRoot = $PSScriptRoot
if (-not $PythonExecutable) {
    $PythonExecutable = Join-Path $projectRoot '.venv\Scripts\python.exe'
} elseif (-not [IO.Path]::IsPathRooted($PythonExecutable)) {
    $PythonExecutable = Join-Path $projectRoot $PythonExecutable
}
if (-not (Test-Path -LiteralPath $PythonExecutable -PathType Leaf)) {
    throw 'Python ontbreekt. Volg README.md of geef -PythonExecutable op.'
}
$scriptPath = Join-Path $projectRoot 'nutcracker_id.py'
if ($Help -or -not $Photos) {
    & $PythonExecutable -B $scriptPath --help
    if ($LASTEXITCODE -ne 0) { throw "Hulpstart mislukt: $LASTEXITCODE" }
    return
}
if (-not [IO.Path]::IsPathRooted($Photos)) {
    $Photos = Join-Path $projectRoot $Photos
}
if (-not $Output) { $Output = '.local-output\patronen' }
if (-not [IO.Path]::IsPathRooted($Output)) {
    $Output = Join-Path $projectRoot $Output
}
& $PythonExecutable -B $scriptPath --photos $Photos --output $Output
if ($LASTEXITCODE -ne 0) { throw "Verwerking mislukt: $LASTEXITCODE" }
Write-Host (Join-Path $Output 'index.html')
