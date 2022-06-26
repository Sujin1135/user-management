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

아래 명령어를 입력하여 PostgreSQL 환경을 설정 합니다.

```
docker-compose up
```

### Poetry 설치

패키지 관리툴 Poetry를 설치 합니다.

```
pip install poetry
```

### 의존성 라이브러리 설치

```
poetry install
```
