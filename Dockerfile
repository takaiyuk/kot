FROM python:3.8-alpine as builder
COPY poetry.lock pyproject.toml ./
# hadolint ignore=DL4006, SC2094
RUN echo @3.11 http://nl.alpinelinux.org/alpine/v3.11/community >> /etc/apk/repositories \
  && echo @3.11 http://nl.alpinelinux.org/alpine/v3.11/main >> /etc/apk/repositories \
  && apk add --update --no-cache gcc@3.11=9.2.0-r4 musl-dev@3.11=1.1.24-r2 libffi-dev@3.11=3.2.1-r6 openssl-dev@3.11=1.1.1d-r3 tzdata@3.11=2019c-r0 \
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
RUN echo @3.11 http://nl.alpinelinux.org/alpine/v3.11/community >> /etc/apk/repositories \
  && echo @3.11 http://nl.alpinelinux.org/alpine/v3.11/main >> /etc/apk/repositories \
  && apk add --update --no-cache \
  chromium@3.11=79.0.3945.130-r0 \
  chromium-chromedriver@3.11=79.0.3945.130-r0

ENTRYPOINT ["python"]
