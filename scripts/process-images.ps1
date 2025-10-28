# Script para procesar imágenes en diferentes tamaños y formatos
# Requiere: ImageMagick instalado (https://imagemagick.org/script/download.php#windows)

$sizes = @(
    @{width=400; suffix="-400"},
    @{width=800; suffix="-800"},
    @{width=1200; suffix=""}
)

$sourceDir = "..\media\images\products"
$formats = @("webp", "jpg")

# Asegurarse que estamos en el directorio correcto
Set-Location $PSScriptRoot

# Procesar cada imagen
Get-ChildItem -Path $sourceDir -Filter "*.webp" | ForEach-Object {
    $baseName = $_.BaseName
    
    foreach ($size in $sizes) {
        foreach ($format in $formats) {
            $outputName = "$sourceDir\$baseName$($size.suffix).$format"
            
            if (!(Test-Path $outputName)) {
                Write-Host "Procesando: $($_.Name) -> $outputName"
                
                # Convertir y redimensionar
                if ($format -eq "webp") {
                    magick convert $_.FullName -resize "$($size.width)x" -quality 85 $outputName
                } else {
                    magick convert $_.FullName -resize "$($size.width)x" -quality 85 $outputName
                }
            }
        }
    }
}

Write-Host "¡Proceso completado!"