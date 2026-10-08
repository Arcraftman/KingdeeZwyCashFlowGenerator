$ErrorActionPreference = 'Stop'
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$python = Join-Path $projectRoot '.weiyu\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) {
    throw 'Python environment missing. Create .weiyu and install the project first.'
}

& $python -m compileall -q (Join-Path $projectRoot 'KingdeeZwyCashFlowGenerator') (Join-Path $projectRoot 'scripts')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$env:PYTHONPATH = $projectRoot
& $python -c 'from KingdeeZwyCashFlowGenerator import cli; from KingdeeZwyCashFlowGenerator.app import desktop; from KingdeeZwyCashFlowGenerator.core import generator; from KingdeeZwyCashFlowGenerator.ledger import loader; from KingdeeZwyCashFlowGenerator.reporting import template_builder; print("Python imports OK")'
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& $python -m ruff --version *> $null
if ($LASTEXITCODE -eq 0) {
    & $python -m ruff check --select E4,E9 (Join-Path $projectRoot 'KingdeeZwyCashFlowGenerator')
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

Write-Output 'Static checks passed.'
exit 0
