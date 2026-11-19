@echo off
chcp 65001 >nul
title BIBLIOTECA - montar la biblioteca comun
echo Deja esta ventana abierta. Se puede cerrar y volver a lanzar: retoma donde lo dejo.
echo Si se abre el navegador, inicia sesion en GitHub.
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0montar_biblioteca.ps1"
echo.
echo Terminado. Ya puedes avisar a Claude.
pause
