# Cronoe Surveys - Base del proyecto

Estructura monolítica en Python para soportar encuestas con acceso por `public_code` (ideal para QR).

## Módulos iniciales

- `surveys`: creación/edición/publicación de encuestas.
- `responses`: captura de respuestas.
- `access`: resolución de encuestas por código público.

## API mínima

- `POST /surveys`
- `GET /surveys/{public_code}`
- `POST /surveys/{public_code}/responses`

### Extra

- `PATCH /surveys/{public_code}` para editar/publicar.

## Ejecución local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
python -m app.main
```

## Notas

- `public_code` se genera con `secrets.token_urlsafe(...)`, por lo que es no secuencial y seguro para compartir en enlaces/QR.
- Almacenamiento actual en memoria (`app/storage.py`) para bootstrap rápido.
