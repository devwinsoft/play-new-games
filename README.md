# Play New Games

Google Play 스토어에서 신작 게임을 수집하고, LLM으로 분석하여, 추천 게임을 선정하는 자동화 시스템입니다.

## 🎯 프로젝트 개요

이 프로젝트는 다음 과정을 자동화합니다:

1. **수집(Ingest)**: Google Play에서 신작 게임 메타데이터 수집
2. **강화(Enrich)**: LLM을 사용해 게임 태깅, 요약, 키워드 추출
3. **랭킹(Rank)**: 신규성/품질/인기도 기반 점수 계산 및 순위 선정
4. **발행(Publish)**: 결과를 JSON/PPT/보고서로 출력

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 가상환경 생성 및 활성화 (Windows PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# 의존성 설치
pip install -r requirements.txt
```

### 2. 스킬 실행

```bash
# 1단계: 게임 데이터 수집
python skills/ingest_play/handler.py

# 2단계: LLM으로 데이터 강화 (ANTHROPIC_API_KEY 필요)
ANTHROPIC_API_KEY="sk-..." python skills/enrich_llm/handler.py

# 3단계: 랭킹 계산
python skills/ranker/scorer.py
```

자세한 내용은 `TEST_GUIDE.md`를 참조하세요.

## 📁 프로젝트 구조

```
play-new-games/
├── .cursor/              # Cursor IDE 설정
├── skills/              # 모든 스킬 모듈
│   ├── skill-index.yaml # 스킬 레지스트리
│   ├── ingest_play/     # 게임 데이터 수집
│   ├── enrich_llm/      # LLM 데이터 강화
│   ├── ranker/          # 랭킹 계산
│   └── ...              # 기타 스킬들
├── outputs/             # 실행 결과물
├── configs/             # 설정 파일
├── tests/              # 테스트 코드
├── requirements.txt    # Python 의존성
├── TEST_GUIDE.md       # 테스트 가이드
└── README.md           # 이 파일
```

## 🛠️ 사용 가능한 스킬

### 데이터 파이프라인

| 스킬 | 설명 | 문서 |
|------|------|------|
| `ingest_play` | Google Play 게임 데이터 수집 | [SKILL.md](skills/ingest_play/SKILL.md) |
| `enrich_llm` | LLM 기반 태깅/요약 | [SKILL.md](skills/enrich_llm/SKILL.md) |
| `ranker` | 게임 랭킹 및 점수 계산 | [SKILL.md](skills/ranker/SKILL.md) |
| `publish` | 결과물 발행 | [SKILL.md](skills/publish/SKILL.md) |

### 개발 도구

| 스킬 | 설명 | 문서 |
|------|------|------|
| `flutter-init` | Flutter 프로젝트 생성 | [SKILL.md](skills/flutter-init/SKILL.md) |
| `nextjs15-init` | Next.js 15 프로젝트 생성 | [SKILL.md](skills/nextjs15-init/SKILL.md) |
| `meta-prompt-generator` | 커스텀 프롬프트 생성 | [SKILL.md](skills/meta-prompt-generator/SKILL.md) |

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

# enrich_llm
ANTHROPIC_API_KEY="sk-..."  # Claude API 키 (필수)

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
```

## 🤝 기여

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 📞 지원

- 이슈: [GitHub Issues](https://github.com/your/repo/issues)
- 문서: [docs/](docs/)
- 테스트 가이드: [TEST_GUIDE.md](TEST_GUIDE.md)

## 🎮 예시 워크플로우

전체 파이프라인 실행:

```bash
# 1. 가상환경 활성화
.venv\Scripts\Activate.ps1

# 2. 환경 변수 설정
$env:ANTHROPIC_API_KEY="sk-..."
$env:LIMIT="50"

# 3. 파이프라인 실행
python skills/ingest_play/handler.py
python skills/enrich_llm/handler.py
python skills/ranker/scorer.py

# 4. 결과 확인
ls outputs/20251106/*/artifacts/
```

---

Made with ❤️ for gamers

