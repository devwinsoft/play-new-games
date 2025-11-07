# Code Changelog 멀티 에이전트 통합 가이드

`code-changelog` 스킬을 멀티 에이전트 환경에서 자동으로 활용하는 완전한 가이드입니다.

## 🎯 목표

AI 에이전트나 자동화 스크립트가 실행될 때마다 자동으로 변경사항을 `reviews/` 폴더에 기록하여, 전체 프로젝트의 변경 이력을 추적할 수 있도록 합니다.

---

## 📋 사전 요구사항

### 1. 코드 로거 설치

```bash
# code_changelog_tracker.py가 modules/에 있는지 확인
ls modules/code_changelog_tracker.py

# reviews 디렉토리 초기화
python modules/code_changelog_tracker.py init
```

### 2. Python 환경

```bash
# Python 3.7+ 필요
python --version

# 추가 패키지 없음 (stdlib만 사용)
```

---

## 🚀 통합 방법

### 방법 1: 각 스킬에 직접 통합 (권장)

각 스킬의 `handler.py` 또는 `scorer.py`에 로깅 코드를 추가합니다.

#### 예시: `ingest_play` 스킬

```python
# skills/ingest_play/handler.py

import sys
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from modules.code_changelog_tracker import CodeChangeLogger

def main():
    # 로거 초기화
    logger = CodeChangeLogger(
        project_name="Game Pipeline - Data Collection",
        user_request=f"Collect {limit} games for query '{query}' in {country}"
    )
    
    # 스킬 로직 실행
    games = collect_games(query, country, limit)
    
    # 결과 저장
    output_path = save_results(games)
    
    # 변경사항 기록
    logger.log_file_creation(
        file_path=output_path,
        content=f"Collected {len(games)} games",
        reason=f"Data collection for query '{query}'"
    )
    
    # 저장 및 빌드
    logger.save_and_build()
    
    # 결과 출력
    print(json.dumps({
        "status": "success",
        "raw_items_path": output_path,
        "total_items": len(games)
    }))

if __name__ == "__main__":
    main()
```

#### 예시: `ranker` 스킬

```python
# skills/ranker/scorer.py

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from modules.code_changelog_tracker import CodeChangeLogger

def main():
    # 로거 초기화
    logger = CodeChangeLogger(
        project_name="Game Pipeline - Ranking",
        user_request=f"Rank games and select top {top_k}"
    )
    
    # 원본 데이터 읽기
    raw_games = load_games(raw_items_path)
    
    # 랭킹 계산
    ranked_games = calculate_ranking(raw_games, top_k)
    
    # 결과 저장
    output_path = save_results(ranked_games)
    
    # 변경사항 기록
    logger.log_file_creation(
        file_path=output_path,
        content=f"Ranked top {len(ranked_games)} games",
        reason=f"Game ranking with diversity algorithm"
    )
    
    # 저장 및 빌드
    logger.save_and_build()
    
    # 결과 출력
    print(json.dumps({
        "status": "success",
        "ranked_items_path": output_path,
        "total_items": len(ranked_games)
    }))

if __name__ == "__main__":
    main()
```

#### 예시: `publish_html` 스킬

```python
# skills/publish_html/handler.py

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from modules.code_changelog_tracker import CodeChangeLogger

def main():
    # 로거 초기화
    logger = CodeChangeLogger(
        project_name="Game Pipeline - HTML Report",
        user_request="Generate HTML report from ranked games"
    )
    
    # 랭킹 데이터 읽기
    ranked_games = load_ranked_games(ranked_items_path)
    
    # HTML 생성
    html_content = generate_html(ranked_games, query, country)
    
    # HTML 저장
    output_path = save_html(html_content)
    
    # 변경사항 기록
    logger.log_file_creation(
        file_path=output_path,
        content=f"HTML report with {len(ranked_games)} games",
        reason="Visual report generation"
    )
    
    # 저장 및 빌드
    logger.save_and_build()
    
    # 결과 출력
    print(json.dumps({
        "status": "success",
        "html_report_path": output_path
    }))

if __name__ == "__main__":
    main()
```

---

### 방법 2: 파이프라인 래퍼로 통합

파이프라인 전체를 래핑하여 자동으로 로깅합니다.

#### 예시: `scripts/run_pipeline.py`에 통합

```python
# scripts/run_pipeline.py

import sys
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from code_changelog_tracker import CodeChangeLogger

def run_skill(skill_name: str, env_vars: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """스킬 실행 (기존 코드)"""
    # ... 기존 로직 ...
    pass

def main():
    # 파이프라인 로거 초기화
    pipeline_logger = CodeChangeLogger(
        project_name=f"Game Pipeline - {args.query}",
        user_request=f"Collect {args.limit} games, rank top {args.top_k}, generate HTML"
    )
    
    print_header("🎮 Game Data Pipeline")
    
    # Step 1: ingest_play
    result1 = run_skill('ingest_play', {...})
    if result1:
        pipeline_logger.log_file_creation(
            file_path=result1['raw_items_path'],
            content=f"{result1['total_items']} games collected",
            reason=f"Data collection for '{args.query}'"
        )
    
    # Step 2: ranker
    result2 = run_skill('ranker', {...})
    if result2:
        pipeline_logger.log_file_creation(
            file_path=result2['ranked_items_path'],
            content=f"{result2['total_items']} games ranked",
            reason="Game ranking and scoring"
        )
    
    # Step 3: publish_html (optional)
    if args.html:
        result3 = run_skill('publish_html', {...})
        if result3:
            pipeline_logger.log_file_creation(
                file_path=result3['html_report_path'],
                content="HTML report generated",
                reason="Visual report for browser"
            )
    
    # 파이프라인 완료 - 변경사항 저장
    pipeline_logger.save_and_build()
    
    print_header("🎉 Pipeline completed successfully!")

if __name__ == "__main__":
    main()
```

---

### 방법 3: Decorator를 이용한 자동 로깅

함수 데코레이터를 사용하여 자동으로 로깅합니다.

```python
# utils/logging_decorator.py

import functools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from modules.code_changelog_tracker import CodeChangeLogger

def log_changes(project_name: str, description: str = ""):
    """
    함수 실행 전후로 자동 로깅
    
    Usage:
        @log_changes("Game Collection", "Collect games from Google Play")
        def collect_games(query, country):
            # ... 로직 ...
            return results
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 로거 초기화
            logger = CodeChangeLogger(
                project_name=project_name,
                user_request=description or f"Execute {func.__name__}"
            )
            
            # 함수 실행
            result = func(*args, **kwargs)
            
            # 결과 파일 자동 감지 및 로깅
            if isinstance(result, dict) and 'output_path' in result:
                logger.log_file_creation(
                    file_path=result['output_path'],
                    content=f"Generated by {func.__name__}",
                    reason=description
                )
                logger.save_and_build()
            
            return result
        return wrapper
    return decorator


# 사용 예시
@log_changes("Game Collection", "Collect games from Google Play")
def collect_games(query: str, country: str, limit: int):
    # ... 로직 ...
    return {
        'output_path': 'outputs/.../raw_games.json',
        'total_items': 87
    }

@log_changes("Game Ranking", "Calculate scores and rank games")
def rank_games(raw_items_path: str, top_k: int):
    # ... 로직 ...
    return {
        'output_path': 'outputs/.../ranked_games.json',
        'total_items': 50
    }
```

---

## 🔧 고급 활용

### 1. 파일 수정 추적

기존 파일을 수정할 때:

```python
logger = CodeChangeLogger("Bug Fix - Ranking Algorithm")

# 변경 전 내용 읽기
old_content = Path("skills/ranker/scorer.py").read_text()

# 파일 수정
# ... 수정 작업 ...

# 변경 후 내용 읽기
new_content = Path("skills/ranker/scorer.py").read_text()

# 변경사항 기록
logger.log_file_modification(
    file_path="skills/ranker/scorer.py",
    old_content=old_content[:500],  # 처음 500자만
    new_content=new_content[:500],
    reason="Fix diversity scoring bug"
)

logger.save_and_build()
```

### 2. 버그 수정 추적

```python
logger = CodeChangeLogger("Bug Fix - Data Normalization")

logger.log_bug_fix(
    file_path="skills/ingest_play/normalize.py",
    old_content="score = rating * 0.1",
    new_content="score = rating / 5.0",
    bug_desc="Rating score was incorrectly calculated",
    fix_desc="Changed formula to normalize rating to 0-1 range"
)

logger.save_and_build()
```

### 3. 리팩토링 추적

```python
logger = CodeChangeLogger("Refactoring - Extract HTML Generation")

logger.log_refactoring(
    file_path="skills/publish_html/handler.py",
    old_content="# Old monolithic function",
    new_content="# New modular functions",
    refactor_type="Extract Method",
    reason="Improve code maintainability and testability"
)

logger.save_and_build()
```

---

## 🌐 문서 서버 실행

### 1. 개발 중 실시간 확인

```bash
# 터미널 1: 문서 서버 (항상 켜둠)
cd reviews
python3 -m http.server 4000

# 브라우저: http://localhost:4000
```

### 2. 백그라운드 실행

```bash
# Linux/macOS
cd reviews && python3 -m http.server 4000 > /dev/null 2>&1 &

# Windows PowerShell
Start-Process python -ArgumentList "-m", "http.server", "4000" -WindowStyle Hidden -WorkingDirectory "reviews"
```

### 3. 자동 빌드 및 서버 실행

```bash
# 빌드 후 서버 실행
python modules/code_changelog_tracker.py build
python modules/code_changelog_tracker.py serve

# 또는 한 번에
python modules/code_changelog_tracker.py build && cd reviews && python3 -m http.server 4000
```

---

## 📊 실전 시나리오

### 시나리오 1: 전체 파이프라인 실행 시 자동 로깅

```python
# pipelines/run_pipeline.py

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.code_changelog_tracker import CodeChangeLogger

def main():
    # 파이프라인 로거
    logger = CodeChangeLogger(
        project_name=f"Game Pipeline Run - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        user_request=f"Query: {args.query}, Country: {args.country}, Top-K: {args.top_k}"
    )
    
    # Step 1
    print_header("Step 1: Collecting games")
    result1 = run_skill('ingest_play', {...})
    logger.log_file_creation(
        file_path=result1['raw_items_path'],
        content=f"Collected {result1['total_items']} games",
        reason="Google Play data collection"
    )
    
    # Step 2
    print_header("Step 2: Ranking games")
    result2 = run_skill('ranker', {...})
    logger.log_file_creation(
        file_path=result2['ranked_items_path'],
        content=f"Ranked top {result2['total_items']} games",
        reason="Freshness + Quality + Popularity scoring"
    )
    
    # Step 3
    if args.html:
        print_header("Step 3: Generating HTML report")
        result3 = run_skill('publish_html', {...})
        logger.log_file_creation(
            file_path=result3['html_report_path'],
            content="HTML report with game cards",
            reason="Browser-based visualization"
        )
    
    # 모든 변경사항 저장
    logger.save_and_build()
    
    print(f"\n✓ Changelog saved: reviews/{logger.timestamp}.md")
    print(f"✓ View at: http://localhost:4000\n")

if __name__ == "__main__":
    main()
```

**실행 후 결과:**
```
reviews/
├── README.md
├── SUMMARY.md
├── index.html
├── 20251107_103252.md  ← 새로 생성됨!
└── ...
```

**브라우저에서 확인:**
```
http://localhost:4000
→ 최신 변경사항이 자동으로 표시됨!
```

---

### 시나리오 2: 각 스킬별 독립 로깅

```python
# skills/ingest_play/handler.py

from code_changelog_tracker import CodeChangeLogger

def main():
    logger = CodeChangeLogger(
        project_name="ingest_play",
        user_request=f"Collect {limit} games for '{query}'"
    )
    
    # ... 스킬 로직 ...
    
    logger.log_file_creation(
        file_path=output_path,
        content=f"{len(games)} games",
        reason=f"Query: {query}, Country: {country}"
    )
    
    logger.save_and_build()

if __name__ == "__main__":
    main()
```

**장점:**
- 각 스킬이 독립적으로 로깅
- 스킬 단위로 변경사항 추적 가능
- 디버깅 및 모니터링 용이

---

### 시나리오 3: CI/CD 통합

```yaml
# .github/workflows/pipeline.yml

name: Game Pipeline

on:
  schedule:
    - cron: '0 6 * * *'  # 매일 오전 6시
  workflow_dispatch:

jobs:
  run-pipeline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run pipeline with changelog
        run: python scripts/run_pipeline.py --html
      
      - name: Deploy reviews to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./reviews
          publish_branch: gh-pages
```

**결과:**
- 매일 자동 실행
- 변경 이력 자동 생성
- GitHub Pages로 자동 배포
- 팀원들이 웹에서 확인 가능

---

## 💡 Best Practices

### 1. 로거 초기화는 명확하게

```python
# ❌ 나쁜 예
logger = CodeChangeLogger("test")

# ✅ 좋은 예
logger = CodeChangeLogger(
    project_name="Game Pipeline - Data Collection Phase",
    user_request="Collect 120 new games from KR Google Play Store"
)
```

### 2. 변경사항은 구체적으로

```python
# ❌ 나쁜 예
logger.log_file_creation("output.json", "data", "create file")

# ✅ 좋은 예
logger.log_file_creation(
    file_path="outputs/20251107/103252/artifacts/raw_games.json",
    content=f"87 games collected: {game_titles[:3]}...",
    reason="Google Play scraping for 'new games' query in KR region"
)
```

### 3. save_and_build() 호출 잊지 말기

```python
# ❌ 나쁜 예 - 변경사항만 기록하고 저장 안 함
logger.log_file_creation(...)

# ✅ 좋은 예 - 저장 및 빌드까지
logger.log_file_creation(...)
logger.save_and_build()  # 반드시 호출!
```

### 4. 서버는 항상 켜두기

```bash
# 개발 시작 시 서버 실행
cd reviews && python3 -m http.server 4000 &

# 브라우저 북마크 추가
http://localhost:4000
```

---

## 🎯 멀티 에이전트 환경 체크리스트

- [ ] `code_changelog_tracker.py`를 프로젝트 루트에 배치
- [ ] `reviews/` 디렉토리 초기화
- [ ] 각 스킬의 `handler.py`에 로깅 코드 추가
- [ ] 파이프라인 스크립트에 통합
- [ ] 문서 서버 실행 및 테스트
- [ ] 브라우저에서 변경사항 확인
- [ ] CI/CD 통합 (선택사항)

---

## 🚀 빠른 테스트

### 1. 수동 테스트

```python
# test_changelog.py

from code_changelog_tracker import CodeChangeLogger

logger = CodeChangeLogger(
    project_name="Test - Manual Changelog",
    user_request="Testing changelog functionality"
)

logger.log_file_creation(
    file_path="test_file.py",
    content="print('Hello World')",
    reason="Testing changelog integration"
)

logger.save_and_build()

print("✓ Changelog created!")
print("✓ Open http://localhost:4000 to view")
```

실행:
```bash
python test_changelog.py
cd reviews && python3 -m http.server 4000
```

### 2. 파이프라인 테스트

```bash
# 파이프라인 실행 (자동으로 로깅됨)
python scripts/run_pipeline.py --limit 5 --top-k 3 --html

# 문서 확인
cd reviews && python3 -m http.server 4000
# → http://localhost:4000
```

---

## 📚 추가 자료

- **SKILL.md**: `skills/code-changelog/SKILL.md` - 전체 기능 문서
- **README.txt**: `skills/code-changelog/README.txt` - 빠른 시작 가이드
- **code_changelog_tracker.py**: 메인 로거 스크립트

---

## 🎉 결론

`code-changelog` 스킬을 멀티 에이전트 환경에 통합하면:

1. ✅ **자동 문서화**: 모든 변경사항이 자동으로 기록됨
2. ✅ **시각적 확인**: 브라우저에서 실시간으로 확인 가능
3. ✅ **팀 협업**: 변경 이력을 팀원들과 공유
4. ✅ **추적 가능성**: 언제, 무엇이, 왜 변경되었는지 명확히 파악
5. ✅ **디버깅 용이**: 문제 발생 시 변경 이력을 통해 원인 파악

**지금 바로 시작하세요!** 🚀

```bash
# 1. 초기화
python code_changelog_tracker.py init

# 2. 파이프라인에 통합
# (위 예시 코드 참고)

# 3. 서버 실행
cd reviews && python3 -m http.server 4000

# 4. 브라우저에서 확인
# http://localhost:4000
```

Happy Logging! 📝✨

