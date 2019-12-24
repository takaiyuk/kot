FROM python:3.8-alpine

ENV APP_HOME /scrape_kot

WORKDIR $APP_HOME

COPY . .

RUN apk add --update --no-cache \
  gcc musl-dev libffi-dev openssl-dev \
  chromium \
  chromium-chromedriver \
  tzdata \
  && pip install poetry \
  && poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi \
  && cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime \
  && apk del tzdata gcc musl-dev libffi-dev openssl-dev

ENTRYPOINT ["python"]
CMD ["./run.py"]
