#!/bin/sh

F_WHITE='\033[38;5;15m'  # foreground white
B_PURPLE='\033[48;5;200m'  # background purple
NC='\033[0m' # No Color
SPEAKER="${F_WHITE}${B_PURPLE}|+_+|${NC}"

DJANGO_CMD="python manage.py runserver 0.0.0.0:8000"

/bin/echo -e "${SPEAKER} Running Space-Pin-Pong Dev Server"
$DJANGO_CMD &
sleep 5

while true
do
    # 서버 프로세스 확인
    if ! pgrep --full --runstates D,R "$DJANGO_CMD" > /dev/null; then
        /bin/echo -e "${SPEAKER} Django 서버가 중지되었습니다. 다시 시작합니다."
        DJANGO_PIDS=$(pgrep -f "$DJANGO_CMD")
        kill -9 $DJANGO_PIDS
        $DJANGO_CMD &
    fi
    sleep 5
done
