FROM python:3.8-buster as builder
COPY poetry.lock pyproject.toml ./
ADD https://chromedriver.storage.googleapis.com/2.45/chromedriver_linux64.zip /usr/bin
# hadolint ignore=DL3008, DL4006, SC2094
RUN apt-get -y update \
  && apt-get -y install --no-install-recommends tzdata wget unzip \
  # pip
  && pip install poetry==1.0.2 \
  && poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi \
  # chromium
  && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add \
  && echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list \
  && apt-get -y update \
  && apt-get -y install --no-install-recommends google-chrome-stable \
  # chrome-driver
  && unzip /usr/bin/chromedriver_linux64.zip -d /usr/bin \
  && rm /usr/bin/chromedriver_linux64.zip \
  # cleanup
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

FROM python:3.8-slim-buster as runner
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=builder /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
COPY --from=builder /usr/bin/chromedriver /usr/bin/chromedriver
COPY --from=builder /usr/bin/google-chrome-stable /usr/bin/google-chrome-stable
ENV PYTHONPATH=/usr/local:$PYTHONPATH
ENV APP_HOME /scrape_kot
WORKDIR $APP_HOME
COPY . .
# RUN apt-get -y update \
#   && apt-get -y install --no-install-recommends \
#   && apt-get clean \
#   && rm -rf /var/lib/apt/lists/*
ENTRYPOINT ["python"]
