FROM python:3.12-slim

WORKDIR /app

COPY reference-runtime/ /app/

RUN pip install --no-cache-dir -e . && \
    mkdir -p /root/.intent-os

EXPOSE 8377

ENTRYPOINT ["intent-os", "proxy", "start", "--host", "0.0.0.0"]
