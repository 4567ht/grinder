# build.ps1

# Build the project using Hatch
py -m hatch build

# Find the generated wheel(s) in dist/
$wheels = Get-ChildItem -Path dist -Filter *.whl

if ($wheels.Count -eq 0) {
    Write-Host "No wheel files found in dist/"
    exit 1
}

# Install each wheel
foreach ($wheel in $wheels) {
    Write-Host "Installing $($wheel.Name)..."
    py -m pip install --force-reinstall $wheel.FullName
}

Write-Host "✅ Build and install complete!"
