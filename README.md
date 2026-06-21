# ARVION Content Engine

Motor de producción de contenido de marca para ARVION GROUP.
Genera reels cinematográficos y carruseles educativos con identidad visual premium (estilo "C": oscuro + azul ARVION + tipografía Sora), y los entrega listos para publicar.

## Estructura
```
scripts/
  brand.py             # identidad visual compartida (colores, fuentes, helpers)
  render_carousel.py   # carrusel (7 slides) desde config JSON
  render_reel.py       # reel (multi-escena + transiciones + música) desde config JSON
assets/
  fonts/               # Montserrat, Sora, Archivo (premium)
  music/               # librería de pistas instrumentales (ElevenLabs)
config/                # configs de ejemplo
RUNBOOK.md             # proceso semanal que ejecuta el agente cloud
setup.sh               # instala ffmpeg + pillow en el entorno cloud
```

## Uso
```bash
bash setup.sh
python3 scripts/render_reel.py config/reel.json
python3 scripts/render_carousel.py config/carousel.json
```

Las imágenes y videos (inputs) se generan con Higgsfield (Nano Banana = Gemini para imágenes, Kling para video). Los scripts hacen el ensamblaje de alta calidad (texto, transiciones, música).

Diseño técnico: `Projects/ARVION GROUP COMPANY CEO/docs/superpowers/specs/2026-06-21-arvion-content-engine-v2-design.md`
Estrategia: `Projects/ARVION GROUP COMPANY CEO/content-engine/MARKETING-PLAYBOOK-Y-CRONOGRAMA.md`
