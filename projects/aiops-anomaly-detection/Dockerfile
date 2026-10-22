FROM python:3.12-alpine
WORKDIR /work
COPY aiops/ ./aiops/
RUN addgroup -S app && adduser -S -G app -u 10001 app && mkdir -p /data && chown app:app /data
USER 10001:10001
ENV AIOPS_HOST=0.0.0.0 AIOPS_DB=/data/metrics.sqlite3
EXPOSE 8091
CMD ["python","-m","aiops.api"]
