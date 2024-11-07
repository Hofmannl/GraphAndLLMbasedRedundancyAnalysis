.\.venv\Scripts\activate
Write-Host "Directory of .venv activation: $(Get-Location)"
Set-Location -Path ".\src_gpt_approach\"
Write-Host "Directory of code and dependency installation and the root for the jupzter notebook: $(Get-Location)"
pip install -e .
jupyter notebook
Write-Host "Jupyter notebook is running"