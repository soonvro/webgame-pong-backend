FROM python:3.11.9-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN chmod +x ./entrypoint/docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint/docker-entrypoint.sh"]
