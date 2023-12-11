FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

ENV LANG C.UTF-8
ENV TZ Asia/Tokyo

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN apt-get update && apt-get install postgresql && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ./app ./app

CMD ["uvicorn","csi_predict_api:app", "--reload","--host","0.0.0.0","--port","8000"]