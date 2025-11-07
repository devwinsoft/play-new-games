# 🚀 빠른 시작 가이드

play-new-games 프로젝트를 빠르게 시작하는 방법입니다.

## 📋 사전 준비

1. **Python 3.8+** 설치
2. **PowerShell** (Windows에서 기본 제공)

## ⚡ 5분 안에 시작하기

### 1단계: 환경 설정 (1분)

```powershell
# 프로젝트 디렉토리로 이동
cd play-new-games

# 가상환경 생성 및 활성화
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 의존성 설치
pip install -r requirements.txt
```

### 2단계: 게임 데이터 수집 및 랭킹 (2-3분)

```powershell
# 기본 실행 (한국 신작 게임 top 50)
.\run-pipeline.ps1
```

**또는 파라미터 지정:**

```powershell
# 퍼즐 게임 top 30
.\run-pipeline.ps1 -Query "puzzle" -TopK 30

# 미국 액션 게임 top 50
.\run-pipeline.ps1 -Query "action" -Country "US" -TopK 50
```

### 3단계: HTML 리포트 생성 (1초)

파이프라인이 완료되면 출력 파일 경로가 표시됩니다:

```
랭킹 결과: outputs\20251107\103252\artifacts\ranked_games.json
```

이 경로를 사용하여 HTML 리포트 생성:

```powershell
.\run-html-report.ps1 -RankedItemsPath "outputs\20251107\103252\artifacts\ranked_games.json"
```

**브라우저가 자동으로 열리면서 결과를 시각적으로 확인할 수 있습니다!** 🎉

---

## 📊 결과 확인

### JSON 파일 (프로그래밍 방식)

```powershell
# 원본 게임 데이터
code outputs\20251107\103252\artifacts\raw_games.json

# 랭킹된 게임
code outputs\20251107\103252\artifacts\ranked_games.json
```

### HTML 리포트 (시각적)

```powershell
# 브라우저에서 열기
start outputs\20251107\103252\reports\game_ranking.html
```

---

## 🎯 예시 시나리오

### 시나리오 1: 한국 퍼즐 게임 top 20

```powershell
.\run-pipeline.ps1 -Query "puzzle" -TopK 20
.\run-html-report.ps1 -RankedItemsPath "outputs\...\ranked_games.json"
```

### 시나리오 2: 일본 RPG 게임 top 50

```powershell
.\run-pipeline.ps1 -Query "rpg" -Country "JP" -TopK 50
.\run-html-report.ps1 -RankedItemsPath "outputs\...\ranked_games.json"
```

### 시나리오 3: 빠른 테스트 (10개만)

```powershell
$env:LIMIT="10"
.\run-pipeline.ps1 -TopK 5
.\run-html-report.ps1 -RankedItemsPath "outputs\...\ranked_games.json"
```

---

## 🔧 트러블슈팅

### 문제 1: 가상환경 활성화 실패

```powershell
# PowerShell 실행 정책 변경
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 다시 시도
.\.venv\Scripts\Activate.ps1
```

### 문제 2: 패키지 설치 실패

```powershell
# pip 업그레이드
python -m pip install --upgrade pip

# 다시 설치
pip install -r requirements.txt
```

### 문제 3: 게임 수집 0개

- 다른 검색 쿼리 시도: `"action"`, `"puzzle"`, `"rpg"`
- 국가 변경: `"US"`, `"JP"`
- 인터넷 연결 확인

---

## 📚 다음 단계

1. **커스터마이징**: `run-pipeline.ps1` 파라미터 조정
2. **HTML 디자인 변경**: `skills/publish_html/handler.py` CSS 수정
3. **자동화**: 스케줄러로 주기적 실행 설정
4. **통합**: 다른 프로젝트에 결과 연동

---

## 💡 팁

1. **빠른 테스트**: `$env:LIMIT="10"`으로 설정하면 1분 안에 완료
2. **여러 쿼리**: 다른 터미널에서 동시 실행 가능
3. **히스토리**: 모든 실행 결과가 `outputs/날짜/시간/` 에 보존됨
4. **공유**: HTML 파일을 이메일이나 슬랙으로 공유

---

**준비 완료! 지금 바로 시작해보세요!** 🚀

```powershell
.\run-pipeline.ps1
```

