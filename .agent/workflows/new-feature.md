---
description: 새 기능 개발 전체 파이프라인 (PM → Backend/Frontend → Review → Doc)
---

# 🆕 새 기능 개발 워크플로우

## 0. 시작 조건
- 사용자가 새 기능 또는 새 프로젝트를 요청했을 때

---

## 📌 0-1. [Doc] GitHub Issue 생성
**투입 에이전트**: `doc-role`

1. GitHub Issue 생성:
   - 제목: `[Feature] {기능명 요약}`
   - 완료 조건 체크리스트 작성
   - blueprint.md 링크 첨부 (완성 후)
2. 칸반 보드: `To Do` → `In Progress`

---

## 1. [PM] 설계 단계
**투입 에이전트**: `pm-role`

1. 요구사항 명확화 (모호한 부분은 사용자에게 질문)
2. `blueprint.md` 작성:
   - 기술 스택 선택 + 이유
   - 폴더 구조 정의
   - DB 스키마 (필요시)
   - API 엔드포인트 목록
   - 에이전트별 작업 분담
3. 사용자에게 `blueprint.md` 검토 요청
4. 승인 후 다음 단계 진행

---

## 2. [Backend + Frontend] 구현 단계
**투입 에이전트**: `backend-role`, `frontend-role` (병렬 진행)

### Backend
1. DB 모델/마이그레이션 작성
2. 비즈니스 로직 구현
3. API 엔드포인트 구현
4. 기본 에러 핸들링 적용

### Frontend
1. 라우팅 구조 설정
2. 공통 레이아웃 구현
3. 페이지/컴포넌트 구현
4. API 연동
5. UI Polish: 디자인 완성도 점검

---

## 3. [Senior Reviewer] 리뷰 단계
**투입 에이전트**: `senior-reviewer`

1. 리뷰 체크리스트 전체 점검
2. 결과 발행: APPROVED / CHANGES REQUESTED
3. CHANGES REQUESTED → 해당 에이전트 수정 후 재리뷰
4. APPROVED → 다음 단계 진행

---

## 4. [Doc] 문서화 단계
**투입 에이전트**: `doc-role`

1. `README.md` 업데이트
2. `CHANGELOG.md` 항목 추가
3. 새 함수/클래스 Docstring 작성
4. 완료 보고

---

## 5. [Doc] GitHub Issue 닫기
**투입 에이전트**: `doc-role`

1. Issue에 완료 코멘트 작성:
   - 완료 일시, 관련 커밋, 변경 요약
   - 문서 업데이트 항목 체크
2. 칸반 보드: `In Progress` → `Done`
3. Issue Close

---

## ✅ 완료 기준
- GitHub Issue `Done` 이동 + Close 확인
- Senior Reviewer APPROVED 확인
- 문서 업데이트 완료
- 사용자에게 완료 보고
