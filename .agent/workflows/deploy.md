---
description: 배포 전 체크리스트 및 배포 워크플로우 (DevOps → Review → Doc)
---

# 🚀 배포 워크플로우

## 0. 시작 조건
- 새 기능 개발 완료 후 배포 요청
- 핫픽스 배포 필요 시

---

## 📌 0-1. [Doc] GitHub Issue 생성
**투입 에이전트**: `doc-role`

1. GitHub Issue 생성:
   - 제목: `[Deploy] v{X.X.X} 배포`
   - 배포 대상 기능/수정 목록 첨부
   - 롤백 계획 명시
2. 칸반 보드: `To Do` → `In Progress`

---

## 1. [DevOps] 배포 전 준비
**투입 에이전트**: `devops-role`

### 필수 체크리스트
```
□ 모든 기능 테스트 통과 확인
□ .env 파일 및 환경변수 설정 확인
□ .env.example 최신화
□ DB 마이그레이션 스크립트 준비
□ Docker 이미지 빌드 성공 확인
□ 헬스체크 엔드포인트 (/api/health) 응답 확인
□ 이전 버전 이미지 태그 보존 (롤백 대비)
□ 롤백 계획 수립
```

### 배포 환경별 주의사항
| 환경 | 주의사항 |
|---|---|
| 로컬 | `docker-compose up` 테스트 |
| 스테이징 | 운영과 동일한 환경변수 사용 |
| 운영(Production) | Senior Reviewer 최종 승인 필수 |

---

## 2. [Senior Reviewer] 배포 최종 승인
**투입 에이전트**: `senior-reviewer`

1. 배포 체크리스트 검토
2. 보안 취약점 최종 점검:
   ```
   □ 비밀키 노출 없음
   □ HTTPS 설정 확인
   □ CORS 설정 적절
   □ 불필요한 포트 노출 없음
   ```
3. APPROVED → 배포 진행
4. BLOCKED → 배포 중단, 이슈 해결 후 재시도

---

## 3. [DevOps] 배포 실행
**투입 에이전트**: `devops-role`

// turbo
1. Docker 이미지 빌드 및 푸시
2. 서비스 배포 (무중단 배포 권장)
3. 헬스체크 통과 확인
4. 주요 기능 Smoke Test

### 배포 후 모니터링 (5분)
```
□ 서비스 응답 정상 (200 OK)
□ 에러 로그 없음
□ DB 연결 정상
□ 메모리/CPU 정상 범위
```

---

## 4. [Doc] 배포 기록
**투입 에이전트**: `doc-role`

1. `CHANGELOG.md` 배포 버전 항목 추가
2. 배포 일시, 버전, 변경사항 기록
3. GitHub Issue 완료 코멘트 작성 + `Done` 이동 + Close
4. 완료 보고

---

## ⚠️ 롤백 절차
```
1. 이전 이미지 태그로 즉시 롤백
2. 에러 원인 분석 (bug-fix 워크플로우 시작)
3. 수정 후 재배포
```

## ✅ 완료 기준
- GitHub Issue `Done` 이동 + Close 확인
- 헬스체크 통과
- Smoke Test 정상
- 배포 기록 문서화 완료
