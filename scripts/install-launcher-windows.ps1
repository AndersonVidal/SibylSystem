$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir

$StartMenuDir = [System.IO.Path]::Combine(
    $env:APPDATA, "Microsoft", "Windows", "Start Menu", "Programs"
)
$ShortcutPath = [System.IO.Path]::Combine($StartMenuDir, "Sibyl.lnk")
$RunScript = [System.IO.Path]::Combine($ProjectDir, "scripts", "run.ps1")

Write-Host "Instalando launcher do Sibyl..."

$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "powershell.exe"
$Shortcut.Arguments = "-ExecutionPolicy Bypass -NoExit -File `"$RunScript`""
$Shortcut.WorkingDirectory = $ProjectDir
$Shortcut.Description = "Sistema pessoal de organizacao e acompanhamento de vida"
$Shortcut.Save()

Write-Host ""
Write-Host "Launcher instalado em: $ShortcutPath"
Write-Host ""
Write-Host "O Sibyl agora aparece no Menu Iniciar como 'Sibyl'."
Write-Host ""
Write-Host "Para remover o launcher:"
Write-Host "  Remove-Item '$ShortcutPath'"
Write-Host ""
Write-Host "Para reinstalar apos mover o projeto de diretorio:"
Write-Host "  .\scripts\install-launcher-windows.ps1"
