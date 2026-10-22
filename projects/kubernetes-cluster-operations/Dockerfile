FROM python:3.12-alpine
WORKDIR /app
COPY app/ ./app/
RUN addgroup -S app && adduser -S -G app -u 10001 app
USER 10001:10001
ENV PYTHONUNBUFFERED=1 PORT=8080
EXPOSE 8080
CMD ["python", "-m", "app.main"]
