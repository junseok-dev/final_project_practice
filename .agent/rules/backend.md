# Backend Agent Rules

## 역할 (Role)
백엔드 개발 전문 에이전트입니다. Python, FastAPI, 데이터베이스 설계 및 API 개발을 담당합니다.

## 기술 스택 (Tech Stack)
- **언어**: Python 3.x
- **프레임워크**: FastAPI
- **패키지 관리**: uv (pyproject.toml)
- **린터/포매터**: Ruff
- **서버**: `run_server.py` (FastAPI + WebSocket)

## 개발 명령어
```bash
# 의존성 설치
uv sync

# 서버 실행
uv run run_server.py

# 상세 로그 서버 실행
uv run run_server.py --verbose

# 코드 린트
ruff check .

# 코드 포맷
ruff format .
```

## 코딩 규칙 (Coding Standards)

### API 설계
- RESTful API 원칙을 준수합니다
- 응답 형식: `{"status": "success|error", "data": ..., "message": "..."}`
- API 버전 prefix 사용: `/api/v1/`
- HTTP 상태 코드를 올바르게 사용합니다 (200, 201, 400, 404, 500)

### WebSocket
- 메시지 타입은 `MessageType` enum을 통해 정의합니다
- 핸들러는 `_handle_*` 패턴으로 네이밍합니다
- `_init_message_handlers()` 딕셔너리에 핸들러를 등록합니다

### 에러 처리
- 모든 WebSocket 핸들러에 `_cleanup_failed_connection` 구현
- try-except로 예외를 처리하고 클라이언트에 에러 응답 전송
- 로깅은 `logging` 모듈 사용

### 설정 관리
- 설정 변경 시 `config_templates/` 의 기본 설정 파일도 함께 업데이트
- `config_manager/` 의 타입 안전 클래스를 활용
- Breaking change는 `upgrade.py` 업그레이드 시스템 사용

### 엔진 추가 패턴
1. 적절한 디렉토리에 인터페이스 파일 생성 (예: `asr_interface.py`)
2. 기존 패턴을 따라 구체 클래스 구현
3. 팩토리 클래스에 추가 (예: `asr_factory.py`)
4. `config_manager/` 에 설정 클래스 업데이트

## 주요 파일 위치
| 파일/디렉토리 | 설명 |
|---|---|
| `run_server.py` | 서버 진입점 |
| `src/open_llm_vtuber/server.py` | FastAPI 서버 |
| `src/open_llm_vtuber/routes.py` | WebSocket 라우팅 |
| `conf.yaml` | 사용자 설정 |
| `config_templates/` | 기본 설정 템플릿 |
| `characters/` | 캐릭터 정의 |

## 테스트 및 품질
- PR 전 반드시 `ruff check .` 통과 확인
- WebSocket 기능은 웹 인터페이스로 수동 테스트
- GitHub Actions CI/CD 파이프라인 확인
