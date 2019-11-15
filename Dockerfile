FROM python:3.8.0-alpine

WORKDIR /root

COPY . .
RUN apk add --update --no-cache chromium chromium-chromedriver \
        && pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["./run.py"]

