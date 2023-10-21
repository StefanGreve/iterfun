[OutputType([void])]
param(
    [switch] $Clean,

    [switch] $Build
)

begin {
    $Module = python setup.py --name
    $Version = python setup.py --version
}

process {
    if ($Clean.IsPresent) {
        Write-Host "Purge build artifacts . . . " -ForegroundColor Yellow -NoNewline
        Remove-Item -Path ./dist -Recurse -ErrorAction SilentlyContinue
        git ls-ignored | Where-Object { $_ -like "src/*" } | Remove-Item -Recurse
        Write-Host "✓" -ForegroundColor Green
    }

    if ($Build.IsPresent) {
        Write-Host "[1/2] Build sdist and wheel" -ForegroundColor Yellow
        python -m build
        Write-Host "[2/2] Install Module" -ForegroundColor Yellow
        pip install "./dist/${Module}-${Version}-cp312-cp312-win_amd64.whl" --force-reinstall
    }
}
