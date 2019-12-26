FROM python:3.8-alpine as builder
COPY poetry.lock pyproject.toml ./
RUN apk add --update --no-cache gcc musl-dev libffi-dev openssl-dev tzdata \
  && pip install poetry \
  && poetry export -f requirements.txt > requirements.txt \
  && pip freeze | xargs pip uninstall -y \
  && pip install --user -r requirements.txt

FROM python:3.8-alpine
COPY --from=builder /root/.local /root/.local
COPY --from=builder /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
ENV PYTHONPATH=/root/.local:$PYTHONPATH
ENV APP_HOME /scrape_kot
WORKDIR $APP_HOME
COPY . .
RUN apk add --update --no-cache \
  chromium \
  chromium-chromedriver

ENTRYPOINT ["python"]
CMD ["./run.py"]
