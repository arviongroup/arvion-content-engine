# RUNBOOK — Lote semanal de contenido ARVION (agente cloud)

Eres el agente de producción de contenido de ARVION GROUP. Cada semana generas el lote y se lo entregas a Daniel para aprobar. Sigue estos pasos en orden.

## 0. Preparar entorno
```bash
bash setup.sh   # instala ffmpeg + Pillow; confirma fuentes y música
```

## 1. Definir los temas de la semana
Genera **3 reels + 2 carruseles**. Usa los 3 pilares de ARVION (consultoría de IA para empresas LatAm):
- Pilar 1 "IA en 60s" (tips prácticos) — 70%
- Pilar 2 "Cómo las empresas usan IA" (casos) — 20%
- Pilar 3 "Arvion explica" (conceptos) — 10%
Tono: profesional cercano, español neutro. Sin vender directo; CTA suave ("síguenos").

## 2. Identidad visual (OBLIGATORIA, no cambiar)
- Oscuro premium + **azul ARVION** + tipografía Sora (estilo "C").
- Imágenes Higgsfield **SIN texto** (el texto lo pone el motor): siempre incluir en el prompt "no people, no text, no letters" y "deep navy and electric blue, cinematic, photorealistic, generous dark empty space for text".

## 3. Producir cada REEL (3 escenas)
Para cada reel:
1. Genera 3 imágenes de fondo 9:16 con `generate_image` (model `nano_banana_pro`), una por escena (gancho / desarrollo / cierre). Prompts en el estilo del §2.
2. Anima cada imagen con `generate_video` (model `kling3_0_turbo`, duration 5, aspect 9:16, medias start_image = id de la imagen). Si responde con preset_recommendation, reintenta con `declined_preset_id`.
3. Descarga los 3 mp4 a una carpeta de trabajo.
4. Escribe `reel_N.json` (ver `config/reel.json`): 3 escenas con sus textos (gancho corto, palabra clave en azul = `1`), elige una música de `assets/music/` acorde al mood.
5. `python3 scripts/render_reel.py reel_N.json`

## 4. Producir cada CARRUSEL (7 slides)
1. Genera 7 imágenes 4:5 con `generate_image` (`nano_banana_pro`), una por slide (portada + 5 contenido + cierre), estilo §2.
2. Descarga las 7 png.
3. Escribe `carousel_N.json` (ver `config/carousel.json`).
4. `python3 scripts/render_carousel.py carousel_N.json`

## 5. Escribir captions (SEO)
Crea `captions.md` con, por cada pieza: caption (gancho en línea 1 + valor + CTA suave), hashtags (8-12 TikTok/IG con #ARVION; 3-5 LinkedIn), y para reels título+descripción YouTube. Mete la palabra clave en la primera línea.

## 6. Entregar
1. Sube todo a Google Drive en `ARVION — Content Engine / Listos-para-publicar / [YYYY-WW]` (reels mp4 + carpetas de carrusel + captions.md). Obtén link compartible de la carpeta.
2. Avisa a Daniel por Telegram con un POST al webhook de n8n:
```bash
curl -X POST "$N8N_NOTIFY_URL" -H "Content-Type: application/json" \
  -d '{"texto":"🎬 Lote semanal listo: 3 reels + 2 carruseles. Revisa y aprueba 👇","link":"<DRIVE_LINK>"}'
```
(`N8N_NOTIFY_URL` = webhook `content-notify` de n8n.)

## Notas
- Calidad ante todo: NO bajar resolución ni saltarse el ensamblaje del motor.
- Logo de marca de agua: pendiente (cuando esté `assets/logo.png`, añadir overlay en una esquina).
- Si algo falla, reporta el error claramente en el resumen final; no entregues piezas a medias.
