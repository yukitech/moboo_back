FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

WORKDIR /app

COPY ./app ./app

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt install -y tzdata && apt-get clean && rm -rf /var/lib/apt/lists/* 

CMD ["uvicorn","app.csi_predict_api:app","--host","0.0.0.0","--port","8000"]