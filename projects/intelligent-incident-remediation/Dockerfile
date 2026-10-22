FROM python:3.12-alpine
WORKDIR /app
COPY engine.py server.py ./
RUN addgroup -S app && adduser -S -G app -u 10001 app
USER 10001:10001
ENV HOST=0.0.0.0 PORT=8080
EXPOSE 8080
CMD ["python","server.py"]
