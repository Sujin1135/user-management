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

아래 명령어를 입력하여 PostgreSQL 설치 및 실행 합니다

```
docker-compose up
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

## Run server

```
uvicorn main:app --reload
```

- Swagger path - 127.0.0.1:8000/docs
- Test
테스트 파일은 해당 프로젝트 root 경로 기준 'app/tests' 하위에 있으며 서비스 로직, API 요청 모두 테스트 코드를 실행하여 단위 테스트를 진행하실 수 있습니다

```
  cd app/tests
  
  // 해당경로 아래 모든 테스트 케이스 실행
  pytest
```


## Code convention

코딩 컨벤션에 따라 코드 포맷팅을 해주고 싶을 경우엔 dev-dependency로 설치된 black을 설정 해주면 되며 Pycharm 사용 시 아래 아티클 참조
- https://velog.io/@heka1024/PyCharm-%ED%8F%AC%EB%A7%A4%ED%84%B0%EB%A1%9C-Black-%EC%84%A4%EC%A0%95%ED%95%98%EA%B8%B0

## Conclusions
외부 서비스와 연동하지 않고 SNS 인증을 구현하는데 회원가입 / 비밀번호 변경이 어떻게 가능하게 할까 고민하다 요청 API 까지만 생성을 해둔 후 인증의 경우
외부 서비스를 연동 후 추후 삽입 한다고 가정하였습니다.

테스트 케이스의 경우 API, 단위 로직들을 테스트 하며 진행 하였습니다.

혹시라도 위 안내대로 필요 프로그램 설치 / 세팅 후 실행이 안되거나 동작하지 않는 부분이 있을 경우 말씀 주시면 빠른 시간 내에 대응 하도록 하겠습니다
