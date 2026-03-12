---
description: AWS 배포 처음부터 끝까지 단계별 워크플로우 (/aws-deploy)
---

# ☁️ AWS 배포 워크플로우

## 0. 시작 조건
- AWS 환경에 새로 배포하거나, 기존 서비스를 업데이트할 때

---

## 🧭 0-0. [AWS] 프로젝트 유형 파악 & 모델 추천
**투입 에이전트**: `aws-role`

> **신규 배포라면 반드시 이 단계를 먼저 진행한다.**
> 기존 서비스 업데이트라면 건너뛰어도 된다.

사용자에게 다음 5가지를 확인한 후 최적 모델을 추천한다:

```
1. 프로젝트 유형은? (포트폴리오 / 팀 프로젝트 / 상업 서비스)
2. 예상 트래픽은? (소수 / 수백 / 수천 명 이상)
3. Docker를 사용하는가?
4. 예산 범위는? (프리티어 / 월 수만원 / 그 이상)
5. 서버가 24시간 떠있어야 하는가?
```

**추천 결과를 아래 형식으로 제시:**
```
📊 프로젝트 분석 결과
- 유형: ...
- 트래픽 예상: 낮음 / 중간 / 높음
- 예산: ...

✅ 추천 모델: {모델명}
이유: {왜 이 모델인지 2줄 이내}
예상 월 비용: 약 {금액}

⚡ 대안 모델: {차선책}
```

| 유형 | 추천 |
|---|---|
| 개인 / 토이 프로젝트 | EC2 t2.micro (프리티어) |
| 팀 프로젝트 / 중소 서비스 | EC2 + Docker + ECR |
| 트래픽 급증 가능 | ECS + Fargate |
| API (간헐적 호출) | Lambda + API Gateway |
| 정적 웹사이트 | S3 + CloudFront |

사용자 승인 후 다음 단계 진행.

---

## 📌 0-1. [Doc] GitHub Issue 생성
**투입 에이전트**: `doc-role`

1. GitHub Issue 생성:
   - 제목: `[Deploy] AWS v{X.X.X} 배포`
   - 채택한 AWS 모델 명시
   - 배포 대상 서비스 및 변경사항 명시
   - 롤백 계획 첨부
2. 칸반 보드: `To Do` → `In Progress`

---


## 1. [AWS] 사전 준비 확인
**투입 에이전트**: `aws-role`

```
□ AWS CLI 인증 상태 확인 (aws sts get-caller-identity)
□ 대상 EC2 인스턴스 실행 중 확인
□ ECR 레포지토리 존재 확인
□ .env 파일 준비 완료
□ 현재 운영 중인 버전 태그 메모 (롤백 대비)
```

---

## 2. [AWS + DevOps] Docker 이미지 빌드 & 푸시
**투입 에이전트**: `aws-role`, `devops-role`

```bash
# 1. ECR 로그인
aws ecr get-login-password --region ap-northeast-2 | \
  docker login --username AWS --password-stdin {ECR주소}

# 2. 이미지 빌드
docker build -t {앱이름}:{버전태그} .

# 3. ECR에 푸시
docker tag {앱이름}:{버전태그} {ECR주소}/{앱이름}:{버전태그}
docker push {ECR주소}/{앱이름}:{버전태그}
```

**확인**: ECR 콘솔에서 이미지 푸시 확인

---

## 3. [Senior Reviewer] 배포 전 최종 승인
**투입 에이전트**: `senior-reviewer`

```
□ 보안그룹 설정 이상 없음
□ .env 환경변수 누락 없음
□ 이전 버전 이미지 태그 보존 (롤백 가능)
□ DB 마이그레이션 스크립트 준비 (필요시)
```

APPROVED → 다음 단계 / BLOCKED → 배포 중단

---

## 4. [AWS] EC2 서버 배포
**투입 에이전트**: `aws-role`

// turbo
```bash
# EC2 SSH 접속
ssh -i {키파일}.pem ec2-user@{EC2_퍼블릭IP}

# ECR 최신 이미지 Pull
aws ecr get-login-password --region ap-northeast-2 | \
  docker login --username AWS --password-stdin {ECR주소}
docker pull {ECR주소}/{앱이름}:{버전태그}

# 기존 컨테이너 중단 & 새 버전 실행
docker stop {컨테이너명} && docker rm {컨테이너명}
docker run -d \
  --name {컨테이너명} \
  --env-file .env \
  -p {호스트포트}:{컨테이너포트} \
  {ECR주소}/{앱이름}:{버전태그}
```

---

## 5. [AWS] DB 마이그레이션 (필요시)
**투입 에이전트**: `aws-role`, `backend-role`

```bash
# 컨테이너 내부에서 마이그레이션 실행
docker exec -it {컨테이너명} python manage.py migrate
# 또는
docker exec -it {컨테이너명} {마이그레이션 명령어}
```

---

## 6. [AWS] 배포 후 검증
**투입 에이전트**: `aws-role`

```bash
# 컨테이너 정상 실행 확인
docker ps | grep {컨테이너명}

# 최근 로그 확인 (에러 없는지)
docker logs {컨테이너명} --tail 50

# 헬스체크
curl http://localhost:{포트}/api/health

# 외부 접속 확인 (퍼블릭 IP 또는 도메인)
curl http://{퍼블릭IP 또는 도메인}/api/health
```

**모니터링 체크리스트**:
```
□ 200 OK 응답 확인
□ 에러 로그 없음
□ DB 연결 정상
□ 기존 기능 Smoke Test
```

---

## 7. [Doc] 배포 완료 기록
**투입 에이전트**: `doc-role`

1. `CHANGELOG.md` 배포 버전 항목 추가
2. 배포 일시, 버전 태그, 서버 정보 기록
3. GitHub Issue 완료 코멘트 + `Done` 이동 + Close
4. 완료 보고

---

## ⚠️ 롤백 절차
```bash
# 이전 버전 이미지로 즉시 롤백
docker stop {컨테이너명} && docker rm {컨테이너명}
docker run -d \
  --name {컨테이너명} \
  --env-file .env \
  -p {호스트포트}:{컨테이너포트} \
  {ECR주소}/{앱이름}:{이전버전태그}

# 롤백 후 /bug-fix 워크플로우 시작
```

---

## ✅ 완료 기준
- GitHub Issue `Done` 이동 + Close 확인
- 외부 도메인/IP 접속 정상 (200 OK)
- 에러 로그 없음
- 배포 기록 문서화 완료
