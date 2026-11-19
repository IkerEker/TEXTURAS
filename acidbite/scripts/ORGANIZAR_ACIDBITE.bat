@echo off
chcp 65001 >nul
title ACIDBITE - descomprimir, ordenar y analizar
echo Deja esta ventana abierta. Se puede cerrar y volver a lanzar: retoma donde lo dejo.
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0organizar_acidbite.ps1"
echo.
echo Terminado. Ya puedes avisar a Claude.
pause
