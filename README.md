# Marcador Streaming TV (Soccer)

Overlay minimalista para transmisión con personalización visual en tiempo real.

## Incluye

- Marcador editable (equipo local/visitante y goles).
- Cronómetro de partido (hasta 90') con inicio, pausa, reanudación y reset.
- Cuadro de tiempo de adición (`+min`) para 45' o 90'.
- Personalización de colores, gradientes, tipografías y estilo visual.
- Persistencia automática en `localStorage`.
- Ejecutable instalador para integración rápida con OBS plugins.

## Descargar el proyecto

### Opción A: con Git

```bash
git clone <URL_DEL_REPO>
cd Cronoe
```

### Opción B: ZIP desde GitHub

1. En GitHub, pulsa **Code > Download ZIP**.
2. Descomprime el archivo.
3. Abre terminal dentro de la carpeta `Cronoe`.

## Ejecutar local (preview del overlay)

```bash
python3 -m http.server 4173
```

Luego abre en navegador:

```text
http://localhost:4173
```

## Ejecutable para OBS plugins

### 1) Construir ejecutable (`.pyz` generado localmente)

```bash
./scripts/build_obs_installer.sh
```

> Nota: el archivo `dist/cronoe_obs_installer.pyz` es un binario generado y no se versiona en Git.

### 2) Ejecutar instalador (autodetección de ruta OBS)

```bash
./dist/cronoe_obs_installer.pyz
```

### 3) Ejecutar instalador (ruta manual)

```bash
./dist/cronoe_obs_installer.pyz --obs-plugin-dir "$HOME/.config/obs-studio/plugins"
```

Esto copia `index.html`, `styles.css`, `app.js`, `README.md` y crea `OBS_SETUP.txt` con pasos rápidos.

## Uso en OBS / Streamlabs

1. Agrega una fuente tipo **Browser Source**.
2. Activa **Local file** y selecciona el `index.html` instalado por el ejecutable.
3. Ajusta tamaño según tu canvas de transmisión.
4. Usa el panel "Personalización visual" para definir branding del canal.
