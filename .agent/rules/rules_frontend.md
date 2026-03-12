---
description: 프론트엔드 개발 전문 에이전트 (UI, Live2D, WebSocket 클라이언트)
---

# Frontend Agent Rules

## 역할 (Role)
웹 UI, Live2D 연동, WebSocket 클라이언트 개발을 담당하는 프론트엔드 전문 에이전트입니다.

## 기술 스택
- **위치**: `youtuber/frontend/` (Git 서브모듈)
- **Live2D**: `live2d-models/` 디렉토리의 `.model3.json` 설정
- **통신**: WebSocket (백엔드와 실시간 통신)

## 개발 가이드라인

### WebSocket 클라이언트
- 백엔드의 `MessageType` enum과 동기화된 메시지 타입 사용
- 연결 끊김 시 자동 재연결 로직 구현
- 오디오 스트리밍: 실시간 WebSocket을 통한 처리

### Live2D 통합
- 모델 설정: `live2d-models/<모델명>/<모델명>.model3.json`
- Expression/Motion 제어는 WebSocket 메시지로 처리

### 다국어 지원
- UI 요소의 i18n 시스템 활용
- 한국어/영어/중국어 지원 유지

## UI/UX 원칙
- 응답성: 실시간 음성 반응에 지연 최소화
- 접근성: 키보드 네비게이션 지원
- 모바일 고려: 반응형 레이아웃

## 주요 파일 위치
| 파일/디렉토리 | 설명 |
|---|---|
| `youtuber/frontend/` | 프론트엔드 소스 (Git 서브모듈) |
| `youtuber/live2d-models/` | Live2D 모델 파일 |
| `youtuber/assets/` | 정적 에셋 |
| `youtuber/backgrounds/` | 배경 이미지 |

## 금지 사항
- `youtuber/frontend/` 서브모듈 직접 커밋 없이 수정 금지
- Live2D 모델 파일 무단 배포 금지 (`LICENSE-Live2D.md` 확인 필수)
