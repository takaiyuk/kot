FROM python:3.10.2-bullseye as builder
COPY requirements.txt ./
RUN apt -y update \
  && apt -y install tzdata \
  && pip install -r requirements.txt

FROM python:3.10.2-slim-bullseye
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
ENV PYTHONPATH=/usr/local:$PYTHONPATH
ENV APP_HOME /kot
WORKDIR $APP_HOME
COPY . .
RUN apt -y update \
  && apt -y install chromium

ENTRYPOINT ["python"]
