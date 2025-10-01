# PowerShell helper to build a single-file EXE using PyInstaller
# Usage: Open PowerShell, navigate to this repo root, then run: .\build_exe.ps1

param(
    [string]$EntryScript = "design_renamer_gui.py",
    [string]$Name = "DesignRenamer",
    [string]$Version = "0.1.0"
)

# Ensure Python and PyInstaller are available
python -c "import sys; print(sys.executable)"; if ($LASTEXITCODE -ne 0) { Write-Error 'Python not found in PATH'; exit 1 }
python -c "import PyInstaller" 2>$null; if ($LASTEXITCODE -ne 0) {
    Write-Host 'PyInstaller not found — installing from requirements.txt...'
    python -m pip install -r requirements.txt
}

# Build with PyInstaller: one-file, windowed (no console), add version in the name
pyinstaller --onefile --noconsole --name "$Name-v$Version" $EntryScript

Write-Host "Build finished. See the dist folder for the EXE: dist\$Name-v$Version.exe"
