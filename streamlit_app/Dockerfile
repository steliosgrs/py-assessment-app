ARG PYTHON_VERSION=3.11

FROM python:${PYTHON_VERSION}-bookworm AS builder

ARG APP_HOME=/app

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential && \
    apt clean && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/0.6.8/install.sh /uv-installer.sh
RUN chmod -R 655 /uv-installer.sh && sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR ${APP_HOME}
COPY requirements.txt .
RUN uv init . && uv add -r requirements.txt

FROM python:${PYTHON_VERSION}-slim-bookworm AS runner
ARG APP_HOME=/app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

WORKDIR ${APP_HOME}

COPY . .
COPY --from=builder ${APP_HOME}/.venv .venv
ENV PATH="/${APP_HOME}/.venv/bin:$PATH"

RUN useradd --create-home uuser
USER uuser

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]