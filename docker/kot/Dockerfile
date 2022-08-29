FROM python:3.9.13-buster as builder
COPY poetry.lock pyproject.toml ./
RUN apt -y update \
  && apt -y install tzdata \
  && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - \
  && . $HOME/.poetry/env \
  && poetry config virtualenvs.create false \
  && poetry install --no-ansi --no-interaction

FROM python:3.9.13-slim-buster
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
ENV PYTHONPATH=/usr/local:$PYTHONPATH
ENV APP_HOME /kot
WORKDIR $APP_HOME
RUN apt -y update \
  && apt -y install chromium \
  && rm -rf /var/lib/apt/lists/*
COPY kot kot
COPY scripts scripts
# Turn off webdriver-manager logs use
ENV WDM_LOG 0

RUN python -m kot initialize

ENTRYPOINT ["python"]
