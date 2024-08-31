#!/bin/sh

DJANGO_CMD="python manage.py runserver 0.0.0.0:8000"

echo "+_+| Running Space-Pin-Pong Dev Server"
$DJANGO_CMD &

while true
do
    # 서버 프로세스 확인
    if ! pgrep -f "$DJANGO_CMD" > /dev/null
    then
        echo "+_+| Django 서버가 중지되었습니다. 다시 시작합니다." >> $LOGFILE
        $DJANGO_CMD &
    fi
    sleep 5
done
