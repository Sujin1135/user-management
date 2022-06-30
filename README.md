# 유저 관리 서비스

## Requirements

해당 환경에서 테스트를 진행 하였습니다:

|                | Main version (dev) |
|----------------|--------------------|
| Python         | 3.8                |
| Platform       | AMD64/ARM64(\*)    |
| PostgreSQL     | 14                 |
| docker-compose | v2.5.0             |

## Getting started

### DB 생성

아래 명령어를 입력하여 PostgreSQL, Redis 를 설치 및 실행 합니다

```
docker-compose up

docker-compose -f ./redis_server.yml up -d
```

### 의존성 라이브러리 설치

패키지 관리툴 Poetry를 설치 합니다

```
pip install poetry
```

pyproject.toml 에 있는 필요 라이브러리 설치

```
poetry install
```

DB 테이블 마이그레이션

```
alembic upgrade head
```

## Code convention

코딩 컨벤션에 따라 코드 포맷팅을 해주고 싶을 경우엔 dev-dependency로 설치된 black을 설정 해주면 되며 Pycharm 사용 시 아래 아티클 참조
- https://velog.io/@heka1024/PyCharm-%ED%8F%AC%EB%A7%A4%ED%84%B0%EB%A1%9C-Black-%EC%84%A4%EC%A0%95%ED%95%98%EA%B8%B0
