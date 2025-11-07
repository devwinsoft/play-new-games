# Play New Games

Google Play 스토어에서 신작 게임을 수집하고, LLM으로 분석하여, 추천 게임을 선정하는 자동화 시스템입니다.

## 🎯 프로젝트 개요

이 프로젝트는 다음 과정을 자동화합니다:

1. **수집(Ingest)**: Google Play에서 신작 게임 메타데이터 수집
2. **랭킹(Rank)**: 신규성/품질/인기도 기반 점수 계산 및 순위 선정
3. **발행(Publish)**: 결과를 HTML 리포트로 시각화

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 가상환경 생성 및 활성화 (Windows PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# 의존성 설치
pip install -r requirements.txt
```

### 2. 전체 파이프라인 실행

#### Windows (PowerShell)

```powershell
# 전체 파이프라인 (수집 → 랭킹)
.\run-pipeline.ps1

# 또는 파라미터 지정
.\run-pipeline.ps1 -Query "puzzle" -TopK 30

# HTML 리포트 생성
.\run-html-report.ps1 -RankedItemsPath "outputs\20251107\103252\artifacts\ranked_games.json"
```

#### Linux/WSL/macOS (Python 통합 스크립트)

```bash
# 가상환경 활성화
source .venv/bin/activate

# 전체 파이프라인 + HTML 리포트
python pipelines/run_pipeline.py --html

# 퍼즐 게임 top 30
python pipelines/run_pipeline.py --query puzzle --top-k 30 --html

# 빠른 테스트 (10개만)
python pipelines/run_pipeline.py --limit 10 --top-k 5 --html --open-browser
```

자세한 내용은 `pipelines/README.md` 및 `pipelines/WSL_TEST_GUIDE.md`를 참조하세요.

## 📁 프로젝트 구조

```
play-new-games/
├── .cursor/              # Cursor IDE 설정
├── skills/              # 모든 스킬 모듈
│   ├── ingest_play/     # 게임 데이터 수집
│   ├── ranker/          # 랭킹 계산
│   ├── publish_html/    # HTML 리포트 생성
│   └── ...              # 기타 스킬들
├── modules/             # 공통 모듈
│   └── code_changelog_tracker.py  # 변경 이력 로거
├── pipelines/           # 파이프라인 스크립트
│   ├── run_pipeline.py  # Python 통합 파이프라인
│   ├── run_pipeline.sh  # Linux/WSL 래퍼
│   ├── README.md        # 파이프라인 문서
│   └── WSL_TEST_GUIDE.md # WSL 테스트 가이드
├── examples/            # 예제 코드
│   └── changelog_example.py
├── docs/                # 문서
│   ├── CHANGELOG_QUICKSTART.md
│   ├── CHANGELOG_INTEGRATION_GUIDE.md
│   └── CHANGELOG_REQUEST_TEMPLATES.md
├── outputs/             # 실행 결과물
├── reviews/             # 변경 이력 문서
├── requirements.txt    # Python 의존성
└── README.md           # 이 파일
```

## 🛠️ 사용 가능한 스킬

### 데이터 파이프라인

| 스킬 | 설명 | 문서 |
|------|------|------|
| `ingest_play` | Google Play 게임 데이터 수집 | [SKILL.md](skills/ingest_play/SKILL.md) |
| `ranker` | 게임 랭킹 및 점수 계산 | [SKILL.md](skills/ranker/SKILL.md) |
| `publish_html` | HTML 리포트 생성 | [SKILL.md](skills/publish_html/SKILL.md) |

### 개발 도구

| 스킬 | 설명 | 문서 |
|------|------|------|
| `flutter-init` | Flutter 프로젝트 생성 | [SKILL.md](skills/flutter-init/SKILL.md) |
| `nextjs15-init` | Next.js 15 프로젝트 생성 | [SKILL.md](skills/nextjs15-init/SKILL.md) |
| `meta-prompt-generator` | 커스텀 프롬프트 생성 | [SKILL.md](skills/meta-prompt-generator/SKILL.md) |
| `code-changelog` | 코드 변경 이력 자동 기록 ⭐ | [SKILL.md](skills/code-changelog/SKILL.md) |

### 유틸리티

| 스킬 | 설명 | 문서 |
|------|------|------|
| `midjourney-cardnews-bg` | Midjourney 프롬프트 생성 | [SKILL.md](skills/midjourney-cardnews-bg/SKILL.md) |
| `prompt-enhancer` | 프롬프트 개선 | [SKILL.md](skills/prompt-enhancer/SKILL.md) |
| `landing-page-guide` | 랜딩 페이지 가이드 | [SKILL.md](skills/landing-page-guide/SKILL.md) |
| `codex` | Codex CLI 실행 | [skill.md](skills/codex/skill.md) |

## 🔧 환경 변수

주요 환경 변수:

```bash
# ingest_play
QUERY="new games"      # 검색 쿼리
COUNTRY="KR"           # 국가 코드
LANGUAGE="ko"          # 언어 코드
LIMIT=120              # 최대 수집 게임 수

# 공통
LOG_LEVEL="INFO"       # 로그 레벨
```

## 📊 출력 예시

실행 결과는 `outputs/{날짜}/{run_id}/artifacts/` 에 저장됩니다:

```
outputs/20251106/142530/artifacts/
├── raw_games.json         # 수집된 원본 게임 데이터
├── enriched_games.json    # LLM으로 강화된 데이터
└── ranked_games.json      # 랭킹된 최종 결과
```

## 🧪 테스트

```bash
# 단위 테스트 실행
python -m pytest tests/ -v

# 특정 스킬 테스트
python -m unittest discover skills/ingest_play/tests/ -v

# Code Changelog 예제 실행
python examples/changelog_example.py
```

## 📝 Code Changelog (변경 이력 추적)

모든 코드 변경사항을 자동으로 기록하고 웹에서 확인할 수 있습니다.

### 빠른 시작

```bash
# 1. 초기화
python modules/code_changelog_tracker.py init

# 2. 예제 실행
python examples/changelog_example.py

# 3. 문서 서버 실행
cd reviews && python3 -m http.server 4000

# 4. 브라우저에서 확인
# http://localhost:4000
```

### 파이프라인에 통합

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.code_changelog_tracker import CodeChangeLogger

logger = CodeChangeLogger("Pipeline Run")
logger.log_file_creation("output.json", "data...", "Pipeline result")
logger.save_and_build()
```

**자세한 내용:**
- 📝 **요청 템플릿**: [docs/CHANGELOG_REQUEST_TEMPLATES.md](docs/CHANGELOG_REQUEST_TEMPLATES.md) ⭐ 시작
- 🚀 빠른 시작: [docs/CHANGELOG_QUICKSTART.md](docs/CHANGELOG_QUICKSTART.md)
- 🔧 통합 가이드: [docs/CHANGELOG_INTEGRATION_GUIDE.md](docs/CHANGELOG_INTEGRATION_GUIDE.md)
- 💡 예제: [examples/changelog_example.py](examples/changelog_example.py)

## 🤝 기여

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 📞 지원

- 테스트 가이드: [WSL_TEST_GUIDE.md](scripts/WSL_TEST_GUIDE.md)

## 🎮 예시 워크플로우

### Windows (PowerShell)

```powershell
# 1. 가상환경 활성화
.venv\Scripts\Activate.ps1

# 2. 파이프라인 실행
.\run-pipeline.ps1

# 3. HTML 리포트 생성
.\run-html-report.ps1 -RankedItemsPath "outputs\20251107\103252\artifacts\ranked_games.json"

# 4. 결과 확인
ls outputs/20251107/*/artifacts/
ls outputs/20251107/*/reports/
```

### Linux/WSL (Python)

```bash
# 1. 가상환경 활성화
source .venv/bin/activate

# 2. 전체 파이프라인 실행 (수집 → 랭킹 → HTML)
python pipelines/run_pipeline.py --html

# 3. 결과 확인
ls outputs/20251107/*/artifacts/
ls outputs/20251107/*/reports/

# 4. HTML 리포트 열기 (WSL)
explorer.exe outputs/20251107/103252/reports/game_ranking.html
```

### 크로스 플랫폼 (Python)

Python 스크립트는 Windows/Linux/macOS 모두에서 동작합니다:

```bash
# 기본 실행 (한국 신작 top 50 + HTML)
python pipelines/run_pipeline.py --html

# 퍼즐 게임 탐색
python pipelines/run_pipeline.py --query puzzle --country US --top-k 30 --html

# 빠른 테스트 (브라우저 자동 열기)
python pipelines/run_pipeline.py --limit 10 --top-k 5 --html --open-browser
```

---

Made with ❤️ for gamers

