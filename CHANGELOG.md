# Changelog

## [2025-11-07-2] - HTML 리포트 및 크로스 플랫폼 지원 추가

### 변경사항

#### publish_html 스킬 추가
- 랭킹 결과를 HTML 리포트로 시각화하는 새로운 스킬
- 브라우저에서 바로 확인 가능한 게임 리스트
- 카드 형식의 게임 정보 표시
- 점수, 장르, 리뷰, 설치 수 등 주요 정보 포함

#### Python 통합 파이프라인
- `scripts/run_pipeline.py` - 크로스 플랫폼 파이프라인 스크립트
- Windows/Linux/macOS 모두에서 동작
- HTML 리포트 생성 옵션 (`--html`)
- 브라우저 자동 열기 옵션 (`--open-browser`)
- 컬러 출력 및 진행 상황 표시

#### 수정된 파일들

1. **skills/publish_html/** (신규)
   - `handler.py` - HTML 생성 로직
   - `SKILL.md` - 스킬 문서
   - `README.md` - 사용 가이드

2. **scripts/** (신규)
   - `run_pipeline.py` - Python 통합 파이프라인
   - `run_pipeline.sh` - Linux/WSL 래퍼 스크립트
   - `README.md` - 스크립트 사용 문서
   - `WSL_TEST_GUIDE.md` - WSL 테스트 가이드

3. **.claude/commands/game-pipeline.md**
   - 단계 3 (publish_html) 추가
   - 3단계 파이프라인으로 확장
   - HTML 리포트 생성 및 열기 안내

4. **README.md**
   - 프로젝트 구조에 `scripts/` 추가
   - 크로스 플랫폼 사용 예시 추가
   - `publish_html` 스킬 추가

5. **run-pipeline.ps1**
   - HTML 리포트 경로 출력 추가
   - 최종 안내 메시지 개선

### 새로운 파이프라인 구조

```
단계 1: 게임 수집 (ingest_play)
  ↓
단계 2: 랭킹 계산 (ranker)
  ↓
단계 3: HTML 리포트 생성 (publish_html)
  ↓
단계 4: 결과 보고
```

### 출력 파일

- `artifacts/raw_games.json` - 수집된 원본 게임
- `artifacts/ranked_games.json` - 랭킹된 최종 결과
- `reports/game_ranking.html` - HTML 리포트 (신규)

### 사용 방법

#### Windows (PowerShell)
```powershell
# 기본 실행
.\run-pipeline.ps1

# HTML 리포트 생성
.\run-html-report.ps1 -RankedItemsPath "outputs\...\ranked_games.json"
```

#### Linux/WSL/macOS (Python)
```bash
# 전체 파이프라인 + HTML 리포트
python scripts/run_pipeline.py --html

# 브라우저 자동 열기
python scripts/run_pipeline.py --html --open-browser

# 퍼즐 게임 top 30
python scripts/run_pipeline.py --query puzzle --top-k 30 --html
```

#### Cursor 커맨드
```
/game-pipeline "puzzle" "KR" 30
```
→ 이제 HTML 리포트까지 자동 생성

### 이점

1. **시각화**: HTML 리포트로 결과를 직관적으로 확인
2. **크로스 플랫폼**: Windows/Linux/macOS 모두 지원
3. **간편한 실행**: 한 번의 명령으로 전체 파이프라인 + HTML 생성
4. **WSL 지원**: Ubuntu WSL 환경에서도 완벽 동작

---

## [2025-11-07-1] - 파이프라인 간소화

### 변경사항

#### enrich_llm 스킬 제거
- `enrich_llm` 스킬을 파이프라인에서 제거
- `ingest_play` → `ranker` 직접 연결로 워크플로우 간소화
- 전체 파이프라인 실행 시간 단축 (5-10분 → 2-5분)

#### 수정된 파일들

1. **skills/ranker/scorer.py**
   - `ENRICHED_ITEMS_PATH` → `RAW_ITEMS_PATH` 지원 추가
   - 하위 호환성 유지 (ENRICHED_ITEMS_PATH도 여전히 동작)

2. **skills/ranker/SKILL.md**
   - 입력 파라미터 문서 업데이트
   - 사용 예시 수정

3. **run-pipeline.ps1**
   - 단계 2 (enrich_llm) 제거
   - 단계 3을 단계 2로 변경
   - API 키 검증 제거

4. **.claude/commands/game-pipeline.md**
   - 워크플로우 문서 전체 업데이트
   - 2단계 파이프라인으로 재구성
   - 테스트 스위트 재조정

5. **.claude/commands/README.md**
   - 파이프라인 설명 업데이트
   - 필수 환경 요구사항 간소화

### 새로운 파이프라인 구조

```
단계 1: 게임 수집 (ingest_play)
  ↓
단계 2: 랭킹 계산 (ranker)
  ↓
단계 3: 결과 보고
```

### 출력 파일

- `raw_games.json` - 수집된 원본 게임
- `ranked_games.json` - 랭킹된 최종 결과

### 이점

1. **실행 시간 단축**: 5-10분 → 2-5분
2. **비용 절감**: Claude API 호출 제거
3. **간단한 구조**: 2단계만으로 결과 도출
4. **빠른 피드백**: 게임 수집 후 바로 랭킹 확인

### 하위 호환성

- `ranker` 스킬은 여전히 `ENRICHED_ITEMS_PATH`를 지원
- 기존 `enrich_llm` 스킬은 삭제되지 않고 독립적으로 사용 가능

### 사용 방법

```powershell
# 기본 실행
.\run-pipeline.ps1

# 파라미터 지정
.\run-pipeline.ps1 -Query "puzzle" -TopK 30

# 또는 Cursor에서
/game-pipeline "puzzle" "KR" 30
```

