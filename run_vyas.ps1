Set-Location -LiteralPath $PSScriptRoot

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "   Starting VYAS Vedic Astrology Platform...      " -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Cyan

$VenvPython = ""
if (Test-Path "$PSScriptRoot\.venv311\Scripts\python.exe") {
    $VenvPython = "$PSScriptRoot\.venv311\Scripts\python.exe"
    Write-Host "[OK] Using Python Environment: .venv311" -ForegroundColor Yellow
} elseif (Test-Path "$PSScriptRoot\.venv\Scripts\python.exe") {
    $VenvPython = "$PSScriptRoot\.venv\Scripts\python.exe"
    Write-Host "[OK] Using Python Environment: .venv" -ForegroundColor Yellow
} else {
    $VenvPython = "python"
    Write-Host "[INFO] Virtual environment not found, using system python" -ForegroundColor White
}

Write-Host "`nStarting Streamlit server on http://localhost:8501..." -ForegroundColor Cyan
& $VenvPython -m streamlit run app.py --server.port 8501
