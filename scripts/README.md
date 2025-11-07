# Scripts

이 디렉토리는 파이프라인 실행 스크립트를 포함합니다.

## 📋 스크립트 목록

### `run_pipeline.py`

Python 기반 통합 파이프라인 스크립트입니다.

**기능:**
- ✅ Google Play 게임 수집 (ingest_play)
- ✅ 게임 랭킹 계산 (ranker)
- ✅ HTML 리포트 생성 (publish_html) - 선택사항
- ✅ 크로스 플랫폼 (Windows/Linux/macOS)
- ✅ 컬러 출력 및 진행 상황 표시
- ✅ 상세한 에러 처리

**사용법:**

```bash
# 기본 실행 (한국 신작 게임 top 50)
python scripts/run_pipeline.py

# HTML 리포트 포함
python scripts/run_pipeline.py --html

# 퍼즐 게임 top 30 + HTML
python scripts/run_pipeline.py --query puzzle --top-k 30 --html

# 미국 액션 게임 + 브라우저 자동 열기
python scripts/run_pipeline.py --query action --country US --html --open-browser

# 빠른 테스트 (10개만)
python scripts/run_pipeline.py --limit 10 --top-k 5 --html
```

**파라미터:**

| 파라미터 | 단축 | 기본값 | 설명 |
|----------|------|--------|------|
| `--query` | `-q` | `new games` | 검색 쿼리 |
| `--country` | `-c` | `KR` | 국가 코드 |
| `--language` | `-l` | `ko` | 언어 코드 |
| `--limit` | - | `120` | 수집할 게임 수 |
| `--top-k` | `-k` | `50` | 선정할 상위 게임 수 |
| `--html` | - | `False` | HTML 리포트 생성 |
| `--open-browser` | - | `False` | 브라우저에서 열기 |
| `--run-id` | - | 자동 | 커스텀 실행 ID |
| `--log-level` | - | `INFO` | 로그 레벨 |

**예시:**

```bash
# 예시 1: 일본 RPG 게임 top 100
python scripts/run_pipeline.py -q "rpg" -c JP -k 100 --html

# 예시 2: 빠른 테스트
python scripts/run_pipeline.py --limit 5 --top-k 3 --html --open-browser

# 예시 3: 디버그 모드
python scripts/run_pipeline.py --log-level DEBUG
```

---

### `run_pipeline.sh`

Linux/macOS/WSL용 bash 래퍼 스크립트입니다.

**기능:**
- 자동으로 가상환경 활성화
- Python 파이프라인 실행

**사용법:**

```bash
# 실행 권한 부여 (처음 한 번만)
chmod +x scripts/run_pipeline.sh

# 실행
./scripts/run_pipeline.sh

# 파라미터 전달
./scripts/run_pipeline.sh --query puzzle --html
./scripts/run_pipeline.sh -q action -c US -k 30 --html
```

---

## 🚀 빠른 시작 (Ubuntu WSL)

### 1. 가상환경 설정

```bash
# Python 가상환경 생성
python3 -m venv .venv

# 활성화
source .venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 파이프라인 실행

```bash
# Python으로 직접
python scripts/run_pipeline.py --html

# 또는 bash 스크립트로
chmod +x scripts/run_pipeline.sh
./scripts/run_pipeline.sh --html
```

### 3. HTML 리포트 보기

```bash
# WSL에서 Windows 브라우저로 열기
explorer.exe outputs/20251107/103252/reports/game_ranking.html

# 또는 자동으로 열기
python scripts/run_pipeline.py --html --open-browser
```

---

## 🎯 사용 시나리오

### 시나리오 1: 빠른 테스트

```bash
python scripts/run_pipeline.py --limit 10 --top-k 5 --html
```

1-2분 안에 전체 파이프라인 + HTML 리포트 생성

### 시나리오 2: 프로덕션 실행

```bash
python scripts/run_pipeline.py \
  --query "new games" \
  --country KR \
  --top-k 50 \
  --html \
  --log-level INFO
```

완전한 데이터 수집 및 리포트 생성

### 시나리오 3: 디버깅

```bash
python scripts/run_pipeline.py \
  --limit 5 \
  --log-level DEBUG
```

상세한 로그와 함께 소량 데이터로 테스트

---

## 📊 출력 구조

```
outputs/
└── 20251107/                  # 날짜
    └── 103252/                # Run ID
        ├── artifacts/
        │   ├── raw_games.json       # 1단계 출력
        │   └── ranked_games.json    # 2단계 출력
        └── reports/
            └── game_ranking.html    # 3단계 출력 (--html 옵션)
```

---

## 🔧 트러블슈팅

### WSL에서 브라우저가 안 열리는 경우

```bash
# --open-browser 대신 수동으로:
explorer.exe outputs/20251107/103252/reports/game_ranking.html

# 또는 WSL 기본 브라우저 설정
export BROWSER=wslview
python scripts/run_pipeline.py --html --open-browser
```

### 가상환경 활성화 안 되는 경우

```bash
# 명시적으로 활성화
source .venv/bin/activate

# Python 경로 확인
which python3
```

### 권한 에러

```bash
# 스크립트 실행 권한
chmod +x scripts/run_pipeline.sh

# 출력 디렉토리 권한
chmod -R 755 outputs/
```

---

## 💡 팁

1. **별칭 설정**
   ```bash
   # ~/.bashrc 또는 ~/.zshrc에 추가
   alias game-pipeline="python3 scripts/run_pipeline.py"
   
   # 사용
   game-pipeline --query puzzle --html
   ```

2. **자동 실행**
   ```bash
   # cron으로 매일 실행
   0 6 * * * cd /path/to/play-new-games && ./scripts/run_pipeline.sh --html
   ```

3. **결과 공유**
   ```bash
   # HTML 파일을 복사하여 공유
   cp outputs/20251107/103252/reports/game_ranking.html ~/shared/
   ```

---

## 🆚 PowerShell vs Python 스크립트

| 기능 | PowerShell (run-pipeline.ps1) | Python (run_pipeline.py) |
|------|-------------------------------|--------------------------|
| 플랫폼 | Windows | Windows/Linux/macOS |
| 컬러 출력 | ✅ | ✅ |
| HTML 리포트 | 별도 스크립트 | 통합 (`--html`) |
| 브라우저 열기 | 자동 | `--open-browser` 옵션 |
| 에러 처리 | ✅ | ✅ |
| 진행 상황 | 상세 | 상세 |

**권장:**
- **Windows**: PowerShell 또는 Python 둘 다 사용 가능
- **Linux/WSL**: Python 스크립트 사용
- **CI/CD**: Python 스크립트 사용 (크로스 플랫폼)

---

Happy Gaming! 🎮

