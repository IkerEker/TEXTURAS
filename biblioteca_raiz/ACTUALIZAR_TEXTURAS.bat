@echo off
chcp 65001 >nul
title BIBLIOTECA - actualizar TEXTURAS
set G=git
where git >nul 2>nul || set G="%ProgramFiles%\Git\cmd\git.exe"
%G% -C "%~dp0TEXTURAS" pull --ff-only
echo.
python "%~dp0TEXTURAS\tools\atlas\buscar.py" --version
echo Si arriba pone "buscar.py v2", ya esta.
pause
