@echo off
chcp 65001 >nul
title BIBLIOTECA - actualizar TEXTURAS
set G=git
where git >nul 2>nul || set G="%ProgramFiles%\Git\cmd\git.exe"
set L="%~dp0_ESTADO_ACTUALIZAR.txt"
echo === %date% %time% === > %L%
echo Actualizando TEXTURAS (si se abre el navegador, inicia sesion en GitHub)...
%G% -C "%~dp0TEXTURAS" status --short >> %L% 2>&1
%G% -C "%~dp0TEXTURAS" pull --ff-only >> %L% 2>&1
%G% -C "%~dp0TEXTURAS" log --oneline -1 >> %L% 2>&1
python "%~dp0TEXTURAS\tools\atlas\buscar.py" --version >> %L% 2>&1
type %L%
echo.
echo Si arriba pone "buscar.py v3", ya esta. Si no, dile a Claude que lo mire (queda en _ESTADO_ACTUALIZAR.txt).
pause
