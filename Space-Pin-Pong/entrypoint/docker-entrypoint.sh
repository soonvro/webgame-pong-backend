#!/bin/sh

F_WHITE='\033[38;5;15m'  # foreground white
B_PURPLE='\033[48;5;200m'  # background purple
NC='\033[0m' # No Color
SPEAKER="${F_WHITE}${B_PURPLE}|+_+|${NC}"

/bin/echo -e "${SPEAKER} Running Database Migrations"
python manage.py makemigrations
python manage.py migrate

exec "$@"
