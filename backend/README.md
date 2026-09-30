# FastAPI backend — next stage

This folder is reserved for the model-serving API.

Planned:
- `app.py` — FastAPI application
- `model/` — trained pipeline/model
- `schemas.py` — request/response validation
- `services/predict.py` — inference logic
- `logs/` — application logs

The React frontend currently uses a clearly marked demo response. We will replace it with `POST /predict` after the ML model is trained.
