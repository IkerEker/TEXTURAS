# ==========================================================================================
#  ACIDBITE · descomprimir, ordenar y analizar
#  Se ejecuta con ORGANIZAR_ACIDBITE.bat (doble clic). Se puede parar y volver a lanzar:
#  retoma donde lo dejó. NO borra ni modifica los .zip originales.
# ==========================================================================================
$ErrorActionPreference = 'Stop'
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$Utf8 = New-Object Text.UTF8Encoding $false

# Que el PC no se duerma mientras trabaja
try {
  Add-Type -Namespace Win -Name Power -MemberDefinition '[DllImport("kernel32.dll")] public static extern uint SetThreadExecutionState(uint f);'
  [Win.Power]::SetThreadExecutionState([uint32]2147483649) | Out-Null
} catch {}

$Log = Join-Path $Here '_ESTADO.txt'
function Log([string]$m) {
  $line = '[{0}] {1}' -f (Get-Date -Format 'dd/MM HH:mm:ss'), $m
  Write-Host $line
  [IO.File]::AppendAllText($Log, $line + "`r`n", $Utf8)
}

# ------------------------------------------------------------------ categorías por pack
$Map = @{
  '16mm_Package_4K'                       = @('02_PELICULA', '16mm Package')
  '35mm_Package_4K'                       = @('02_PELICULA', '35mm Package')
  'Super_8_Package_4K'                    = @('02_PELICULA', 'Super 8 Package')
  'Film_Burns_4K'                         = @('02_PELICULA', 'Film Burns')
  'Film_Leaks_4K'                         = @('02_PELICULA', 'Film Leaks')
  'Viewfinders+_4K'                       = @('02_PELICULA', 'Viewfinders Plus')
  'Burning_Paper_Transitions_4K'          = @('01_TRANSICIONES', 'Burning Paper Transitions')
  'Cine_Snip_Transitions_4K'              = @('01_TRANSICIONES', 'Cine Snip Transitions')
  'Cracked_Glass_Transitions_4K'          = @('01_TRANSICIONES', 'Cracked Glass Transitions')
  'Cyber_Transitions_4K'                  = @('01_TRANSICIONES', 'Cyber Transitions')
  'Light_Transitions_4K'                  = @('01_TRANSICIONES', 'Light Transitions')
  'Wipe_&_Light_Transitions_4K'           = @('01_TRANSICIONES', 'Wipe and Light Transitions')
  'Pre-Built_VHS_Transitions_Standard'    = @('01_TRANSICIONES', 'Pre-Built VHS Transitions')
  'Punch_Hole_Transitions_Standard'       = @('01_TRANSICIONES', 'Punch Hole Transitions')
  'Textile_Transitions_Standard'          = @('01_TRANSICIONES', 'Textile Transitions')
  'Tunnel_Transitions_4K'                 = @('01_TRANSICIONES', 'Tunnel Transitions')
  'Dissected_Textures_4K'                 = @('03_TEXTURAS_OVERLAYS', 'Dissected Textures')
  'CRT_Elements_4K'                       = @('03_TEXTURAS_OVERLAYS', 'CRT Elements')
  'Analog_Video_Package_Standard'         = @('03_TEXTURAS_OVERLAYS', 'Analog Video Package')
  'Optical_Elements_4K'                   = @('03_TEXTURAS_OVERLAYS', 'Optical Elements')
  'DynamiXXX_4K'                          = @('03_TEXTURAS_OVERLAYS', 'DynamiXXX')
  'Super_Mixed_Media_Pack_4K_SMMP_Assets' = @('04_COLLAGE_MIXED_MEDIA', 'Super Mixed Media Pack')
  'Ultimate_Paper_Pack_4K_Assets'         = @('04_COLLAGE_MIXED_MEDIA', 'Ultimate Paper Pack')
  'Abstracts_4K'                          = @('05_ANIMACIONES_ELEMENTOS', 'Abstracts')
  'Liquids_4K'                            = @('05_ANIMACIONES_ELEMENTOS', 'Liquids')
  'Animated_Markers_4K'                   = @('05_ANIMACIONES_ELEMENTOS', 'Animated Markers')
  'Cinemarkers_4K'                        = @('05_ANIMACIONES_ELEMENTOS', 'Cinemarkers')
  'Cinemarkers_2_4K'                      = @('05_ANIMACIONES_ELEMENTOS', 'Cinemarkers 2')
  'Morpheus_Standard'                     = @('06_PLANTILLAS', 'Morpheus')
  'Dystopia_SFX_Standard'                 = @('07_SONIDO', 'Dystopia SFX')
  'Elements_SFX_Standard'                 = @('07_SONIDO', 'Elements SFX')
  'Urban_SFX_Standard'                    = @('07_SONIDO', 'Urban SFX')
}

Log '=========== ACIDBITE: inicio ==========='
$Zips = @(Get-ChildItem -LiteralPath $Here -Filter '*.zip' -File | Sort-Object Name)
Log ("Zips encontrados: {0}" -f $Zips.Count)

# ------------------------------------------------------------------ espacio en disco
$Root = Join-Path $Here 'BIBLIOTECA'
$need = [int64]0
foreach ($f in $Zips) {
  $z = [IO.Compression.ZipFile]::OpenRead($f.FullName)
  try { foreach ($e in $z.Entries) { $need += $e.Length } } finally { $z.Dispose() }
}
$needGB = [math]::Round($need / 1GB, 1)
$drive = New-Object IO.DriveInfo ([IO.Path]::GetPathRoot($Here))
$freeGB = [math]::Round($drive.AvailableFreeSpace / 1GB, 1)
# lo que ya esté descomprimido no cuenta
$doneBytes = [int64]0
if (Test-Path -LiteralPath $Root) {
  $doneBytes = (Get-ChildItem -LiteralPath $Root -Recurse -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
  if (-not $doneBytes) { $doneBytes = 0 }
}
$pending = $need - $doneBytes + 8GB
Log ("Descomprimido ocupa {0} GB. Libre en {1}: {2} GB. Falta por escribir aprox. {3} GB" -f $needGB, $drive.Name, $freeGB, [math]::Round($pending/1GB,1))

if ($drive.AvailableFreeSpace -lt $pending) {
  Log 'NO HAY ESPACIO SUFICIENTE en este disco.'
  Write-Host ''
  Write-Host 'Discos disponibles:'
  [IO.DriveInfo]::GetDrives() | Where-Object { $_.IsReady -and $_.DriveType -in 'Fixed','Removable','Network' } |
    ForEach-Object { Write-Host ('  {0}  libre: {1} GB' -f $_.Name, [math]::Round($_.AvailableFreeSpace/1GB,1)) }
  Write-Host ''
  $alt = Read-Host 'Escribe la LETRA de otro disco con espacio (por ejemplo D) o pulsa Enter para salir'
  if (-not $alt) { Log 'Cancelado por falta de espacio.'; exit 1 }
  $Root = ($alt.Trim().TrimEnd(':','\') + ':\ACIDBITE_BIBLIOTECA')
  $drive = New-Object IO.DriveInfo ([IO.Path]::GetPathRoot($Root))
  if ($drive.AvailableFreeSpace -lt ($need + 8GB)) { Log "Tampoco hay espacio en $Root. Cancelado."; exit 1 }
}
Log "Biblioteca en: $Root"
$Ana = Join-Path $Root '_ANALISIS'
foreach ($d in @($Root, $Ana, "$Ana\estado", "$Ana\probe", "$Ana\stats", "$Ana\sheets", "$Ana\audio", "$Ana\docs")) {
  [IO.Directory]::CreateDirectory($d) | Out-Null
}
[IO.File]::WriteAllText((Join-Path $Here '_RUTA_BIBLIOTECA.txt'), $Root, $Utf8)

# ------------------------------------------------------------------ 1. descomprimir
function Expand-Pack([string]$zipPath, [string]$dest) {
  $errs = 0
  $z = [IO.Compression.ZipFile]::OpenRead($zipPath)
  try {
    $entries = @($z.Entries | Where-Object {
      $fn = ([string]$_.FullName) -replace '\\', '/'; $nm = [string]$_.Name
      $fn -and ($fn -notmatch '(^|/)__MACOSX/') -and ($nm -ne '.DS_Store') -and -not $nm.StartsWith('._') })
    # si todo cuelga de una sola carpeta, se quita ese nivel
    $strip = ''
    $tops = @($entries | ForEach-Object { ((([string]$_.FullName) -replace '\\', '/') -split '/')[0] } | Select-Object -Unique)
    if ($tops.Count -eq 1) {
      $pre = $tops[0] + '/'
      if (@($entries | Where-Object { -not ((([string]$_.FullName) -replace '\\', '/').StartsWith($pre)) }).Count -eq 0) { $strip = $pre }
    }
    $destFull = [IO.Path]::GetFullPath($dest)
    $n = $entries.Count; $i = 0
    if ($n -eq 0) { throw 'sin entradas legibles' }
    foreach ($e in $entries) {
      $i++
      $rel = ([string]$e.FullName) -replace '\\', '/'
      if ($strip -and $rel.StartsWith($strip)) { $rel = $rel.Substring($strip.Length) }
      if ([string]::IsNullOrEmpty($rel)) { continue }
      $target = [IO.Path]::GetFullPath((Join-Path $dest ($rel -replace '/', '\')))
      if (-not $target.StartsWith($destFull)) { $errs++; continue }
      if ($i % 10 -eq 0) { Write-Progress -Activity "Descomprimiendo $(Split-Path $zipPath -Leaf)" -Status "$i / $n" -PercentComplete ([int](100 * $i / [math]::Max($n,1))) }
      try {
        if ($rel.EndsWith('/') -or [string]::IsNullOrEmpty([string]$e.Name)) { [IO.Directory]::CreateDirectory($target) | Out-Null; continue }
        [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($target)) | Out-Null
        if ((Test-Path -LiteralPath $target) -and ((Get-Item -LiteralPath $target).Length -eq $e.Length)) { continue }
        [IO.Compression.ZipFileExtensions]::ExtractToFile($e, $target, $true)
      } catch {
        $errs++
        Log ("   ERROR en {0}: {1}" -f $e.FullName, $_.Exception.Message)
      }
    }
    Write-Progress -Activity 'Descomprimiendo' -Completed
  } finally { $z.Dispose() }
  return $errs
}

function Expand-WithTar([string]$zipPath, [string]$dest) {
  [IO.Directory]::CreateDirectory($dest) | Out-Null
  & "$env:SystemRoot\System32\tar.exe" -xf $zipPath -C $dest --exclude '__MACOSX' --exclude '*.DS_Store' --exclude '._*'
  $code = $LASTEXITCODE
  # si todo quedó dentro de una sola carpeta, se sube un nivel
  $items = @(Get-ChildItem -LiteralPath $dest -Force)
  if ($items.Count -eq 1 -and $items[0].PSIsContainer) {
    $inner = $items[0].FullName
    Get-ChildItem -LiteralPath $inner -Force | ForEach-Object { Move-Item -LiteralPath $_.FullName -Destination $dest -Force }
    Remove-Item -LiteralPath $inner -Force -Recurse -ErrorAction SilentlyContinue
  }
  return $code
}

function Pack-Has-Files([string]$dest) {
  if (-not (Test-Path -LiteralPath $dest)) { return $false }
  return [bool](Get-ChildItem -LiteralPath $dest -Recurse -File -ErrorAction SilentlyContinue | Select-Object -First 1)
}

$k = 0
foreach ($f in $Zips) {
  $k++
  $base = [IO.Path]::GetFileNameWithoutExtension($f.Name)
  $marker = Join-Path "$Ana\estado" ($base + '.ok')
  if ($Map.ContainsKey($base)) { $cat = $Map[$base][0]; $nice = $Map[$base][1] } else { $cat = '99_OTROS'; $nice = $base }
  $dest = Join-Path (Join-Path $Root $cat) $nice
  if ((Test-Path -LiteralPath $marker) -and (Pack-Has-Files $dest)) { Log ("[{0}/{1}] Ya descomprimido: {2}" -f $k, $Zips.Count, $base); continue }
  Log ("[{0}/{1}] Descomprimiendo {2}  ->  {3}\{4}" -f $k, $Zips.Count, $f.Name, $cat, $nice)
  try { $errs = Expand-Pack $f.FullName $dest } catch {
    Log ("   .NET no puede leer este zip ({0}); se usa tar de Windows" -f $_.Exception.Message)
    try { $code = Expand-WithTar $f.FullName $dest; $errs = $(if ($code -eq 0) { 0 } else { 1 }) } catch { $errs = 1; Log ("   ERROR con tar: {0}" -f $_.Exception.Message) }
  }
  if (-not (Pack-Has-Files $dest)) { $errs = [math]::Max($errs, 1); Log '   La carpeta del pack ha quedado vacia' }
  if ($errs -eq 0) { [IO.File]::WriteAllText($marker, (Get-Date).ToString('s'), $Utf8); Log '   OK' }
  else { Log ("   Terminado con {0} errores (se reintentará en la próxima ejecución)" -f $errs) }
}

# ------------------------------------------------------------------ 2. inventario
Log 'Haciendo inventario...'
$ext = @{
  video = 'mov','mp4','m4v','mxf','avi','webm','mkv'
  imagen = 'png','jpg','jpeg','tif','tiff','exr','psd','dpx','bmp','gif'
  audio = 'wav','aif','aiff','mp3','flac','m4a','ogg'
  lut = 'cube','3dl','look','csp'
  plantilla = 'mogrt','prproj','drp','drfx','setting','moti','motn','motr','moef','aep','aet','xml','ffx','prfpset','drt','fcpxml','prtl'
  doc = 'pdf','txt','rtf','html','htm','url','webloc','md'
}
function TypeOf([string]$e) { foreach ($t in $ext.Keys) { if ($ext[$t] -contains $e) { return $t } }; return 'otro' }

$rootFull = [IO.Path]::GetFullPath($Root).TrimEnd('\') + '\'
$files = @(Get-ChildItem -LiteralPath $Root -Recurse -File | Where-Object { -not $_.FullName.StartsWith($Ana) } |
  ForEach-Object { $_.FullName.Substring($rootFull.Length) } | Sort-Object)
$inv = New-Object System.Collections.Generic.List[object]
$md5 = [Security.Cryptography.MD5]::Create()
foreach ($rel in $files) {
  $id = ([BitConverter]::ToString($md5.ComputeHash([Text.Encoding]::UTF8.GetBytes($rel.ToLowerInvariant())))).Replace('-', '').Substring(0, 12).ToLower()
  $parts = $rel -split '\\'
  $e = [IO.Path]::GetExtension($rel).TrimStart('.').ToLower()
  $inv.Add([pscustomobject]@{
    id = $id; categoria = $parts[0]; pack = $(if ($parts.Count -gt 1) { $parts[1] } else { '' })
    ruta = $rel; tipo = (TypeOf $e); ext = $e; bytes = (Get-Item -LiteralPath (Join-Path $Root $rel)).Length
  })
}
$inv | Export-Csv -LiteralPath "$Ana\inventario.csv" -NoTypeInformation -Encoding UTF8
Copy-Item -LiteralPath "$Ana\inventario.csv" -Destination (Join-Path $Here '_INVENTARIO.csv') -Force
$inv | Group-Object tipo | ForEach-Object { Log ("   {0}: {1}" -f $_.Name, $_.Count) }

# ------------------------------------------------------------------ 3. ffmpeg
function Find-Tool([string]$name) {
  $c = Get-Command $name -ErrorAction SilentlyContinue
  if ($c) { return $c.Source }
  foreach ($p in @("$env:LOCALAPPDATA\Microsoft\WinGet\Links\$name.exe", "C:\ffmpeg\bin\$name.exe", "$env:ProgramFiles\ffmpeg\bin\$name.exe")) {
    if (Test-Path -LiteralPath $p) { return $p }
  }
  $g = Get-ChildItem "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" -Recurse -Filter "$name.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($g) { return $g.FullName }
  return $null
}
$ffmpeg = Find-Tool 'ffmpeg'; $ffprobe = Find-Tool 'ffprobe'
if (-not $ffmpeg -or -not $ffprobe) {
  Write-Host ''
  Write-Host 'Para analizar los clips hace falta ffmpeg (gratuito) y no lo encuentro en este PC.'
  $r = Read-Host 'Lo instalo con winget? (s/n)'
  if ($r -match '^[sSyY]') {
    try { winget install --id Gyan.FFmpeg -e --accept-source-agreements --accept-package-agreements } catch { Log 'No se pudo usar winget.' }
    $ffmpeg = Find-Tool 'ffmpeg'; $ffprobe = Find-Tool 'ffprobe'
  }
}
if (-not $ffmpeg -or -not $ffprobe) {
  Log 'SIN ffmpeg: la biblioteca queda descomprimida y ordenada, pero sin analisis. Instala ffmpeg y vuelve a lanzar el .bat.'
  exit 0
}
Log "ffmpeg: $ffmpeg"

# ------------------------------------------------------------------ 4. análisis
function Run([string[]]$a) { & $ffmpeg -hide_banner -nostdin -v error @a | Out-Null }

$work = @($inv | Where-Object { $_.tipo -in 'video','imagen','audio','doc' })
$total = $work.Count; $i = 0
$t0 = Get-Date
foreach ($it in $work) {
  $i++
  $path = Join-Path $Root $it.ruta
  $idn = $it.id
  if ($i % 5 -eq 0) {
    $el = ((Get-Date) - $t0).TotalMinutes
    $eta = if ($i -gt 0) { [math]::Round($el / $i * ($total - $i)) } else { 0 }
    Write-Progress -Activity 'Analizando clips' -Status "$i / $total  (quedan ~$eta min)" -PercentComplete ([int](100 * $i / $total))
  }
  try {
    if ($it.tipo -eq 'doc') {
      if ($it.bytes -lt 20MB) { Copy-Item -LiteralPath $path -Destination ("$Ana\docs\{0}_{1}" -f $idn, [IO.Path]::GetFileName($path)) -Force }
      continue
    }
    # probe
    $pj = "$Ana\probe\$idn.json"
    if (-not (Test-Path -LiteralPath $pj)) {
      $out = & $ffprobe -v error -show_format -show_streams -of json -i $path
      [IO.File]::WriteAllText($pj, ($out -join "`n"), $Utf8)
    }
    $p = (Get-Content -LiteralPath $pj -Raw -Encoding UTF8) | ConvertFrom-Json
    $vs = @($p.streams | Where-Object { $_.codec_type -eq 'video' -and $_.disposition.attached_pic -ne 1 }) | Select-Object -First 1
    $as = @($p.streams | Where-Object { $_.codec_type -eq 'audio' }) | Select-Object -First 1
    $dur = 0.0; if ($p.format.duration) { $dur = [double]::Parse($p.format.duration, [Globalization.CultureInfo]::InvariantCulture) }

    Push-Location "$Ana\stats"; [Environment]::CurrentDirectory = (Get-Location).Path
    try {
      if ($vs) {
        $w = [int]$vs.width; $h = [int]$vs.height
        $alpha = ($vs.pix_fmt -match '^(yuva|rgba|argb|bgra|abgr|gbrap|ya|pal8)')
        $isStill = ($it.tipo -eq 'imagen') -or ($dur -lt 0.2)
        $skipStats = $isStill -or ($it.ruta -match '(?i)tutorial|teaser|preview|promo')
        # 4a. luminancia, movimiento y alfa por fotograma
        if (-not $skipStats -and -not (Test-Path -LiteralPath "${idn}_Y.txt")) {
          if ($alpha) {
            $fc = "[0:v]scale=480:-2,format=yuva444p,split=3[s1][s2][s3];" +
                  "[s1]format=yuv444p,signalstats,metadata=mode=print:key=lavfi.signalstats.YAVG:file=${idn}_Y.tmp[o1];" +
                  "[s2]format=yuv444p,tblend=all_mode=difference,signalstats,metadata=mode=print:key=lavfi.signalstats.YAVG:file=${idn}_D.txt[o2];" +
                  "[s3]alphaextract,signalstats,metadata=mode=print:key=lavfi.signalstats.YAVG:file=${idn}_A.txt[o3]"
            Run @('-i', $path, '-filter_complex', $fc, '-map', '[o1]', '-f', 'null', '-', '-map', '[o2]', '-f', 'null', '-', '-map', '[o3]', '-f', 'null', '-')
          } else {
            $fc = "[0:v]scale=480:-2,format=yuv444p,split=2[s1][s2];" +
                  "[s1]signalstats,metadata=mode=print:key=lavfi.signalstats.YAVG:file=${idn}_Y.tmp[o1];" +
                  "[s2]tblend=all_mode=difference,signalstats,metadata=mode=print:key=lavfi.signalstats.YAVG:file=${idn}_D.txt[o2]"
            Run @('-i', $path, '-filter_complex', $fc, '-map', '[o1]', '-f', 'null', '-', '-map', '[o2]', '-f', 'null', '-')
          }
          if (Test-Path -LiteralPath "${idn}_Y.tmp") { Move-Item -LiteralPath "${idn}_Y.tmp" -Destination "${idn}_Y.txt" -Force }
        }
        # 4b. hoja de miniaturas (8 fotogramas; 1 si es imagen fija)
        $sheet = "$Ana\sheets\$idn.jpg"
        if (-not (Test-Path -LiteralPath $sheet)) {
          $tw = 240; $th = [int]([math]::Round($tw * $h / [math]::Max($w,1) / 2) * 2); if ($th -lt 2) { $th = 136 }
          $nf = if ($isStill) { 1 } else { 8 }
          $a = @(); $fc = ''
          for ($j = 0; $j -lt $nf; $j++) {
            if ($nf -gt 1) { $t = $dur * ($j + 0.5) / $nf; $a += @('-ss', $t.ToString('0.###', [Globalization.CultureInfo]::InvariantCulture), '-t', '1') }
            $a += @('-i', $path)
            if ($alpha) {
              $fc += "[${j}:v]scale=${tw}:${th},format=yuva444p,split[f$j][g$j];[f$j]drawbox=c=0x7f7f7f:t=fill,format=yuv444p[b$j];[b$j][g$j]overlay=format=auto,format=yuv420p[v$j];"
            } else {
              $fc += "[${j}:v]scale=${tw}:${th},format=yuv420p[v$j];"
            }
          }
          if ($nf -gt 1) {
            $fc += "[v0][v1][v2][v3]hstack=inputs=4[r1];[v4][v5][v6][v7]hstack=inputs=4[r2];[r1][r2]vstack=inputs=2,scale=out_range=full,format=yuvj420p[out]"
          } else { $fc += "[v0]scale=out_range=full,format=yuvj420p[out]" }
          Run ($a + @('-filter_complex', $fc, '-map', '[out]', '-frames:v', '1', '-q:v', '5', '-strict', 'unofficial', $sheet))
        }
      }
      # 4c. envolvente de audio (pico cada 10 ms)
      if ($as -and -not $vs -and -not (Test-Path -LiteralPath "$Ana\audio\${idn}_E.txt")) {
        Push-Location "$Ana\audio"; [Environment]::CurrentDirectory = (Get-Location).Path
        try {
          $af = "aformat=channel_layouts=mono,asetnsamples=n=480:p=0,astats=metadata=1:reset=1,ametadata=mode=print:key=lavfi.astats.Overall.Peak_level:file=${idn}_E.tmp"
          Run @('-i', $path, '-af', $af, '-f', 'null', '-')
          if (Test-Path -LiteralPath "${idn}_E.tmp") { Move-Item -LiteralPath "${idn}_E.tmp" -Destination "${idn}_E.txt" -Force }
        } finally { Pop-Location }
      }
    } finally { Pop-Location; [Environment]::CurrentDirectory = $Here }
  } catch {
    Log ("   aviso analizando {0}: {1}" -f $it.ruta, $_.Exception.Message)
  }
}
Write-Progress -Activity 'Analizando clips' -Completed
Log ("Analisis terminado en {0} min" -f [math]::Round(((Get-Date) - $t0).TotalMinutes))

# ------------------------------------------------------------------ 5. empaquetar el análisis para Claude
Log 'Empaquetando el analisis...'
Get-ChildItem -LiteralPath $Here -Filter '_ANALISIS_parte*.zip' -File | Remove-Item -Force
$limit = 350MB; $part = 0; $zip = $null; $fs = $null
$anaFull = [IO.Path]::GetFullPath($Ana).TrimEnd('\') + '\'
foreach ($f in (Get-ChildItem -LiteralPath $Ana -Recurse -File | Where-Object { $_.Name -notlike '*.tmp' })) {
  if ($zip -eq $null -or $fs.Length -gt $limit) {
    if ($zip) { $zip.Dispose(); $fs.Dispose() }
    $part++
    $fs = [IO.File]::Open((Join-Path $Here ("_ANALISIS_parte{0}.zip" -f $part)), 'Create')
    $zip = New-Object IO.Compression.ZipArchive($fs, [IO.Compression.ZipArchiveMode]::Create)
  }
  $name = $f.FullName.Substring($anaFull.Length) -replace '\\', '/'
  [void][IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $f.FullName, $name, [IO.Compression.CompressionLevel]::Optimal)
  $fs.Flush()
}
if ($zip) { $zip.Dispose(); $fs.Dispose() }
Log ("LISTO. Analisis en {0} parte(s): _ANALISIS_parte*.zip. Avisa a Claude." -f $part)
