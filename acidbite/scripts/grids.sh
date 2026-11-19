#!/bin/bash
# uso: grids.sh <video> <carpeta_salida> [n_fotogramas]
f="$1"; out="$2"; n="${3:-18}"
mkdir -p "$out"; rm -f "$out"/*.jpg
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
step=$(python3 -c "print(max(4, float('$d')/$n))")
ffmpeg -v error -y -i "$f" -vf "fps=1/$step,scale=800:-2,drawtext=text='%{pts\:hms}':x=10:y=10:fontsize=28:fontcolor=yellow:box=1:boxcolor=black,tile=2x3" -q:v 4 "$out/t_%02d.jpg"
echo "$(basename "$f"): ${d}s -> $(ls "$out" | wc -l) rejillas"
