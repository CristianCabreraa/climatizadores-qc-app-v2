$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

Add-Type -AssemblyName System.IO.Compression.FileSystem

$baseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $baseDir) {
    $baseDir = "C:\Users\GreenAir\Desktop\APP ELECTRICIDAD\climatizadores-qc-app"
}

$workDir = "$baseDir\apk_workdir"
$unsignedApk = "$baseDir\app-unsigned.apk"
$outDir = "$baseDir\out_apk"
$finalApk = "$baseDir\GreenAir-QC-v2.apk"
$javaExe = "C:\Program Files\Java\jre1.8.0_441\bin\java.exe"
$signerJar = "$baseDir\uber-apk-signer.jar"

Write-Output "========================================================"
Write-Output " [INICIO] COMPILANDO APK ANDROID v2 - GREENAIR QC"
Write-Output "========================================================"

# 1. Limpiar directorios previos
if (Test-Path $workDir) { Remove-Item -Recurse -Force $workDir }
if (Test-Path $outDir) { Remove-Item -Recurse -Force $outDir }
if (Test-Path $unsignedApk) { Remove-Item -Force $unsignedApk }

# 2. Descomprimir plantilla APK base con .NET ZipFile
Write-Output "[1/5] Extrayendo estructura base Capacitor Android..."
[System.IO.Compression.ZipFile]::ExtractToDirectory("$baseDir\temp_base.apk", $workDir)

# 3. Limpiar e inyectar codigo web en assets/public
Write-Output "[2/5] Inyectando codigo y vistas de la aplicacion V2..."
$targetPublic = "$workDir\assets\public"
if (Test-Path $targetPublic) {
    Remove-Item -Recurse -Force "$targetPublic\*"
} else {
    New-Item -ItemType Directory -Force -Path $targetPublic | Out-Null
}

# 4. Copiar los archivos de la app actualizada
Copy-Item "$baseDir\index.html" -Destination $targetPublic -Force
Copy-Item "$baseDir\manifest.json" -Destination $targetPublic -Force
Copy-Item "$baseDir\sw.js" -Destination $targetPublic -Force
Copy-Item "$baseDir\css" -Destination $targetPublic -Recurse -Force
Copy-Item "$baseDir\js" -Destination $targetPublic -Recurse -Force
Copy-Item "$baseDir\assets" -Destination $targetPublic -Recurse -Force

# Eliminar firma previa META-INF para firma limpia
if (Test-Path "$workDir\META-INF") {
    Remove-Item -Recurse -Force "$workDir\META-INF"
}

# 5. Reempaquetar a archivo ZIP / APK
Write-Output "[3/5] Empaquetando nuevo contenedor APK..."
$zipPath = "$baseDir\app-unsigned.zip"
if (Test-Path $zipPath) { Remove-Item -Force $zipPath }

[System.IO.Compression.ZipFile]::CreateFromDirectory($workDir, $zipPath)
Rename-Item $zipPath $unsignedApk -Force

# 6. Alinear y Firmar con uber-apk-signer
Write-Output "[4/5] Firmando APK con esquemas v1, v2 y v3 para Android 5.0 a 15..."
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$signOutput = & $javaExe -jar $signerJar -a $unsignedApk --allowResign -o $outDir --verbose
$signOutput | ForEach-Object { Write-Output $_ }

# 7. Obtener APK final firmado
$signedFiles = Get-ChildItem "$outDir\*.apk"
if ($signedFiles.Count -gt 0) {
    Copy-Item $signedFiles[0].FullName -Destination $finalApk -Force
    $sizeMb = [Math]::Round((Get-Item $finalApk).Length / 1MB, 2)
    Write-Output "[5/5] ¡EXITO! Archivo APK V2 compilado y firmado correctamente:"
    Write-Output "      Nombre:     GreenAir-QC-v2.apk"
    Write-Output "      Tamano:     $sizeMb MB"
    Write-Output "      Ruta:       $finalApk"
} else {
    Write-Error "No se genero el archivo APK firmado en $outDir"
}

# 8. Limpiar temporales de compilacion
Remove-Item -Recurse -Force $workDir -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force $outDir -ErrorAction SilentlyContinue
Remove-Item -Force $unsignedApk -ErrorAction SilentlyContinue

Write-Output "========================================================"
Write-Output " LISTO PARA INSTALAR EN TU CELULAR ANDROID"
Write-Output "========================================================"
