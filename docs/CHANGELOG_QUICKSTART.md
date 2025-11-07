# Code Changelog 빠른 시작 가이드

`code-changelog` 스킬을 5분 안에 시작하는 가이드입니다.

## 🚀 1단계: 설치 (30초)

```bash
# 프로젝트 루트에서 실행
python modules/code_changelog_tracker.py init
```

**생성되는 것:**
- `reviews/` 디렉토리
- `reviews/README.md`

---

## ✍️ 2단계: 첫 번째 로그 작성 (1분)

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.code_changelog_tracker import CodeChangeLogger

# 로거 생성
logger = CodeChangeLogger(
    project_name="My First Changelog",
    user_request="Testing changelog feature"
)

# 변경사항 기록
logger.log_file_creation(
    file_path="test.py",
    content="print('Hello, World!')",
    reason="Create test file"
)

# 저장
logger.save_and_build()

print("✓ Changelog created!")
```

**실행:**
```bash
python examples/changelog_example.py
```

---

## 🌐 3단계: 문서 확인 (30초)

```bash
# 서버 실행
cd reviews
python3 -m http.server 4000

# 브라우저에서 열기
# http://localhost:4000
```

**보이는 것:**
- 좌측: 변경 이력 목록 (최신순)
- 우측: 선택한 문서 내용
- 자동 Markdown 렌더링

---

## 🎯 4단계: 파이프라인에 통합 (2분)

### 방법 1: 각 스킬에 추가

```python
# skills/your_skill/handler.py

import sys
from pathlib import Path

# 프로젝트 루트 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from modules.code_changelog_tracker import CodeChangeLogger

def main():
    # 로거 초기화
    logger = CodeChangeLogger(
        project_name="Your Skill Name",
        user_request="What this skill does"
    )
    
    # 스킬 로직 실행
    result = your_skill_logic()
    
    # 변경사항 기록
    logger.log_file_creation(
        file_path=result['output_path'],
        content=f"Generated {result['count']} items",
        reason="Skill execution"
    )
    
    # 저장
    logger.save_and_build()
    
    return result

if __name__ == "__main__":
    main()
```

### 방법 2: 파이프라인 래퍼

```python
# pipelines/run_pipeline.py

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.code_changelog_tracker import CodeChangeLogger

def main():
    # 파이프라인 로거
    logger = CodeChangeLogger(
        project_name="Full Pipeline",
        user_request="Run complete pipeline"
    )
    
    # Step 1
    result1 = run_skill('skill1', {})
    logger.log_file_creation(
        file_path=result1['output_path'],
        content="Step 1 output",
        reason="Step 1 execution"
    )
    
    # Step 2
    result2 = run_skill('skill2', {})
    logger.log_file_creation(
        file_path=result2['output_path'],
        content="Step 2 output",
        reason="Step 2 execution"
    )
    
    # 저장
    logger.save_and_build()

if __name__ == "__main__":
    main()
```

---

## 📋 5단계: 사용 패턴

### 패턴 1: 파일 생성

```python
logger.log_file_creation(
    file_path="path/to/file.py",
    content="file content...",
    reason="why created"
)
```

### 패턴 2: 파일 수정

```python
logger.log_file_modification(
    file_path="path/to/file.py",
    old_content="old code...",
    new_content="new code...",
    reason="why modified"
)
```

### 패턴 3: 버그 수정

```python
logger.log_bug_fix(
    file_path="path/to/file.py",
    old_content="buggy code...",
    new_content="fixed code...",
    bug_desc="what was wrong",
    fix_desc="how fixed"
)
```

### 패턴 4: 파일 삭제

```python
logger.log_file_deletion(
    file_path="path/to/file.py",
    content="deleted content...",
    reason="why deleted"
)
```

---

## 💡 빠른 팁

### 1. 서버 항상 켜두기

```bash
# 백그라운드 실행 (Linux/macOS)
cd reviews && python3 -m http.server 4000 > /dev/null 2>&1 &

# 백그라운드 실행 (Windows PowerShell)
Start-Process python -ArgumentList "-m", "http.server", "4000" -WindowStyle Hidden -WorkingDirectory "reviews"
```

### 2. 브라우저 북마크

```
http://localhost:4000
```
→ 개발 중 빠른 접근

### 3. 포트 충돌 시

```bash
# 다른 포트 사용
python3 -m http.server 4001
python3 -m http.server 8080
```

---

## 🎮 실전 예제

### 예제 1: 게임 파이프라인

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.code_changelog_tracker import CodeChangeLogger

# 파이프라인 실행
logger = CodeChangeLogger(
    project_name="Game Pipeline - Puzzle Games",
    user_request="Collect and rank puzzle games"
)

# Step 1: Collect
games = collect_games("puzzle", "KR", 100)
logger.log_file_creation(
    file_path="outputs/raw_games.json",
    content=f"{len(games)} games collected",
    reason="Google Play data collection"
)

# Step 2: Rank
ranked = rank_games(games, top_k=30)
logger.log_file_creation(
    file_path="outputs/ranked_games.json",
    content=f"Top {len(ranked)} games",
    reason="Score calculation and ranking"
)

# 저장
logger.save_and_build()

print("✓ Pipeline completed and logged!")
```

### 예제 2: 버그 수정

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.code_changelog_tracker import CodeChangeLogger

logger = CodeChangeLogger(
    project_name="Bug Fix - Rating Normalization",
    user_request="Fix incorrect rating calculation"
)

logger.log_bug_fix(
    file_path="normalize.py",
    old_content="score = rating * 0.1",
    new_content="score = rating / 5.0",
    bug_desc="Rating score out of range (0-0.5 instead of 0-1)",
    fix_desc="Use division to normalize 0-5 rating to 0-1"
)

logger.save_and_build()

print("✓ Bug fix logged!")
```

---

## 🔥 자동화 팁

### 모든 스킬에 한 번에 추가

```bash
# scripts/add_logging.sh

for skill in skills/*/handler.py; do
    echo "Adding logging to $skill"
    # 로거 import 추가
    # logger 초기화 코드 추가
    # save_and_build() 호출 추가
done
```

### Git Hook 통합

```bash
# .git/hooks/post-commit

#!/bin/bash
# 커밋 후 자동으로 changelog 생성

python code_changelog_tracker.py build
```

---

## 📚 더 알아보기

- **전체 가이드**: `docs/CHANGELOG_INTEGRATION_GUIDE.md`
- **스킬 문서**: `skills/code-changelog/SKILL.md`
- **예제 모음**: `examples/changelog_example.py`

---

## 🎉 완료!

이제 모든 변경사항이 자동으로 기록됩니다!

```bash
# 확인
cd reviews
python3 -m http.server 4000

# 브라우저
http://localhost:4000
```

**Happy Logging! 📝✨**

