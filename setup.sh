#!/usr/bin/env bash
# Prepara el entorno cloud para el motor (ffmpeg + Pillow).
set -e
echo "== ARVION Content Engine setup =="
if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "Instalando ffmpeg..."
  (sudo apt-get update -y && sudo apt-get install -y ffmpeg) || apt-get install -y ffmpeg || true
fi
python3 -m pip install --quiet --upgrade pillow || pip install --quiet pillow
echo "ffmpeg: $(command -v ffmpeg || echo NO)"
python3 -c "import PIL; print('Pillow', PIL.__version__)"
echo "Fuentes:"; ls assets/fonts
echo "Música:"; ls assets/music
echo "== listo =="
