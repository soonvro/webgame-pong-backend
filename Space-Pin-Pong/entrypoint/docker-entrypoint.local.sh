#!/bin/sh

F_WHITE='\033[38;5;15m'  # foreground white
B_PURPLE='\033[48;5;200m'  # background purple
NC='\033[0m' # No Color
SPEAKER="${F_WHITE}${B_PURPLE}|+_+|${NC}"

DJANGO_CMD="python manage.py runserver 0.0.0.0:8000"

/bin/echo -e "${SPEAKER} Running Space-Pin-Pong Dev Server"
exec $DJANGO_CMD
