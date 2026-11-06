param(
    [string]$Python = 'python',
    [string]$Pdftoppm = 'pdftoppm',
    [ValidateSet('poppler','pymupdf')][string]$Renderer = 'poppler'
)
$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
Push-Location $PSScriptRoot
try {
    & $Python scripts/build_full21.py --browser --output-dir output/v1.1-full21-windows --renderer $Renderer --pdftoppm $Pdftoppm
    if ($LASTEXITCODE -ne 0) { throw "Build failed (exit $LASTEXITCODE). Existing editions were not replaced." }
} finally { Pop-Location }
