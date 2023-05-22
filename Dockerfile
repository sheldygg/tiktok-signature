# Separate "build" image
FROM python:3.11-slim-bullseye as compile-image
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY tiktok_signature .
COPY pyproject.toml .


# "Run" image
FROM python:3.11-slim-bullseye
COPY --from=compile-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
COPY . /app/
RUN pip install .[server]
RUN playwright install chromium && playwright install-deps
EXPOSE 8002

CMD ["python", "tiktok_signature/server.py"]