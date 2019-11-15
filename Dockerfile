FROM python:3.8-alpine

ENV APP_HOME /scrape_kot

WORKDIR $APP_HOME

COPY . .

RUN apk add --update \
  chromium \
  chromium-chromedriver \
  && pip install poetry \
  && poetry config settings.virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

ENTRYPOINT ["python"]
CMD ["./run.py"]
