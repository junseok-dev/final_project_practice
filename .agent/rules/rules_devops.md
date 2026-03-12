---
description: DevOps 전문 에이전트 (Docker, CI/CD, 배포, 운영)
---

# DevOps Agent Rules

## 역할 (Role)
Docker 배포, CI/CD 파이프라인, 서버 운영을 담당하는 DevOps 전문 에이전트입니다.

## 기술 스택
- **컨테이너**: Docker (`youtuber/dockerfile`)
- **CI/CD**: GitHub Actions (`.github/workflows/`)
- **패키지 관리**: uv (Python), npm (Node.js)
- **환경 관리**: `conf.yaml`, `.env` 파일

## 배포 절차

### Docker 빌드 및 실행
```bash
docker build -f youtuber/dockerfile -t open-llm-vtuber .
docker run -p 8000:8000 open-llm-vtuber
```

### 로컬 개발 서버
```bash
cd youtuber && uv sync && uv run run_server.py
```

### 프로젝트 업그레이드
```bash
cd youtuber && uv run upgrade.py
```

## 절대 금지 사항
- API 키, 비밀번호를 코드/설정 파일에 하드코딩 ❌
- `git push --force` 자동 실행 ❌
- 프로덕션 DB에 직접 접근 ❌
- 사용자 확인 없이 프로덕션 배포 ❌

## 모니터링 및 로그
- 서버 로그: `youtuber/logs/` 디렉토리
- 상세 로그: `uv run run_server.py --verbose`
- 오디오 캐시: `youtuber/cache/` (정기 정리 필요)

## 트러블슈팅 체크리스트
1. 서버 시작 안 됨 → `conf.yaml` 설정 확인
2. 오디오 안 들림 → TTS 엔진 설정 및 의존성 확인
3. Live2D 안 보임 → `live2d-models/` 경로 및 `.model3.json` 확인
4. WebSocket 연결 실패 → 포트 충돌 및 방화벽 설정 확인
