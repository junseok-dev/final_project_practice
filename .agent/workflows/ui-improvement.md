---
description: UI/UX 개선 워크플로우 (Frontend UI Polish → Review → Doc)
---

# ✨ UI 개선 워크플로우

## 0. 시작 조건
- "화면이 이상하다", "디자인을 개선해달라", 반응형 깨짐 등

---

## 📌 0-1. [Doc] GitHub Issue 생성
**투입 에이전트**: `doc-role`

1. GitHub Issue 생성:
   - 제목: `[UI] {개선 내용 요약}`
   - 개선 전 상태 설명 (스크린샷 첨부 권스)
   - 목표 화면 크기 명시
2. 칸반 보드: `To Do` → `In Progress`

---

## 1. [Frontend] UI Polish 단계
**투입 에이전트**: `frontend-role`

### 현황 파악
1. 현재 화면 상태 확인 (스크린샷 또는 코드 리뷰)
2. 개선 목표 명확화:
   ```
   개선 전: ...
   개선 목표: ...
   영향 파일: ...
   ```

### 개선 작업
1. 레이아웃 및 간격 조정 (8px 단위 시스템)
2. 색상 및 타이포그래피 최적화
3. 반응형 대응 (모바일 → 태블릿 → 데스크탑)
4. 인터랙션 개선 (hover, focus, transition)
5. 로딩/에러 상태 UI 추가

### 체크리스트
```
□ 모바일 (320px~) 정상
□ 태블릿 (768px~) 정상
□ 데스크탑 (1024px~) 정상
□ hover/focus 상태 있음
□ 로딩/에러 상태 처리
```

---

## 2. [Senior Reviewer] 시각적 검토
**투입 에이전트**: `senior-reviewer`

1. UI 체크리스트 점검
2. 사용자 동선이 직관적인지 검토
3. APPROVED / CHANGES REQUESTED 발행

---

## 3. [Doc] 변경 기록
**투입 에이전트**: `doc-role`

1. `CHANGELOG.md`에 Changed 항목 추가
2. 주요 디자인 결정 사항 주석으로 기록
3. GitHub Issue 완료 코멘트 작성 + `Done` 이동 + Close
4. 완료 보고

---

## ✅ 완료 기준
- GitHub Issue `Done` 이동 + Close 확인
- 3개 화면 크기에서 레이아웃 정상 확인
- Senior Reviewer APPROVED
