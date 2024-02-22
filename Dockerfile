FROM python:3.11.6 AS MAIN

WORKDIR /app

COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN apt-get update -y

COPY ./isamples_sesar/ ./isamples_sesar/
COPY ./scripts/ ./scripts/

ENV PYTHONPATH "${PYTHONPATH}:/app"

CMD exec python /app/scripts/sesar_things.py --sesar_db_url $SESAR_DB_URL --isb_db_url $ISB_DB_URL load