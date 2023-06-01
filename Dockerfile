FROM python:3.7-alpine
RUN apk add --no-cache curl
WORKDIR /
COPY command-exporter.py /
EXPOSE 8080
CMD ["python", "command-exporter.py"]
