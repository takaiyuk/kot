FROM python:3.8-alpine as builder
COPY poetry.lock pyproject.toml ./
# hadolint ignore=DL4006, SC2094
RUN apk add --update --no-cache gcc=8.3.0-r0 musl-dev=1.1.22-r3 libffi-dev=3.2.1-r6 openssl-dev=1.1.1d-r2 tzdata=2019c-r0 \
  && pip install poetry==1.0.2 \
  && poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

FROM python:3.8-alpine
COPY --from=builder /usr/local /usr/local
COPY --from=builder /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
ENV PYTHONPATH=/usr/local:$PYTHONPATH
ENV APP_HOME /scrape_kot
WORKDIR $APP_HOME
COPY . .
RUN apk add --update --no-cache \
  chromium=77.0.3865.120-r0 \
  chromium-chromedriver=77.0.3865.120-r0

ENTRYPOINT ["python"]
CMD ["./run.py"]
