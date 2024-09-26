#!/bin/sh

F_WHITE='\033[38;5;15m'  # foreground white
B_PURPLE='\033[48;5;200m'  # background purple
NC='\033[0m' # No Color
SPEAKER="${F_WHITE}${B_PURPLE}|+_+|${NC}"

APP_DOMAIN="api.spp.com"

# Generate SSL certificate
set -ex \
    && apt install openssl \
    && openssl req \
      -newkey rsa:2048 -nodes -keyout /app/django.key \
      -x509 -days 365 -out /app/django.crt \
      -subj "/C=KR/ST=Seoul/L=Seoul/O=42/OU=42 Seoul/CN=${APP_DOMAIN}"

DJANGO_CMD="daphne -b 0.0.0.0 \
    -e ssl:8443:privateKey=/app/django.key:certKey=/app/django.crt \
    config.asgi:application"

/bin/echo -e "${SPEAKER} Running Space-Pin-Pong Dev Server"
exec $DJANGO_CMD
