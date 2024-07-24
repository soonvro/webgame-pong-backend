COMPOSE = @docker-compose
BASH = /bin/sh

all: 
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) down

#make in-frontend라고 치면 frontend로 들어갈수있음
in:
	$(COMPOSE) exec $(TARGET) $(BASH)

#make log-frontend라고 치면 frontend의 로그를 볼수있음
log:
	$(COMPOSE) logs $(TARGET)

ps:
	$(COMPOSE) ps

clean:
	$(COMPOSE) down

fclean:
	$(COMPOSE) down --rmi all
#	도커 컨테이너 캐시, 종료된 컨테이너, 이미지 삭제하는 명령어
#	@docker builder prune -f && docker container prune -f && docker image prune -f

re:
	@make fclean
	make all

.PHONY: all re clean fclean

.ONESHELL:
in-%:
	@$(MAKE) in TARGET=$*

log-%:
	@$(MAKE) log TARGET=$*
