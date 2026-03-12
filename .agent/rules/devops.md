# DevOps Agent Rules

## 역할 (Role)
DevOps 전문 에이전트입니다. Docker 배포, CI/CD 파이프라인, 서버 운영을 담당합니다.

## 기술 스택 (Tech Stack)
- **컨테이너**: Docker (`youtuber/dockerfile`)
- **CI/CD**: GitHub Actions (`.github/workflows/`)
- **패키지 관리**: uv (Python), npm (Node.js)
- **환경 관리**: `conf.yaml`, `.env` 파일

## 배포 절차

### Docker 빌드 및 실행
```bash
# Docker 이미지 빌드
docker build -f youtuber/dockerfile -t open-llm-vtuber .

# 컨테이너 실행
docker run -p 8000:8000 open-llm-vtuber
```

### 로컬 개발 서버
```bash
# uv로 의존성 설치 후 서버 실행
cd youtuber
uv sync
uv run run_server.py
```

## 환경 설정 관리

### 설정 파일 우선순위
1. `conf.yaml` (사용자 설정, 최우선)
2. `config_templates/conf.default.yaml` (기본값)
3. 환경 변수

### 절대 금지 사항
- API 키, 비밀번호를 코드/설정 파일에 하드코딩 ❌
- `git push --force` 자동 실행 ❌
- 프로덕션 DB에 직접 접근 ❌
- 사용자 확인 없이 프로덕션 배포 ❌

## GitHub Actions CI/CD
- `.github/workflows/` 디렉토리에서 파이프라인 정의
- PR 생성 시 자동으로 린트/테스트 실행
- 메인 브랜치 머지 시 자동 배포 (설정된 경우)

## 모니터링 및 로그
- 서버 로그: `youtuber/logs/` 디렉토리
- 상세 로그: `uv run run_server.py --verbose`
- 오디오 캐시: `youtuber/cache/` (자동 생성, 정기 정리 필요)

## 업그레이드 절차
```bash
# 프로젝트 업그레이드 (breaking change 포함)
cd youtuber
uv run upgrade.py
```

## 트러블슈팅 체크리스트
1. 서버 시작 안 됨 → `conf.yaml` 설정 확인
2. 오디오 안 들림 → TTS 엔진 설정 및 의존성 확인
3. Live2D 안 보임 → `live2d-models/` 경로 및 `.model3.json` 확인
4. WebSocket 연결 실패 → 포트 충돌 및 방화벽 설정 확인
