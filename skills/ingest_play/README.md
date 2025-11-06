# ingest_play

Google Play 스토어에서 신작 게임 메타데이터를 수집하여 표준 스키마로 정규화하는 스킬입니다.

## 🚀 빠른 시작

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

또는 가상환경을 사용하는 경우:

```bash
# 가상환경 생성 (처음 한 번만)
python -m venv .venv

# 가상환경 활성화
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat
# Linux/Mac:
source .venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 기본 실행

```bash
python skills/ingest_play/handler.py
```

기본값으로 한국(KR) 스토어에서 "new games" 검색어로 최대 120개의 게임을 수집합니다.

### 3. 커스텀 파라미터로 실행

```bash
# 환경 변수로 파라미터 전달
QUERY="rpg games" COUNTRY="US" LANGUAGE="en" LIMIT=50 python skills/ingest_play/handler.py

# 또는 Windows PowerShell:
$env:QUERY="rpg games"; $env:COUNTRY="US"; $env:LANGUAGE="en"; $env:LIMIT="50"; python skills/ingest_play/handler.py
```

## 📋 파라미터

| 파라미터 | 타입 | 기본값 | 설명 |
|---------|------|--------|------|
| `QUERY` | string | `"new games"` | 검색 쿼리 |
| `COUNTRY` | string | `"KR"` | 국가 코드 (KR, US, JP 등) |
| `LANGUAGE` | string | `"ko"` | 언어 코드 (ko, en, ja 등) |
| `LIMIT` | integer | `120` | 수집할 최대 게임 수 |
| `LOG_LEVEL` | string | `"INFO"` | 로그 레벨 (DEBUG, INFO, WARNING, ERROR) |
| `RUN_ID` | string | 자동 생성 | 실행 ID (선택사항) |

## 📁 출력

수집된 데이터는 다음 경로에 JSON 파일로 저장됩니다:

```
outputs/{날짜}/{run_id}/artifacts/raw_games.json
```

예: `outputs/20251106/142530/artifacts/raw_games.json`

## 📊 출력 스키마

```json
[
  {
    "package_name": "com.example.game",
    "title": "Game Title",
    "developer": "Dev Studio",
    "genre": "Action",
    "description": "게임 설명...",
    "rating": 4.6,
    "ratings_count": 1234,
    "installs": 50000,
    "release_date": "2025-11-03",
    "icon_url": "https://...",
    "screenshots": ["https://...", "..."],
    "store_url": "https://play.google.com/store/apps/details?id=com.example.game",
    "price": 0,
    "free": true,
    "content_rating": "Everyone",
    "updated": "2025-11-05"
  }
]
```

## 🧪 테스트

```bash
# 단위 테스트 실행
python -m pytest skills/ingest_play/tests/ -v

# 또는 unittest로:
python -m unittest discover skills/ingest_play/tests/
```

## 📚 사용 예시

### 예시 1: 한국 신작 게임 수집

```bash
python skills/ingest_play/handler.py
```

### 예시 2: 미국 RPG 게임 수집

```bash
QUERY="rpg" COUNTRY="US" LANGUAGE="en" LIMIT=100 python skills/ingest_play/handler.py
```

### 예시 3: 일본 액션 게임 수집

```bash
QUERY="アクションゲーム" COUNTRY="JP" LANGUAGE="ja" python skills/ingest_play/handler.py
```

### 예시 4: 디버그 모드로 실행

```bash
LOG_LEVEL="DEBUG" python skills/ingest_play/handler.py
```

## 🔧 트러블슈팅

### google-play-scraper 설치 실패

```bash
# 최신 pip로 업그레이드
python -m pip install --upgrade pip

# 다시 설치
pip install google-play-scraper
```

### Rate Limiting 에러

Google Play Store의 요청 제한에 걸린 경우, 잠시 기다린 후 다시 시도하세요.
또는 `LIMIT` 값을 줄여서 실행하세요.

### 데이터가 수집되지 않음

1. 인터넷 연결 확인
2. 검색 쿼리 변경 (QUERY 파라미터)
3. 국가/언어 설정 확인
4. `LOG_LEVEL=DEBUG`로 상세 로그 확인

## 🏗️ 아키텍처

```
skills/ingest_play/
├── handler.py           # 메인 실행 엔트리포인트
├── normalize.py         # 데이터 정규화 및 필터링
├── adapters/
│   └── play_store.py   # Google Play Store API 래퍼
├── tests/              # 단위 테스트
└── README.md           # 이 파일
```

## 📝 라이선스

이 프로젝트의 일부입니다.

