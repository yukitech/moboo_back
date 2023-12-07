FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

WORKDIR /app

COPY ./api /api

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8083

CMD ["uvicorn","api.csi_predict_api:app","--host","0.0.0.0","--port","8000"]