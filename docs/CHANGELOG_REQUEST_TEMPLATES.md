# AI에게 Changelog 자동 기록 요청하는 방법

`.cursorrules`에 자동 로깅 규칙이 추가되었으므로, 이제 AI는 코드 변경 시 자동으로 changelog를 기록해야 합니다.

---

## 📝 요청 템플릿

### 템플릿 1: 간단한 요청

```
[작업 내용]을 구현하고, 변경 이력을 reviews에 기록해줘.
```

**예시:**
```
HTML 리포트 생성 기능을 publish_html 스킬에 추가하고, 
변경 이력을 reviews에 기록해줘.
```

---

### 템플릿 2: 상세한 요청 (권장)

```
[작업 내용]을 구현해줘.

요구사항:
1. [구체적 요구사항 1]
2. [구체적 요구사항 2]
3. CodeChangeLogger로 변경사항을 reviews/ 폴더에 기록
4. 작업 완료 후 changelog 확인 방법 안내
```

**예시:**
```
게임 데이터 수집 스킬에 중복 제거 기능을 추가해줘.

요구사항:
1. normalize.py에 deduplicate_games() 함수 추가
2. handler.py에서 중복 제거 호출
3. CodeChangeLogger로 변경사항을 reviews/ 폴더에 기록
4. 작업 완료 후 changelog 확인 방법 안내
```

---

### 템플릿 3: 버그 수정 요청

```
[파일명]의 [버그 설명]을 수정하고, 
log_bug_fix()로 변경 이력을 기록해줘.
```

**예시:**
```
scorer.py의 rating 점수 계산 버그를 수정하고,
log_bug_fix()로 변경 이력을 기록해줘.

버그: rating이 0-5 범위인데 0-0.5로 계산됨
수정: rating / 5.0 으로 정규화
```

---

### 템플릿 4: 새 스킬 생성

```
[스킬 이름] 스킬을 새로 만들어줘.

기능:
- [기능 1]
- [기능 2]

그리고 CodeChangeLogger로 스킬 생성 이력을 reviews에 기록해줘.
```

**예시:**
```
data_validator 스킬을 새로 만들어줘.

기능:
- 게임 메타데이터 유효성 검사
- 필수 필드 확인
- 데이터 타입 검증

그리고 CodeChangeLogger로 스킬 생성 이력을 reviews에 기록해줘.
```

---

### 템플릿 5: 파이프라인 통합

```
[작업 내용]을 구현하고, 전체 파이프라인 실행 시 
자동으로 changelog가 기록되도록 통합해줘.
```

**예시:**
```
run_pipeline.py에 자동 로깅 기능을 통합해줘.

요구사항:
- 각 단계(ingest, rank, html) 실행 후 결과를 로깅
- 파이프라인 전체 완료 시 하나의 changelog 문서 생성
- CodeChangeLogger 사용
```

---

## 🎯 실전 예시

### 예시 1: 단순 기능 추가

**사용자 요청:**
```
publish_html 스킬에 CSS 스타일을 개선하고, 
변경 이력을 reviews에 기록해줘.
```

**AI가 할 일:**
1. CSS 스타일 개선
2. CodeChangeLogger 사용:
   ```python
   logger = CodeChangeLogger(
       "Improve HTML Report Styling",
       "User requested CSS improvements for better readability"
   )
   logger.log_file_modification(...)
   logger.save_and_build()
   ```
3. 변경 이력 확인 방법 안내

---

### 예시 2: 버그 수정

**사용자 요청:**
```
ranker의 diversity_score 계산이 잘못되었어. 
unique genre 수를 세야 하는데 전체 genre를 더하고 있어.
수정하고 log_bug_fix()로 기록해줘.
```

**AI가 할 일:**
1. 버그 분석 및 수정
2. CodeChangeLogger의 log_bug_fix() 사용:
   ```python
   logger = CodeChangeLogger(
       "Bug Fix - Diversity Score Calculation",
       "Fix diversity score to count unique genres"
   )
   logger.log_bug_fix(
       file_path="skills/ranker/scorer.py",
       old_content="return sum([g.genre for g in games])",
       new_content="return len(set(g.genre for g in games))",
       bug_desc="Summing all genres instead of counting unique",
       fix_desc="Use set() to count unique genres"
   )
   logger.save_and_build()
   ```

---

### 예시 3: 새 파일 생성

**사용자 요청:**
```
utils/validator.py를 만들어서 게임 데이터 검증 함수를 추가해줘.
그리고 CodeChangeLogger로 기록해줘.

필요한 함수:
- validate_rating(): rating이 0-5 범위인지 확인
- validate_installs(): installs가 숫자인지 확인
```

**AI가 할 일:**
1. utils/validator.py 생성
2. 필요한 함수 구현
3. CodeChangeLogger 사용:
   ```python
   logger = CodeChangeLogger(
       "Create Data Validator",
       "Add validation functions for game metadata"
   )
   logger.log_file_creation(
       file_path="utils/validator.py",
       content="# validator.py code...",
       reason="Validate game data before processing"
   )
   logger.save_and_build()
   ```

---

### 예시 4: 파이프라인 통합

**사용자 요청:**
```
run_pipeline.py를 수정해서 전체 파이프라인 실행 시 
자동으로 changelog가 기록되도록 해줘.

각 단계(ingest → rank → html)의 결과를 하나의 changelog 문서에 기록하고,
완료 시 reviews/ 경로를 알려줘.
```

**AI가 할 일:**
1. run_pipeline.py 수정
2. 파이프라인 로거 추가:
   ```python
   logger = CodeChangeLogger(
       f"Game Pipeline - {query}",
       f"Full pipeline: collect → rank → html"
   )
   
   # Step 1
   result1 = run_skill('ingest_play', {...})
   logger.log_file_creation(result1['raw_items_path'], ...)
   
   # Step 2
   result2 = run_skill('ranker', {...})
   logger.log_file_creation(result2['ranked_items_path'], ...)
   
   # Step 3
   result3 = run_skill('publish_html', {...})
   logger.log_file_creation(result3['html_report_path'], ...)
   
   # 저장
   logger.save_and_build()
   print(f"Changelog: reviews/{logger.timestamp}.md")
   ```

---

## 💡 핵심 포인트

### ✅ DO (해야 할 것)

1. **명시적으로 changelog 기록 요청**
   ```
   "... 하고, 변경 이력을 reviews에 기록해줘."
   ```

2. **상세한 작업 내용 제공**
   ```
   "버그: [설명]
    수정: [방법]
    그리고 log_bug_fix()로 기록해줘."
   ```

3. **확인 방법 요청**
   ```
   "... 하고, changelog 확인 방법도 알려줘."
   ```

### ❌ DON'T (하지 말아야 할 것)

1. **모호한 요청**
   ```
   ❌ "코드 좀 수정해줘"
   ✅ "scorer.py의 rating 계산 수정하고 changelog 기록해줘"
   ```

2. **changelog 언급 없음**
   ```
   ❌ "HTML 리포트 기능 추가해줘"
   ✅ "HTML 리포트 기능 추가하고 reviews에 기록해줘"
   ```

---

## 🔄 워크플로우

```
1. AI에게 요청
   ↓
   "파이프라인에 HTML 리포트 추가하고, 
    변경 이력을 reviews에 기록해줘."

2. AI가 작업 수행
   ↓
   - 코드 변경
   - CodeChangeLogger 호출
   - logger.save_and_build()

3. 결과 확인
   ↓
   cd reviews && python3 -m http.server 4000
   브라우저: http://localhost:4000

4. 최신 문서 확인
   ↓
   가장 최근 타임스탬프 문서가 자동으로 표시됨!
```

---

## 🎓 학습 곡선

### 1단계: 기본
```
"[작업]하고, changelog 기록해줘."
```

### 2단계: 구체적
```
"[파일]의 [기능]을 [방법]으로 수정하고,
 CodeChangeLogger로 reviews에 기록해줘."
```

### 3단계: 자동화
```
".cursorrules에 따라 모든 코드 변경 시 
 자동으로 changelog를 기록해줘."
```

→ `.cursorrules` 업데이트 후에는 3단계 요청만으로도 자동 기록!

---

## 🚀 지금 바로 시작

### 간단한 테스트

```
"test.py 파일을 만들고 'Hello World'를 출력하는 코드를 작성해줘.
그리고 CodeChangeLogger로 변경 이력을 reviews에 기록해줘."
```

AI가 다음을 수행합니다:
1. test.py 생성
2. CodeChangeLogger로 기록
3. reviews/YYYYMMDD_HHMMSS.md 생성
4. 확인 방법 안내

### 확인

```bash
cd reviews && python3 -m http.server 4000
# http://localhost:4000
```

---

## 📚 참고

- `.cursorrules`: 프로젝트 자동 로깅 규칙
- `docs/CHANGELOG_QUICKSTART.md`: 빠른 시작 가이드
- `docs/CHANGELOG_INTEGRATION_GUIDE.md`: 통합 가이드
- `examples/changelog_example.py`: 예제 코드

---

**이제 AI에게 코드 변경을 요청할 때 "changelog 기록해줘"만 추가하면 자동으로 기록됩니다!** 🎉

