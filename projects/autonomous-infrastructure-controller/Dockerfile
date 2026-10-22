FROM python:3.12-alpine
WORKDIR /app
COPY controller/ ./controller/
RUN addgroup -S app && adduser -S -G app -u 10001 app
USER 10001:10001
ENTRYPOINT ["python","-m","controller.cli"]
