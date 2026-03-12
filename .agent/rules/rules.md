---
description: final_project_practice 워크스페이스 전체 에이전트 규칙 모음
---

# Workspace Agent Rules

`final_project_practice` 워크스페이스에서 활동하는 에이전트들의 공통 규칙 및 역할별 규칙 모음입니다.

---

## 공통 원칙 (모든 에이전트 적용)

- 작업 전 계획을 명확히 설명하고, 불명확한 요구사항은 반드시 확인합니다
- 파일 삭제, 프로덕션 배포 등 파괴적인 작업은 사용자 확인 후 실행합니다
- API 키/비밀번호 하드코딩 금지, `git push --force` 자동 실행 금지
- 사용자가 한국어로 질문하면 한국어로 답변합니다 (코드 주석은 영어 유지)

---

## 에이전트 역할 (@로 개별 호출 가능)

| 에이전트 | 호출 | 담당 영역 |
|---|---|---|
| General | `@general` | 공통 규칙, 기본 원칙 |
| Backend | `@backend` | Python, FastAPI, WebSocket, API 설계 |
| Frontend | `@frontend` | UI, Live2D 연동, WebSocket 클라이언트 |
| DevOps | `@devops` | Docker, CI/CD, 배포, 트러블슈팅 |

---

## 프로젝트 구조

```
final_project_practice/
├── .agent/
│   ├── rules/          # 에이전트 규칙 파일
│   │   ├── rules.md    # 이 파일 (전체 인덱스)
│   │   ├── general.md
│   │   ├── backend.md
│   │   ├── frontend.md
│   │   └── devops.md
│   └── workflows/      # 자동화 워크플로우
├── youtuber/           # Open-LLM-VTuber (Python/FastAPI + Live2D)
├── awesome_skills/     # Skills 인덱스
├── auto_create_video/
└── voice_test/
```

---

## 빠른 참조: 주요 명령어

```bash
# 백엔드 서버 실행
cd youtuber && uv sync && uv run run_server.py

# 코드 품질 검사
ruff check . && ruff format .

# Docker 빌드
docker build -f youtuber/dockerfile -t open-llm-vtuber .
```
