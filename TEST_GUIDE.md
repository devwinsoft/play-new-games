# ingest_play 스킬 테스트 가이드

이 문서는 `ingest_play` 스킬을 직접 테스트하는 방법을 안내합니다.

## 📋 사전 준비

### 1. Python 환경 확인

```bash
python --version
```

Python 3.8 이상이 필요합니다.

### 2. 가상환경 생성 및 활성화 (권장)

**Windows PowerShell:**
```powershell
# 가상환경 생성
python -m venv .venv

# 가상환경 활성화
.venv\Scripts\Activate.ps1

# 활성화 확인 (프롬프트 앞에 (.venv) 표시됨)
```

**Windows CMD:**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

설치되는 패키지:
- `google-play-scraper`: Google Play Store 데이터 수집
- `python-dateutil`: 날짜 파싱
- `colorlog`: 컬러 로그 출력

## 🧪 테스트 시나리오

### 테스트 1: 기본 실행 (한국 신작 게임)

가장 기본적인 테스트입니다.

```bash
python skills/ingest_play/handler.py
```

**예상 결과:**
- 콘솔에 진행 상황 로그 출력
- 약 1-2분 소요 (네트워크 속도에 따라 다름)
- `outputs/YYYYMMDD/HHMMSS/artifacts/raw_games.json` 파일 생성
- 최종적으로 수집된 게임 개수 출력

### 테스트 2: 소량 데이터로 빠른 테스트

테스트 시간을 단축하려면 LIMIT을 낮춰서 실행하세요.

```bash
# PowerShell
$env:LIMIT="10"; python skills/ingest_play/handler.py

# CMD (한 줄씩 실행)
set LIMIT=10
python skills/ingest_play/handler.py
```

**예상 결과:**
- 약 10-20초 내에 완료
- 10개 이하의 게임 데이터 수집

### 테스트 3: 다른 검색 쿼리

```bash
# PowerShell
$env:QUERY="puzzle"; $env:LIMIT="20"; python skills/ingest_play/handler.py

# CMD
set QUERY=puzzle
set LIMIT=20
python skills/ingest_play/handler.py
```

### 테스트 4: 미국 스토어 테스트

```bash
# PowerShell
$env:COUNTRY="US"; $env:LANGUAGE="en"; $env:LIMIT="15"; python skills/ingest_play/handler.py

# CMD
set COUNTRY=US
set LANGUAGE=en
set LIMIT=15
python skills/ingest_play/handler.py
```

### 테스트 5: 디버그 모드

문제가 발생하면 디버그 모드로 상세 로그를 확인하세요.

```bash
# PowerShell
$env:LOG_LEVEL="DEBUG"; $env:LIMIT="5"; python skills/ingest_play/handler.py

# CMD
set LOG_LEVEL=DEBUG
set LIMIT=5
python skills/ingest_play/handler.py
```

## 📊 결과 확인

### 1. 출력 파일 찾기

실행이 완료되면 콘솔에 출력 파일 경로가 표시됩니다:

```
Output file: C:\Users\USER\Documents\Projects\play-new-games\outputs\20251106\142530\artifacts\raw_games.json
```

### 2. JSON 파일 확인

생성된 JSON 파일을 텍스트 에디터나 VS Code로 열어보세요.

**구조 확인:**
```json
[
  {
    "package_name": "com.example.game",
    "title": "게임 이름",
    "developer": "개발사",
    "genre": "장르",
    "rating": 4.5,
    "ratings_count": 1000,
    "installs": 10000,
    "release_date": "2025-11-01",
    ...
  }
]
```

### 3. 데이터 검증

확인할 사항:
- ✅ 배열 형태인가?
- ✅ 각 게임이 `package_name`, `title` 필드를 가지고 있는가?
- ✅ 중복된 `package_name`이 없는가?
- ✅ 게임만 포함되어 있는가? (다른 앱은 필터링되었는가?)

## 🧪 단위 테스트 실행

코드 수준의 테스트를 실행하려면:

```bash
# unittest로 실행
python -m unittest discover skills/ingest_play/tests/ -v

# 또는 특정 테스트만:
python -m unittest skills.ingest_play.tests.test_normalize -v
```

## ❗ 문제 해결

### 문제 1: ModuleNotFoundError: No module named 'google_play_scraper'

**해결:**
```bash
pip install google-play-scraper
```

### 문제 2: 데이터가 수집되지 않음 (0개)

**원인:**
- 네트워크 문제
- Google Play Store 접근 제한
- 검색 쿼리가 결과가 없음

**해결:**
1. 인터넷 연결 확인
2. 다른 검색 쿼리 시도: `QUERY="action"`
3. VPN 사용 (국가별 접근 제한이 있을 수 있음)

### 문제 3: Rate limiting 에러

**해결:**
- 10-30분 정도 기다린 후 재시도
- `LIMIT` 값을 낮춰서 실행 (예: `LIMIT=30`)

### 문제 4: Permission denied (outputs 폴더)

**해결:**
```bash
# outputs 폴더가 없으면 생성
mkdir outputs
```

## 📈 성공 기준

테스트가 성공했다면:

- ✅ 에러 없이 실행 완료
- ✅ JSON 파일이 생성됨
- ✅ JSON 파일이 유효한 형식 (배열)
- ✅ 게임 데이터가 1개 이상 포함
- ✅ 각 게임이 필수 필드를 포함 (`package_name`, `title`, `developer` 등)
- ✅ 중복 제거 완료

## 🎯 다음 단계

`ingest_play` 스킬이 정상 동작하면, 다음 스킬들과 연계할 수 있습니다:

1. **enrich_llm**: 수집된 게임을 LLM으로 태깅 및 요약
2. **ranker**: 게임을 점수화하고 랭킹
3. **publish**: 결과를 PPT나 다른 형식으로 발행

## 💡 팁

1. **빠른 테스트**: 처음엔 `LIMIT=5`로 시작하여 동작 확인
2. **디버깅**: 문제 발생 시 `LOG_LEVEL=DEBUG` 사용
3. **다양한 쿼리**: 여러 검색어로 테스트 (puzzle, rpg, action, casual 등)
4. **결과 비교**: 다른 국가(US, JP)의 결과와 비교

## 📞 도움이 필요하면

1. 로그 메시지 확인
2. `LOG_LEVEL=DEBUG`로 상세 정보 수집
3. 에러 메시지와 함께 질문

Happy Testing! 🎮

