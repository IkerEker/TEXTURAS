# ==========================================================================================
#  BIBLIOTECA · montar la biblioteca común en este ordenador (Windows)
#  Se ejecuta con MONTAR_BIBLIOTECA.bat (doble clic). Se puede cerrar y volver a lanzar: retoma.
#  NO borra nada. AcidBite se MUEVE (mismo disco = instantáneo), no se copia.
# ==========================================================================================
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$Utf8 = New-Object Text.UTF8Encoding $false

$Raiz     = Join-Path $env:USERPROFILE 'Biblioteca'
$Acid     = Join-Path $env:USERPROFILE 'Downloads\ADIDBITE\BIBLIOTECA'
$Fuentes  = Join-Path $Raiz '_fuentes'
$RamaTx   = 'atlas'

try {
  Add-Type -Namespace Win -Name Power -MemberDefinition '[DllImport("kernel32.dll")] public static extern uint SetThreadExecutionState(uint f);'
  [Win.Power]::SetThreadExecutionState([uint32]2147483649) | Out-Null
} catch {}

New-Item -ItemType Directory -Force -Path $Raiz | Out-Null
$Log = Join-Path $Raiz '_ESTADO_MONTAJE.txt'
function Log([string]$m) {
  $line = '[{0}] {1}' -f (Get-Date -Format 'dd/MM HH:mm:ss'), $m
  Write-Host $line
  [IO.File]::AppendAllText($Log, $line + "`r`n", $Utf8)
}
Log "=== Montando la Biblioteca en $Raiz ==="

# ------------------------------------------------------------------ 1. git
function Find-Git {
  $g = Get-Command git -ErrorAction SilentlyContinue
  if ($g) { return $g.Source }
  foreach ($p in @("$env:ProgramFiles\Git\cmd\git.exe", "$env:LOCALAPPDATA\Programs\Git\cmd\git.exe")) { if (Test-Path $p) { return $p } }
  return $null
}
$Git = Find-Git
if (-not $Git) {
  Log 'Falta git. Lo instalo con winget (puede pedir permiso)...'
  winget install --id Git.Git -e --source winget --accept-package-agreements --accept-source-agreements
  $Git = Find-Git
  if (-not $Git) { Log 'ERROR: no se pudo instalar git. Instálalo desde https://git-scm.com y vuelve a lanzar.'; exit 1 }
}
Log "git: $Git"
function GitRun([string[]]$a) {
  $p = Start-Process -FilePath $Git -ArgumentList (@('-c', 'core.longpaths=true') + $a) -NoNewWindow -Wait -PassThru
  return $p.ExitCode
}
function Clonar($url, $dest, $rama) {
  if (Test-Path (Join-Path $dest '.git')) { Log "  ya está: $dest (actualizando)"; [void](GitRun @('-C', "`"$dest`"", 'pull', '--ff-only')); return }
  if (Test-Path $dest) { Log "  ERROR: $dest existe pero no es un clon. Revísalo."; return }
  Log "  clonando $url ($rama) -> $dest  (puede tardar)"
  $c = GitRun @('clone', '--depth', '1', '--branch', $rama, $url, "`"$dest`"")
  if ($c -ne 0) { Log "  ERROR al clonar $url (código $c)" }
}

# ------------------------------------------------------------------ 2. AcidBite (mover)
$AcidDest = Join-Path $Raiz 'ACIDBITE'
if (Test-Path $AcidDest) { Log 'AcidBite ya está en la Biblioteca.' }
elseif (Test-Path $Acid) {
  Log "Moviendo AcidBite: $Acid -> $AcidDest"
  Move-Item -LiteralPath $Acid -Destination $AcidDest
  [IO.File]::WriteAllText((Join-Path (Split-Path $Acid -Parent) '_RUTA_BIBLIOTECA.txt'),
    "La biblioteca de AcidBite se ha movido a:`r`n$AcidDest`r`n", $Utf8)
  Log '  movido.'
} else { Log "AVISO: no encuentro AcidBite en $Acid" }

# ------------------------------------------------------------------ 3. TEXTURAS (repo privado: pedirá iniciar sesión en GitHub)
Log 'TEXTURAS (si se abre el navegador, inicia sesión en GitHub con tu cuenta)'
Clonar 'https://github.com/IkerEker/TEXTURAS.git' (Join-Path $Raiz 'TEXTURAS') $RamaTx
$ManPath = Join-Path $Raiz 'TEXTURAS\originales\montaje.json'
if (-not (Test-Path $ManPath)) { Log 'ERROR: no está TEXTURAS\originales\montaje.json. Vuelve a lanzar.'; exit 1 }
$Man = [IO.File]::ReadAllText($ManPath, [Text.Encoding]::UTF8) | ConvertFrom-Json

# ------------------------------------------------------------------ 4. repos de los plugins (fuentes)
New-Item -ItemType Directory -Force -Path $Fuentes | Out-Null
foreach ($p in $Man.repos.PSObject.Properties) {
  Clonar ("https://github.com/{0}.git" -f $p.Value.repo) (Join-Path $Fuentes $p.Name) $p.Value.rama
}

# ------------------------------------------------------------------ 5. originales intactos (md5 comprobado)
function Md5($f) { (Get-FileHash -LiteralPath $f -Algorithm MD5).Hash.ToLower() }
$copiados = 0; $yaEstaban = 0; $faltan = New-Object Collections.ArrayList; $malos = New-Object Collections.ArrayList
$tareas = @($Man.tareas)
$n = 0; $total = $tareas.Count
Log "Originales: $total archivos"
foreach ($t in $tareas) {
  $n++
  if ($n % 200 -eq 0) { Log "  $n / $total" }
  $dst = Join-Path $Raiz ($t[0] -replace '/', '\')
  if ((Test-Path -LiteralPath $dst) -and ((Md5 $dst) -eq $t[1])) { $yaEstaban++; continue }
  $src = $null
  foreach ($r in $t[2]) { $c = Join-Path $Fuentes ($r -replace '/', '\'); if (Test-Path -LiteralPath $c) { $src = $c; break } }
  if (-not $src) { [void]$faltan.Add($t[0]); continue }
  if ((Md5 $src) -ne $t[1]) { [void]$malos.Add($src); continue }
  New-Item -ItemType Directory -Force -Path (Split-Path $dst -Parent) | Out-Null
  Copy-Item -LiteralPath $src -Destination $dst -Force
  $copiados++
}
# catálogos de NEONIZADOR (los usa su build_texpack)
$nb = Join-Path $Fuentes 'neonizador_bt\BIBLIOTECA\elementos'
if (Test-Path $nb) {
  Get-ChildItem -LiteralPath $nb -Recurse -Filter *.json | ForEach-Object {
    $rel = $_.FullName.Substring((Join-Path $Fuentes 'neonizador_bt').Length + 1)
    $d = Join-Path $Raiz ('originales\heredado\neonizador\' + $rel)
    New-Item -ItemType Directory -Force -Path (Split-Path $d -Parent) | Out-Null
    Copy-Item -LiteralPath $_.FullName -Destination $d -Force
  }
}
New-Item -ItemType Directory -Force -Path (Join-Path $Raiz 'generadas') | Out-Null

# ------------------------------------------------------------------ 6. comprobar AcidBite contra su inventario
$faltaAcid = 0
$inv = Join-Path $Raiz 'TEXTURAS\acidbite\datos\inventario.csv'
if ((Test-Path $AcidDest) -and (Test-Path $inv)) {
  Import-Csv -LiteralPath $inv -Encoding UTF8 | ForEach-Object {
    if (-not (Test-Path -LiteralPath (Join-Path $AcidDest $_.ruta))) { $faltaAcid++ }
  }
}

# ------------------------------------------------------------------ 7. resumen
Log ("RESUMEN: originales copiados {0} · ya estaban {1} · faltan {2} · md5 distinto {3} · AcidBite faltan {4}" -f `
     $copiados, $yaEstaban, $faltan.Count, $malos.Count, $faltaAcid)
foreach ($f in $faltan | Select-Object -First 20) { Log "  falta: $f" }
foreach ($f in $malos | Select-Object -First 20) { Log "  md5 distinto: $f" }
$estado = [ordered]@{ raiz = $Raiz; copiados = $copiados; ya_estaban = $yaEstaban; faltan = @($faltan); md5_distinto = @($malos); acidbite_faltan = $faltaAcid }
[IO.File]::WriteAllText((Join-Path $Raiz 'ESTADO_BIBLIOTECA.json'), ($estado | ConvertTo-Json -Depth 4), $Utf8)
[Environment]::SetEnvironmentVariable('TEXTURAS_ROOT', $Raiz, 'User')
Log "Variable TEXTURAS_ROOT = $Raiz (para tu usuario)"
if ($faltan.Count -eq 0 -and $malos.Count -eq 0 -and $faltaAcid -eq 0) { Log 'LISTO: la Biblioteca está completa.' }
else { Log 'TERMINADO CON AVISOS: díselo a Claude.' }
