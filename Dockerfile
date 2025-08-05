FROM python:3.13-bullseye

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8930

RUN chmod +x run_metaafzar.sh
CMD ["./run_metaafzar.sh"]
