.\.venv\Scripts\activate
Write-Host "Directory of .venv activation: $(Get-Location)"
Set-Location -Path ".\src_graph_approach\"
Write-Host "Directory of code and dependency installation: $(Get-Location)"
pip install -e .
jupyter notebook
Write-Host "Jupyter notebook is running"