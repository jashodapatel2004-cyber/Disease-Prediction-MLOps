# DiabetesAI — Disease Prediction MLOps

A professional full-stack starter for an MSc Data Science MLOps project.

## Current stage
- Professional React + Vite frontend
- Diabetes prediction dashboard UI
- Patient prediction form matching the selected dataset
- Dashboard, prediction, model performance, monitoring and documentation views
- Demo prediction flow (backend not connected yet)
- Dataset included under `data/`

## Planned MLOps pipeline
Dataset → preprocessing → model training → evaluation → MLflow → FastAPI → logging/monitoring → Docker → React frontend

## Run frontend
```bash
cd frontend
npm install
npm run dev
```

The frontend is intentionally separated from the ML/API layer so we can connect FastAPI after the model is trained.
