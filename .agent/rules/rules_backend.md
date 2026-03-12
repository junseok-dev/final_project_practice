---
description: 백엔드 개발 전문 에이전트 (Python, FastAPI, WebSocket)
---

# Backend Agent Rules

## 역할 (Role)
Python, FastAPI, 데이터베이스 설계 및 API 개발을 담당하는 백엔드 전문 에이전트입니다.

## 기술 스택
- **언어**: Python 3.x
- **프레임워크**: FastAPI
- **패키지 관리**: uv (pyproject.toml)
- **린터/포매터**: Ruff

## 주요 명령어
```bash
uv sync                          # 의존성 설치
uv run run_server.py             # 서버 실행
uv run run_server.py --verbose   # 상세 로그 서버 실행
ruff check .                     # 코드 린트
ruff format .                    # 코드 포맷
```

## 코딩 규칙

### API 설계
- RESTful API 원칙 준수
- 응답 형식: `{"status": "success|error", "data": ..., "message": "..."}`
- API 버전 prefix 사용: `/api/v1/`
- HTTP 상태 코드를 올바르게 사용 (200, 201, 400, 404, 500)

### WebSocket
- 메시지 타입은 `MessageType` enum으로 정의
- 핸들러는 `_handle_*` 패턴으로 네이밍
- `_init_message_handlers()` 딕셔너리에 핸들러 등록

### 에러 처리
- WebSocket 핸들러에 `_cleanup_failed_connection` 구현
- try-except로 예외 처리 후 클라이언트에 에러 응답 전송
- 로깅은 `logging` 모듈 사용

### 설정 관리
- 설정 변경 시 `config_templates/` 기본 설정 파일도 함께 업데이트
- `config_manager/` 의 타입 안전 클래스 활용
- Breaking change는 `upgrade.py` 사용

## 주요 파일 위치
| 파일/디렉토리 | 설명 |
|---|---|
| `run_server.py` | 서버 진입점 |
| `src/open_llm_vtuber/server.py` | FastAPI 서버 |
| `src/open_llm_vtuber/routes.py` | WebSocket 라우팅 |
| `conf.yaml` | 사용자 설정 |
| `config_templates/` | 기본 설정 템플릿 |
