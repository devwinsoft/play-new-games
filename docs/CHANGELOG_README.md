# Code Changelog 스킬 - 완전 가이드

## 📚 문서 구조

### 1. **빠른 시작** - 5분 안에 시작
📄 [CHANGELOG_QUICKSTART.md](CHANGELOG_QUICKSTART.md)
- 설치부터 첫 로그 작성까지
- 문서 서버 실행
- 기본 사용 패턴

### 2. **멀티 에이전트 통합 가이드** - 완전 통합
📄 [CHANGELOG_INTEGRATION_GUIDE.md](CHANGELOG_INTEGRATION_GUIDE.md)
- 각 스킬에 직접 통합
- 파이프라인 래퍼로 통합
- Decorator를 이용한 자동 로깅
- 실전 시나리오 및 예제
- CI/CD 통합

### 3. **예제 코드**
📄 [../examples/changelog_example.py](../examples/changelog_example.py)
- 5가지 실전 예제
- 대화형 데모
- 멀티 에이전트 시뮬레이션

---

## 🎯 핵심 개념

### 변경 이력 자동 기록

모든 코드 변경사항을 자동으로 `reviews/` 폴더에 Markdown 파일로 저장합니다.

```
reviews/
├── index.html              # HTML 뷰어 (자동 생성)
├── README.md               # 홈페이지
├── SUMMARY.md              # 네비게이션 (자동 생성)
├── 20251107_103252.md     # 변경 이력 1
├── 20251107_105430.md     # 변경 이력 2
└── ...
```

### 웹 기반 문서 확인

Python HTTP 서버로 브라우저에서 실시간 확인:

```bash
cd reviews && python3 -m http.server 4000
# → http://localhost:4000
```

---

## 🚀 사용 방법 요약

### 1단계: 초기화 (최초 1회)

```bash
python modules/code_changelog_tracker.py init
```

### 2단계: 코드에서 로깅

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.code_changelog_tracker import CodeChangeLogger

# 로거 생성
logger = CodeChangeLogger(
    project_name="작업 이름",
    user_request="작업 설명"
)

# 변경사항 기록
logger.log_file_creation(
    file_path="파일경로",
    content="파일내용",
    reason="생성이유"
)

# 저장 및 빌드
logger.save_and_build()
```

### 3단계: 문서 확인

```bash
cd reviews
python3 -m http.server 4000

# 브라우저: http://localhost:4000
```

---

## 💡 주요 기능

### 로깅 메서드

| 메서드 | 용도 |
|--------|------|
| `log_file_creation()` | 파일 생성 |
| `log_file_modification()` | 파일 수정 |
| `log_file_deletion()` | 파일 삭제 |
| `log_bug_fix()` | 버그 수정 |
| `log_refactoring()` | 리팩토링 |

### 자동 기능

- ✅ **자동 SUMMARY.md 생성**: 파일 목록 자동 업데이트
- ✅ **자동 index.html 생성**: HTML 뷰어 자동 생성/업데이트
- ✅ **최신 문서 우선**: 가장 최근 문서가 기본으로 표시
- ✅ **Markdown 렌더링**: 코드 하이라이팅 포함
- ✅ **다크 모드 UI**: GitHub 스타일

---

## 🎮 통합 시나리오

### 시나리오 1: 개별 스킬에 통합

```python
# skills/ingest_play/handler.py

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.code_changelog_tracker import CodeChangeLogger

def main():
    logger = CodeChangeLogger("ingest_play", "Collect games")
    
    # 스킬 로직
    games = collect_games()
    output_path = save_games(games)
    
    # 로깅
    logger.log_file_creation(
        file_path=output_path,
        content=f"{len(games)} games",
        reason="Google Play data collection"
    )
    logger.save_and_build()
```

### 시나리오 2: 파이프라인 전체 통합

```python
# pipelines/run_pipeline.py

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.code_changelog_tracker import CodeChangeLogger

def main():
    logger = CodeChangeLogger("Full Pipeline", "3-step pipeline")
    
    # Step 1
    result1 = run_skill('ingest_play')
    logger.log_file_creation(result1['output_path'], "...", "Step 1")
    
    # Step 2
    result2 = run_skill('ranker')
    logger.log_file_creation(result2['output_path'], "...", "Step 2")
    
    # Step 3
    result3 = run_skill('publish_html')
    logger.log_file_creation(result3['output_path'], "...", "Step 3")
    
    # 한 번에 저장
    logger.save_and_build()
```

---

## 📊 실전 예제

### 예제 1: 파일 생성

```python
logger = CodeChangeLogger("Create Config")
logger.log_file_creation(
    file_path="config/settings.json",
    content='{"debug": true}',
    reason="Add development configuration"
)
logger.save_and_build()
```

### 예제 2: 버그 수정

```python
logger = CodeChangeLogger("Fix Bug")
logger.log_bug_fix(
    file_path="scorer.py",
    old_content="score = rating * 0.1",
    new_content="score = rating / 5.0",
    bug_desc="Incorrect rating scale",
    fix_desc="Normalize to 0-1 range"
)
logger.save_and_build()
```

### 예제 3: 파일 수정

```python
logger = CodeChangeLogger("Add Feature")
logger.log_file_modification(
    file_path="handler.py",
    old_content="# Old version",
    new_content="# New version with feature",
    reason="Add HTML report generation"
)
logger.save_and_build()
```

---

## 🔧 고급 활용

### Decorator 패턴

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logging_decorator import log_changes

@log_changes("Data Collection", "Collect games")
def collect_games(query, country):
    # ... 로직 ...
    return {'output_path': '...', 'total_items': 87}
```

### CI/CD 통합

```yaml
# .github/workflows/pipeline.yml
- name: Run pipeline with changelog
  run: python scripts/run_pipeline.py --html

- name: Deploy reviews to GitHub Pages
  uses: peaceiris/actions-gh-pages@v3
  with:
    publish_dir: ./reviews
```

---

## 🌐 서버 실행 팁

### 포트 변경

```bash
python3 -m http.server 3000  # 포트 3000
python3 -m http.server 8080  # 포트 8080
```

### 백그라운드 실행

```bash
# Linux/macOS
cd reviews && python3 -m http.server 4000 > /dev/null 2>&1 &

# Windows PowerShell
Start-Process python -ArgumentList "-m", "http.server", "4000" -WindowStyle Hidden -WorkingDirectory "reviews"
```

### 포트 충돌 해결

```bash
# 사용 중인 프로세스 종료
lsof -ti:4000 | xargs kill -9

# 또는 다른 포트 사용
python3 -m http.server 4001
```

---

## 📁 파일 구조

```
your-project/
├── modules/
│   └── code_changelog_tracker.py  # 로거 스크립트
├── pipelines/
│   ├── run_pipeline.py            # 통합 파이프라인
│   └── ...
├── examples/
│   └── changelog_example.py       # 예제 모음
├── docs/
│   ├── CHANGELOG_README.md        # 이 파일
│   ├── CHANGELOG_QUICKSTART.md    # 빠른 시작
│   └── CHANGELOG_INTEGRATION_GUIDE.md  # 통합 가이드
├── reviews/                        # 생성된 문서
│   ├── index.html                 # HTML 뷰어
│   ├── README.md                  # 홈페이지
│   ├── SUMMARY.md                 # 네비게이션
│   └── YYYYMMDD_HHMMSS.md        # 변경 이력
└── skills/
    └── */handler.py               # 각 스킬 (통합 가능)
```

---

## 🎓 학습 경로

### 1️⃣ 초급: 기본 사용
→ [CHANGELOG_QUICKSTART.md](CHANGELOG_QUICKSTART.md)
- 설치 및 초기화
- 첫 번째 로그 작성
- 문서 서버 실행

### 2️⃣ 중급: 파이프라인 통합
→ [CHANGELOG_INTEGRATION_GUIDE.md](CHANGELOG_INTEGRATION_GUIDE.md) (방법 1)
- 각 스킬에 로깅 추가
- 파일 생성/수정/삭제 추적

### 3️⃣ 고급: 자동화 및 CI/CD
→ [CHANGELOG_INTEGRATION_GUIDE.md](CHANGELOG_INTEGRATION_GUIDE.md) (방법 2, 3)
- Decorator 패턴
- 파이프라인 래퍼
- CI/CD 통합
- 자동 배포

---

## ✅ 체크리스트

### 설정 완료 체크
- [ ] `code_changelog_tracker.py` 파일 존재
- [ ] `reviews/` 디렉토리 생성됨
- [ ] 예제 실행 성공
- [ ] 문서 서버 실행 확인
- [ ] 브라우저에서 문서 확인

### 통합 완료 체크
- [ ] 각 스킬에 로깅 코드 추가
- [ ] 파이프라인에 통합
- [ ] 변경사항이 자동으로 기록됨
- [ ] 문서가 자동으로 업데이트됨
- [ ] 팀원들과 공유 가능

---

## 💬 FAQ

### Q: 파일이 너무 많아지면?
A: 필요 없는 오래된 파일은 삭제해도 됩니다. `save_and_build()`가 자동으로 SUMMARY와 index.html을 재생성합니다.

### Q: 서버가 항상 켜져 있어야 하나요?
A: 개발 중에는 켜두는 것이 편리하지만, 필수는 아닙니다. 필요할 때만 실행하면 됩니다.

### Q: 팀원들과 공유하려면?
A: GitHub Pages, Netlify, Vercel 등에 `reviews/` 폴더를 배포하면 됩니다.

### Q: CI/CD에서 자동 실행?
A: GitHub Actions 등에서 파이프라인 실행 후 `reviews/`를 GitHub Pages로 자동 배포할 수 있습니다.

---

## 🎉 시작하기

```bash
# 1. 초기화
python code_changelog_tracker.py init

# 2. 예제 실행 (대화형)
python examples/changelog_example.py

# 3. 문서 확인
cd reviews && python3 -m http.server 4000
# → http://localhost:4000
```

**Happy Logging! 📝✨**

---

## 📚 관련 문서

- [빠른 시작 가이드](CHANGELOG_QUICKSTART.md)
- [멀티 에이전트 통합 가이드](CHANGELOG_INTEGRATION_GUIDE.md)
- [예제 코드](../examples/changelog_example.py)
- [스킬 문서](../skills/code-changelog/SKILL.md)

