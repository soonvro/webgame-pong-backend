<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Unlicense License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
<br /><br />


<!-- PROJECT LOGO & NAME -->
<!-- Logo Source: https://pixabay.com/illustrations/icosphere-image-images-blender-3200744/ -->
<div align="center">
  <img alt="Logo" src="https://i.imgur.com/7OsJPNI.png" width="350" height="45">
</div>


<!-- HEADLINE -->
<h1 align="center">
  Pong 온라인 웹 게임 서비스 - Backend
</h1>


<!-- SHORT DESCRIPTION -->
<h4 align="center">
  고전 게임 Pong을 현대적으로 재해석한 실시간 멀티플레이어 게임의 백엔드 서비스입니다. Django와 WebSocket을 활용하여 원활한 게임플레이, 사용자 관리, 실시간 알림을 제공합니다.
</h4>
<br />


<!-- SHOWCASE -->
<!--
<div align="center">
  <img alt="Showcase" src="https://cdn.pixabay.com/animation/2022/10/11/23/03/23-03-06-809_512.gif" width="500" height="500">
</div>
<br />
-->


<!-- TABLE OF CONTENTS -->
<details>
  <summary><b>Table of Contents</b></summary>
  <ul>
    <li><a href="#주요-기능">주요 기능</a></li>
    <li><a href="#빠른-시작">빠른 시작</a></li>
    <li><a href="#사용-예시">사용 예시</a></li>
    <ul>
      <li><a href="#api-엔드포인트">API 엔드포인트</a></li>
    </ul>
    <li><a href="#왜-space-pin-pong을-만들었나요">왜 Space-Pin-Pong을 만들었나요?</a></li>
    <li><a href="#기술-스택">기술 스택</a></li>
    <li><a href="#프로젝트-구조">프로젝트 구조</a></li>
    <li><a href="#게임-시스템">게임 시스템</a></li>
    <li><a href="#개발">개발</a></li>
    <li><a href="#라이선스">라이선스</a></li>
  </ul>
</details>


# 주요 기능

- **실시간 게임 엔진**:
    - WebSocket 기반 240 FPS 게임 엔진
    - 정밀한 물리 충돌 처리
    - 자동 스코어링 시스템
    - 다양한 게임 모드 (1v1, 로컬, AI, 토너먼트)
- **42 OAuth 인증**:
    - 42 계정 연동
    - JWT 기반 사용자 인증
    - 토큰 자동 갱신
- **사용자 관리**:
    - 프로필 수정
    - 전적 및 통계 시스템
    - 계정 비활성화
- **토너먼트 시스템**:
    - 실시간 토너먼트 매칭
    - 준결승/결승 라운드
    - 승자 투표 시스템
- **친구 시스템**:
    - 친구 추가/수락/거절
    - 온라인 상태 확인
    - 실시간 알림

<p align="right"><a href="#readme-top">▲ 맨 위로</a></p>


# 빠른 시작

### 요구 사항
- Docker 및 Docker Compose
- 42 OAuth 애플리케이션 설정

### 환경 변수
```
# Django
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB_CACHE=1
REDIS_DB_CHANNEL=2

# 42 OAuth
OAUTH_CLIENT_ID=your_42_client_id
OAUTH_CLIENT_SECRET=your_42_client_secret
OAUTH_REDIRECT_URI=your_redirect_uri
OAUTH_AUTHORIZE_URL=https://api.intra.42.fr/oauth/authorize
OAUTH_TOKEN_URL=https://api.intra.42.fr/oauth/token
OAUTH_USER_API_URL=https://api.intra.42.fr/v2/me
```

### 서버 실행
```shell
# 저장소 클론:
git clone [repository-url]
cd back_end

# 개발 서버 시작:
docker-compose -f docker-compose.local.yml up --build

# 프로덕션 환경:
docker-compose up --build

```

**서버 접속**:  
- API: `http://localhost:8000/api/`
- WebSocket: `ws://localhost:8000/ws/`

<p align="right"><a href="#readme-top">▲ 맨 위로</a></p>


# 사용 예시

### API 엔드포인트

자세한 API 문서는 `API.md` 파일을 참고하세요.

주요 엔드포인트:
- `/api/users/` - 사용자 관리
- `/api/games/` - 게임 관련 작업
- `/api/notifications/` - 알림
- `/ws/game/` - 게임 웹소켓
- `/ws/notification/` - 알림 웹소켓

<p align="right"><a href="#readme-top">▲ 맨 위로</a></p>


# 왜 Space-Pin-Pong을 만들었나요?

단순히 게임을 즐기는 것을 넘어서, 실시간 멀티플레이어 웹 게임의 백엔드를 직접 구현하여 그 작동 방식을 깊이 이해하고자 시작한 프로젝트입니다. 덕분에 평소에는 추상적으로만 이해했던 실시간 게임 서버의 내부 구조를 명확하게 파악하고, 필요시 분석 및 수정까지 가능한 수준으로 이해도를 높일 수 있었습니다.

### 기술적 도전
- **WebSocket 기반 실시간 통신**: Django Channels를 활용한 양방향 실시간 통신을 구현하여 지연 없는 게임플레이를 구현했습니다. 특히 240 FPS의 게임 엔진과 60 FPS의 클라이언트 간의 최적화된 상태 동기화를 달성했습니다.
- **물리 엔진 구현**: 충돌 감지, 반사각 계산, 속도 벡터 처리 등 게임 물리를 Python으로 구현하며 게임 서버의 핵심 로직을 이해했습니다.
- **상태 관리**: 다중 사용자의 게임 상태를 실시간으로 관리하고 동기화하는 과정에서 분산 시스템의 동시성 처리를 경험했습니다.

### 서버 아키텍처 설계
- **마이크로서비스 구조**: 인증, 게임, 알림, 사용자 관리를 독립적인 Django 앱으로 분리하여 확장 가능한 아키텍처를 설계했습니다.
- **캐싱 전략**: Redis를 활용한 게임 상태 및 사용자 세션 캐싱으로 성능을 최적화했습니다.
- **보안**: JWT 기반 인증, OAuth 통합, HTTPS/SSL 설정을 통해 안전한 서비스 환경을 구축했습니다.

### 개발 프로세스 개선
- **코드 품질**: pre-commit 훅을 통한 자동화된 코드 검사와 포맷팅으로 일관된 코드 스타일을 유지했습니다.
- **테스트 자동화**: 단위 테스트와 통합 테스트를 구현하여 안정적인 서비스 품질을 보장했습니다.
- **문서화**: API 문서화를 통해 프론트엔드 팀과의 효율적인 협업 환경을 구축했습니다.

<p align="right"><a href="#readme-top">▲ 맨 위로</a></p>


# 기술 스택

**Languages & Frameworks**:  
- ![Python][python-badge]  ![Django][django-badge]  ![DRF][django-rest-badge]  

**Databases**:  
- ![PostgreSQL][postgres-badge]  
- ![Redis][redis-badge]

**Authentication & Authorization**:  
- ![JWT][jwt-badge]  
- ![OAuth 2.0][oauth-2-badge]

**Infrastructure & DevOps**:  
- ![Docker][docker-badge]  

**Protocols & APIs**:
- ![REST API][rest-api-badge]  
- ![WebSocket][websocket-badge]

<p align="right"><a href="#readme-top">▲ 맨 위로</a></p>


# 프로젝트 구조

```
Space-Pin-Pong/
├── apps/                    # Django 애플리케이션
│   ├── accounts/           # 인증 및 계정 관리
│   ├── games/             # 게임 로직 및 매칭
│   ├── notifications/     # 실시간 알림 시스템
│   └── users/            # 사용자 프로필 및 친구 관리
├── config/                # 프로젝트 설정
│   ├── settings/         # 환경별 설정
│   │   ├── base.py      # 기본 설정
│   │   └── local.py     # 개발 환경 설정
│   ├── urls.py          # URL 라우팅
│   └── asgi.py          # ASGI 설정
└── entrypoint/           # Docker 진입점 스크립트
```

<p align="right"><a href="#readme-top">▲ 맨 위로</a></p>


# 게임 시스템

### 게임 규칙
- 게임 엔진: 내부 240 FPS, 클라이언트 60 FPS
- 필드 크기: -500 ~ 500 (X축), -250 ~ 250 (Y축)
- 패들 크기: 10x100 단위
- 공 반지름: 7 단위
- 공 속도: 1000 단위/초
- 패들 속도: 500 단위/초
- 승리 조건: 15점 선취

### 게임 모드
1. **1대1 원격**
   - 실시간 매칭
   - 게임 코드로 초대
2. **로컬 게임**
   - 한 기기에서 두 명이 플레이
3. **AI 대전**
   - 컴퓨터와 대결
4. **토너먼트**
   - 4인 토너먼트
   - 준결승/결승 방식
   - 승자 투표 시스템

<p align="right"><a href="#readme-top">▲ 맨 위로</a></p>








# 개발

### 테스트 실행
```bash
python manage.py test
```

### DB 마이그레이션
```bash
python manage.py makemigrations
python manage.py migrate
```

### 코드 품질 관리
프로젝트는 다음 도구들을 사용하여 코드 품질을 관리합니다:

- **Black**: 코드 포맷터 (최대 라인 길이: 120)
- **isort**: 임포트 문 정렬
- **mypy**: 타입 체크 (django-stubs 포함)
- **flake8**: 린터 (최대 라인 길이: 120)

pre-commit 설정:
```bash
# pre-commit 설치
pip install pre-commit

# pre-commit 훅 설치
pre-commit install
```

<p align="right"><a href="#readme-top">▲ 맨 위로</a></p>


# 라이선스

이 프로젝트는 42 School 교육과정의 일부이며, 해당 라이선스 조항을 따릅니다.

<p align="right"><a href="#readme-top">▲ 맨 위로</a></p>



<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/soonvro/Github-Docs-Templates.svg?style=for-the-badge
[contributors-url]: https://github.com/soonvro/Github-Docs-Templates/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/soonvro/Github-Docs-Templates.svg?style=for-the-badge
[forks-url]: https://github.com/soonvro/Github-Docs-Templates/network/members
[stars-shield]: https://img.shields.io/github/stars/soonvro/Github-Docs-Templates.svg?style=for-the-badge
[stars-url]: https://github.com/soonvro/Github-Docs-Templates/stargazers
[issues-shield]: https://img.shields.io/github/issues/soonvro/Github-Docs-Templates.svg?style=for-the-badge
[issues-url]: https://github.com/soonvro/Github-Docs-Templates/issues
[license-shield]: https://img.shields.io/github/license/soonvro/Github-Docs-Templates?label=license&style=for-the-badge
[license-url]: https://github.com/soonvro/Github-Docs-Templates/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/soonhyung-kwon-aa4331351/

<!-- Source: https://github.com/Ileriayo/markdown-badges -->
[python-badge]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[django-badge]: https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white
[django-rest-badge]: https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray
[postgres-badge]: https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white
[docker-badge]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white
[jwt-badge]: https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens
[redis-badge]: https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white

<!-- My Custom Badges -->
[oauth-2-badge]: https://img.shields.io/badge/OAuth%202.0-white?style=for-the-badge
[rest-api-badge]: https://img.shields.io/badge/REST_API-white?style=for-the-badge
[websocket-badge]: https://img.shields.io/badge/WebSocket-white?style=for-the-badge
