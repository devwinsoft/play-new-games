# Claude Custom Commands

이 디렉토리는 Cursor/Claude에서 사용할 수 있는 커스텀 슬래시 커맨드를 포함합니다.

## 📋 사용 가능한 커맨드

### 🎮 game-pipeline

Google Play에서 게임을 수집하고 점수를 계산하여 상위 게임을 선정하는 전체 파이프라인입니다.

**사용법:**
```
/game-pipeline
/game-pipeline "puzzle" "KR" 30
/game-pipeline "action" "US" 50
```

**파라미터:**
- `$1` (query): 검색 쿼리 (기본값: "new games")
- `$2` (country): 국가 코드 (기본값: "KR")
- `$3` (top_k): 최종 선정 게임 수 (기본값: 50)

**필수 환경:**
- Python 가상환경 활성화
- 필수 패키지 설치 (`requirements.txt`)

**출력:**
- `raw_games.json` - 수집된 원본 게임 데이터
- `ranked_games.json` - 점수 계산 및 랭킹된 최종 결과

**예상 소요 시간:** 2-5분 (120개 게임 기준)

---

## 🚀 빠른 시작

### 1. 환경 설정

```powershell
# 가상환경 활성화
.\.venv\Scripts\Activate.ps1
```

### 2. 커맨드 실행

#### Cursor/Claude에서:
```
/game-pipeline
```

#### PowerShell에서:
```powershell
.\run-pipeline.ps1
.\run-pipeline.ps1 -Query "puzzle" -TopK 30
```

---

## 📖 커맨드 구조

각 커맨드는 다음 섹션을 포함합니다:

```markdown
---
allowed-tools: [도구 목록]
description: 커맨드 설명
argument-hint: [인수 힌트]
model: sonnet
---

# 커맨드 이름

## 변수
- 동적/정적 변수 정의

## 지침
- 실행 규칙 및 제약사항

## 워크플로우
- 단계별 작업 항목

## 테스트 스위트
- 단위/통합/종단 간 테스트

## 최종 결과물
- 출력 파일 및 보고서
```

---

## 🛠️ 새 커맨드 만들기

`meta-prompt-generator` 스킬을 사용하여 새 커맨드를 자동 생성할 수 있습니다:

```
"[원하는 작업 설명]을 하는 커맨드를 만들어줘"
```

예시:
```
"React와 TypeScript로 TODO 앱을 만드는 커맨드를 만들어줘"
"CSV 파일을 분석하고 시각화하는 커맨드를 만들어줘"
```

---

## 📚 추가 자료

- 프로젝트 README: `../../README.md`
- 스킬 문서: `../../skills/*/SKILL.md`
- 테스트 가이드: `../../TEST_GUIDE.md`

---

## 💡 팁

1. **파라미터 활용**: 커맨드에 파라미터를 전달하여 동작 커스터마이징
2. **중간 결과 보존**: 각 단계의 출력이 `outputs/` 디렉토리에 저장됨
3. **에러 복구**: 실패한 단계부터 재시작 가능
4. **병렬 실행**: 서로 다른 파라미터로 여러 커맨드 동시 실행 가능

---

Made with ❤️ using Claude

