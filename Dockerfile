FROM python:3.9.0 AS builder

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY Pipfile Pipfile.lock setup.py attention_attention.py ETS_fermeture.mp3 /app/

RUN pip install --no-cache-dir pipenv \
    && python -m pipenv --three \
    && python -m pipenv install

FROM python:3.9.0-slim AS runtime

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir pipenv \
    && apt-get update \
    && apt-get install -y ffmpeg libopus0 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local/share/virtualenvs /root/.local/share/virtualenvs
COPY --from=builder /app /app

CMD [ "python", "-m", "pipenv", "run", "python", "attention_attention.py" ]
