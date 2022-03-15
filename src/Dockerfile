ARG PYTHON_V=3.10.2

# ---- Base python ----
FROM python:${PYTHON_V}-slim AS base

RUN addgroup --gid 1001 app && adduser \
    --uid 1001 \
    --ingroup app \
    --disabled-password \
    --gecos "" \
    --home /app \
    app

USER app
WORKDIR /app

ENV PATH="/app/.local/bin:${PATH}"

COPY --chown=app:app requirements.txt requirements.txt

RUN pip install --upgrade \
    pip \
    setuptools

RUN pip install --user --no-cache-dir -r requirements.txt

RUN chown app:app /app 

EXPOSE 80

# --- Release app ---
FROM python:${PYTHON_V}-slim AS release

RUN addgroup --gid 1001 app && adduser \
    --uid 1001 \
    --ingroup app \
    --disabled-password \
    --gecos "" \
    --home /app \
    app

USER app
WORKDIR /app

COPY --from=base /app /app
COPY --chown=app:app app .

ENV PATH="/app/.local/bin:${PATH}"

CMD ["python3", "app.py", "-W", "ignore::DeprecationWarning"]

# ---- Test app ----
FROM python:${PYTHON_V}-slim AS test

RUN addgroup --gid 1001 app && adduser \
    --uid 1001 \
    --ingroup app \
    --disabled-password \
    --gecos "" \
    --home /app \
    app

USER app
WORKDIR /app

COPY --from=base /app /app

ENV PATH="/app/.local/bin:${PATH}"
RUN pip install --upgrade \
    pytest-asyncio \
    pytest-mock \
    coverage

COPY --chown=app:app app .
COPY --chown=app:app tests tests

RUN python3 -m coverage run -m \
    pytest --tb=auto tests && \
    python3 -m coverage \
    report --omit="tests*"