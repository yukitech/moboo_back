FROM python:3.9.4-buster

ENV LANG C.UTF-8
ENV TZ Asia/Tokyo

WORKDIR /moboo_back/app

COPY ./requirements.txt requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libpq-dev \
    libhdf5-dev \
    python3-dev \
    build-essential \
    gcc \
    musl-dev \
    postgresql \
  && pip install --upgrade pip \
  && pip install -r requirements.txt --no-cache-dir \
  && apt-get purge -y --auto-remove build-essential gcc musl-dev

COPY ./app .

EXPOSE 8000

CMD ["uvicorn","csi_predict_api:app", "--reload","--host","0.0.0.0","--port","8000"]