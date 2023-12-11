FROM python:3.9.18-alpine

ENV LANG C.UTF-8
ENV TZ Asia/Tokyo

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN apk add --no-cache postgresql-libs \
 && apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev \
 && pip install --upgrade pip \
 && pip install -r requirements.txt --no-cache-dir \
 && apk --purge del .build-deps

COPY ./app ./app

CMD ["uvicorn","csi_predict_api:app", "--reload","--host","0.0.0.0","--port","8000"]