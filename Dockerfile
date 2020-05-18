FROM python:3.8-alpine as builder
COPY poetry.lock pyproject.toml ./
# hadolint ignore=DL3018, DL4006, SC2094
RUN apk add --update --no-cache gcc musl-dev libffi-dev openssl-dev tzdata \
  && pip install poetry==1.0.2 \
  && poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

FROM python:3.8-alpine
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=builder /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
ENV PYTHONPATH=/usr/local:$PYTHONPATH
ENV APP_HOME /scrape_kot
WORKDIR $APP_HOME
COPY . .
RUN apk add --update --no-cache \
  chromium=81.0.4044.113-r0 \
  chromium-chromedriver=81.0.4044.113-r0

ENTRYPOINT ["python"]
