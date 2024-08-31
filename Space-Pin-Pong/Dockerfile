FROM python:3.11.9-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt upgrade -y && apt install -y \
        dumb-init \
    && pip install --upgrade pip

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN chmod +x ./entrypoint/docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/usr/bin/dumb-init", "--", "./entrypoint/docker-entrypoint.sh"]
