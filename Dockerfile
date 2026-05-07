FROM node:22-alpine3.23 AS frontend-build

WORKDIR /app/frontend

ARG VITE_API_BASE_URL=/api
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

RUN apk upgrade --no-cache

COPY frontend/package*.json ./
RUN npm ci

COPY frontend ./
RUN npm run build

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FRONTEND_DIST_DIR=/app/frontend_dist
ENV CCPNA_DATA_DIR=/data

WORKDIR /app

COPY backend ./backend
RUN pip install --no-cache-dir -e ./backend

COPY --from=frontend-build /app/frontend/dist ./frontend_dist

EXPOSE 8000

CMD python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}