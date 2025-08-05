FROM python:3.13-bullseye

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8930

CMD ["./run_metaafzar.sh"]
