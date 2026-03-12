---
description: 버그 수정 워크플로우 (에러 감지 → Fix → Review → Doc)
---

# 🐛 버그 수정 워크플로우

## 0. 시작 조건
- 에러 로그 발생, 기능 오동작, 사용자 버그 리포트 접수 시

---

## 📌 0-1. [Doc] GitHub Issue 생성
**투입 에이전트**: `doc-role`

1. GitHub Issue 생성:
   - 제목: `[Bug] {증상 요약}`
   - 재현 조건 및 에러 로그 첨부
   - 영향 범위 명시
2. 칸반 보드: `To Do` → `In Progress`

---

## 1. [Fix] 원인 분석
**투입 에이전트**: `backend-role` 또는 `devops-role` (에러 유형에 따라)

| 에러 유형 | 투입 에이전트 |
|---|---|
| 서버 500 에러, API 오동작 | `backend-role` |
| Docker 실패, 배포 에러 | `devops-role` |
| UI 깨짐, 프론트 에러 | `frontend-role` |

### 분석 프로세스
1. 에러 로그 전문 수집 및 읽기
2. 재현 조건 파악
3. 근본 원인(Root Cause) 명시:
   ```
   ## 원인 분석
   - 증상: ...
   - 원인: ...
   - 영향 범위: ...
   ```
4. 수정 코드 작성 + 방어 코드 추가
5. 재발 방지 주석 작성

---

## 2. [Senior Reviewer] 수정 검토
**투입 에이전트**: `senior-reviewer`

1. 수정 코드가 근본 원인을 해결했는지 확인
2. 수정으로 인한 부작용(regression) 검토
3. APPROVED / CHANGES REQUESTED 발행

---

## 3. [Doc] 버그 기록
**투입 에이전트**: `doc-role`

1. `CHANGELOG.md`에 Fixed 항목 추가
2. 재발 방지를 위한 주석/문서 추가
3. GitHub Issue 완료 코멘트 작성 + `Done` 이동 + Close
4. 완료 보고

---

## ✅ 완료 기준
- GitHub Issue `Done` 이동 + Close 확인
- 에러 재현 불가 확인
- 원인 분석 문서화 완료
- Senior Reviewer APPROVED
