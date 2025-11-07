---
allowed-tools: ["read_file", "write", "search_replace", "run_terminal_cmd", "grep", "list_dir"]
description: Google Play에서 게임을 수집하고 점수를 계산하여 상위 게임을 선정한 후 HTML 리포트를 생성하는 전체 파이프라인을 실행합니다
argument-hint: [검색쿼리] [국가코드] [최종선정개수]
model: sonnet
---

# Game Data Pipeline

Google Play에서 신작 게임을 수집하고 점수를 계산하여 상위 N개 게임을 선정한 후 HTML 리포트를 생성하는 완전 자동화된 파이프라인입니다.

## 변수

### 동적 변수 (사용자 입력)
- `$1` (query): 검색 쿼리 (기본값: "new games")
- `$2` (country): 국가 코드 (기본값: "KR")  
- `$3` (top_k): 최종 선정 게임 수 (기본값: "50")

### 정적 변수
- `LANGUAGE`: 언어 코드 = "ko"
- `INITIAL_LIMIT`: 초기 수집 게임 수 = 120
- `OUTPUT_BASE`: 출력 디렉토리 = "outputs"
- `RUN_ID`: 실행 ID = 타임스탬프

## 지침

### 실행 규칙

1. **환경 검증**: 시작 전 필수 조건 확인
   - Python 가상환경 활성화 여부
   - 필수 패키지 설치 여부

2. **단계별 실행**: 각 단계는 순차적으로 실행 (3단계)
   - 단계 1: ingest_play (게임 수집)
   - 단계 2: ranker (랭킹 계산)
   - 단계 3: publish_html (HTML 리포트 생성)
   - 이전 단계의 출력이 다음 단계의 입력
   - 각 단계 완료 후 결과 검증
   - 실패 시 에러 메시지와 함께 중단

3. **진행 상황 보고**: 사용자에게 명확한 피드백
   - 각 단계 시작/완료 알림
   - 처리된 항목 수 표시
   - 예상 소요 시간 안내

4. **에러 처리**:
   - Rate limiting 발생 시 재시도 전략 안내
   - 일부 게임 처리 실패 시에도 파이프라인 계속 진행
   - 최종 결과에 성공/실패 통계 포함

5. **출력 관리**:
   - 모든 중간 결과물 보존
   - 최종 결과는 시간별로 구분된 디렉토리에 저장
   - 결과 파일 경로를 명확하게 보고

### 엣지 케이스 처리

- **수집 게임 0개**: 쿼리 변경 제안
- **랭킹 계산 실패**: 필수 필드 누락 확인
- **중복 실행**: 같은 날짜에 여러 번 실행 가능하도록 RUN_ID로 구분

## 코드베이스 구조

```
play-new-games/
├── skills/
│   ├── ingest_play/
│   │   └── handler.py           # 단계 1: 게임 데이터 수집
│   ├── ranker/
│   │   └── scorer.py            # 단계 2: 랭킹 계산
│   └── publish_html/
│       └── handler.py           # 단계 3: HTML 리포트 생성
├── outputs/
│   └── YYYYMMDD/
│       └── HHMMSS/
│           ├── artifacts/       # JSON 결과물
│           └── reports/         # HTML 리포트
└── .venv/                       # Python 가상환경
```

## 워크플로우

### 단계 0: 환경 검증 및 초기화

**종속성:** 없음  
**실행 모드:** 순차적  
**서브 에이전트 전략:** 메인 컨텍스트에서 실행

#### 작업 항목

1. 가상환경 활성화 상태 확인
   ```powershell
   if (-not $env:VIRTUAL_ENV) {
       Write-Host "가상환경을 활성화하세요: .\.venv\Scripts\Activate.ps1"
       exit 1
   }
   ```

2. 파라미터 설정
   - query = $1 또는 "new games"
   - country = $2 또는 "KR"
   - top_k = $3 또는 50
   - RUN_ID = 현재 시간 (HHMMSS)

3. 시작 알림
   ```
   ============================================================
   🎮 Game Data Pipeline 시작
   ============================================================
   검색 쿼리: {query}
   국가: {country}
   최종 선정: {top_k}개
   Run ID: {RUN_ID}
   ============================================================
   ```

**병렬 실행:** 불가 (환경 검증은 순차적으로 수행)

---

### 단계 1: 게임 데이터 수집 (Ingest)

**종속성:** 단계 0  
**실행 모드:** 순차적  
**서브 에이전트 전략:** 메인 컨텍스트에서 실행

#### 작업 항목

1. ingest_play 스킬 실행
   ```powershell
   $env:QUERY = $query
   $env:COUNTRY = $country
   $env:LANGUAGE = "ko"
   $env:LIMIT = "120"
   $env:RUN_ID = $RUN_ID
   
   python skills/ingest_play/handler.py
   ```

2. 출력 파일 경로 파싱
   - JSON 출력에서 `raw_items_path` 추출
   - 경로: `outputs/{날짜}/{RUN_ID}/artifacts/raw_games.json`

3. 수집 결과 검증
   - 게임 수가 0개인 경우 경고
   - 최소 10개 이상 권장

4. 진행 상황 보고
   ```
   ✓ 단계 1 완료: {N}개 게임 수집
   출력 파일: {raw_items_path}
   ```

**예상 소요 시간:** 1-3분 (네트워크 속도에 따라)

**병렬 실행:** 불가 (단일 데이터 소스)

---

### 단계 2: 게임 랭킹 계산 (Rank)

**종속성:** 단계 1 (raw_items_path 필요)  
**실행 모드:** 순차적  
**서브 에이전트 전략:** 메인 컨텍스트에서 실행

#### 작업 항목

1. 입력 파일 확인
   - raw_items_path가 존재하는지 확인
   - 필수 필드(rating, release_date, installs)가 있는지 확인

2. ranker 스킬 실행
   ```powershell
   $env:RAW_ITEMS_PATH = $raw_items_path
   $env:TOP_K = $top_k
   $env:RUN_ID = $RUN_ID
   
   python skills/ranker/scorer.py
   ```

3. 출력 파일 경로 파싱
   - JSON 출력에서 `ranked_items_path` 추출
   - 경로: `outputs/{날짜}/{RUN_ID}/artifacts/ranked_games.json`

4. 랭킹 결과 검증
   - top_k 개수만큼 선정되었는지 확인
   - 점수가 내림차순으로 정렬되었는지 확인

5. 진행 상황 보고
   ```
   ✓ 단계 2 완료: 상위 {top_k}개 게임 선정
   출력 파일: {ranked_items_path}
   ```

**예상 소요 시간:** 10-30초

**병렬 실행:** 불가 (전체 데이터를 대상으로 계산)

---

### 단계 3: HTML 리포트 생성 (Publish)

**종속성:** 단계 2 (ranked_items_path 필요)  
**실행 모드:** 순차적  
**서브 에이전트 전략:** 메인 컨텍스트에서 실행

#### 작업 항목

1. 입력 파일 확인
   - ranked_items_path가 존재하는지 확인
   - JSON 파일 유효성 검증

2. publish_html 스킬 실행
   ```powershell
   $env:RANKED_ITEMS_PATH = $ranked_items_path
   $env:QUERY = $query
   $env:COUNTRY = $country
   $env:RUN_ID = $RUN_ID
   
   python skills/publish_html/handler.py
   ```

3. 출력 파일 경로 파싱
   - JSON 출력에서 `html_report_path` 추출
   - 경로: `outputs/{날짜}/{RUN_ID}/reports/game_ranking.html`

4. HTML 리포트 검증
   - 파일이 생성되었는지 확인
   - 파일 크기가 0보다 큰지 확인

5. 진행 상황 보고
   ```
   ✓ 단계 3 완료: HTML 리포트 생성
   출력 파일: {html_report_path}
   ```

6. 브라우저에서 리포트 열기 (선택사항)
   ```powershell
   Start-Process $html_report_path
   ```

**예상 소요 시간:** 1-3초

**병렬 실행:** 불가 (단일 HTML 생성)

---

### 단계 4: 결과 요약 및 보고

**종속성:** 단계 3  
**실행 모드:** 순차적  
**서브 에이전트 전략:** 메인 컨텍스트에서 실행

#### 작업 항목

1. ranked_games.json 파일 읽기

2. 상위 10개 게임 정보 추출
   - 순위, 제목, 개발사, 점수
   - 주요 태그

3. 통계 계산
   - 총 수집 게임 수
   - 최종 선정 게임 수
   - 장르별 분포

4. 최종 보고서 생성
   ```
   ============================================================
   🎉 Game Data Pipeline 완료!
   ============================================================
   
   📊 실행 통계:
   - 수집 게임: {raw_count}개
   - 최종 선정: {top_k}개
   
   🏆 상위 10개 게임:
   1. [{점수}] {제목} - {개발사}
      Tags: {태그들}
   2. ...
   
   📁 결과 파일:
   - 원본: {raw_items_path}
   - 랭킹: {ranked_items_path}
   - HTML: {html_report_path}
   
   ⏱️ 총 소요 시간: {duration}
   ============================================================
   ```

5. 다음 단계 제안
   - HTML 리포트 열기
   - 결과 파일 확인 방법
   - 다른 쿼리로 재실행 제안

**병렬 실행:** 불가 (최종 통합 보고)

---

## 테스트 스위트

### 단위 테스트

#### 테스트 1: 환경 검증
```powershell
# 가상환경 없이 실행
# 예상: 에러 메시지와 함께 중단
```
**병렬 실행:** 가능

#### 테스트 2: 각 단계 개별 실행
```powershell
# 단계 1만 실행하여 출력 확인
# 단계 2만 실행하여 출력 확인 (단계 1 결과 사용)
```
**병렬 실행:** 가능 (독립적인 테스트)

---

### 통합 테스트

#### 테스트 3: 전체 파이프라인 (소량 데이터)
```powershell
# LIMIT=10으로 설정하여 빠른 테스트
$env:LIMIT = "10"
# 전체 파이프라인 실행
# 예상: 1-2분 내 완료
```
**병렬 실행:** 불가 (순차 종속성)

#### 테스트 4: 다양한 검색 쿼리
```powershell
# 쿼리: "puzzle", "action", "rpg"
# 각각 실행하여 결과 비교
```
**병렬 실행:** 가능 (서로 다른 RUN_ID)

---

### 종단 간 테스트

#### 테스트 5: 실제 운영 시나리오
```powershell
# 120개 수집 → 50개 선정
# 전체 과정 실행 및 결과 검증
```
**병렬 실행:** 불가

#### 테스트 6: 연속 실행
```powershell
# 같은 날 2회 실행
# RUN_ID로 구분되는지 확인
```
**병렬 실행:** 가능 (다른 RUN_ID)

---

### 엣지 케이스

#### 테스트 7: 수집 게임 0개
```powershell
# 존재하지 않는 쿼리로 검색
$query = "nonexistentgamexyz123"
# 예상: 경고 메시지와 함께 중단
```

#### 테스트 8: Rate Limiting
```powershell
# 짧은 시간에 여러 번 실행
# 예상: 재시도 안내 메시지
```

#### 테스트 9: 필수 필드 누락
```powershell
# rating이나 release_date가 없는 데이터로 테스트
# 예상: 에러 처리 및 필드 확인 안내
```

---

### 검증 명령

#### 환경 검증
```powershell
# Python 버전 확인
python --version

# 패키지 설치 확인
pip list | Select-String "google-play-scraper|colorlog|dateutil"
```

#### 출력 파일 검증
```powershell
# 파일 존재 확인
Test-Path outputs/YYYYMMDD/HHMMSS/artifacts/raw_games.json
Test-Path outputs/YYYYMMDD/HHMMSS/artifacts/ranked_games.json

# JSON 유효성 검증
Get-Content outputs/.../ranked_games.json | ConvertFrom-Json | 
    Select-Object -First 1
```

#### 결과 데이터 검증
```powershell
# 게임 수 확인
$games = Get-Content outputs/.../ranked_games.json | ConvertFrom-Json
Write-Host "Total games: $($games.Count)"

# 필수 필드 확인
$games[0] | Select-Object rank, title, final_score, tags

# 점수 정렬 확인
$games | Select-Object rank, final_score | Sort-Object rank
```

---

### 최종 품질 보증

#### 완료 기준

**필수 요구사항:**
- [ ] 모든 3단계가 에러 없이 완료
- [ ] 2개의 artifacts 파일이 생성됨 (raw_games.json, ranked_games.json)
- [ ] 1개의 HTML 리포트가 생성됨 (game_ranking.html)
- [ ] ranked_games.json에 top_k 개수만큼 게임 포함
- [ ] 각 게임이 필수 필드를 모두 포함 (rank, title, final_score)
- [ ] HTML 리포트가 브라우저에서 정상적으로 렌더링됨

**품질 기준:**
- [ ] 수집 게임 수 ≥ 10개
- [ ] 최종 게임이 점수 내림차순으로 정렬
- [ ] 장르 다양성이 확보됨 (MMR 알고리즘)

**성능 기준:**
- [ ] 전체 파이프라인 ≤ 5분 (120개 게임 기준)
- [ ] 단계 1 (수집): ≤ 3분
- [ ] 단계 2 (랭킹): ≤ 1분
- [ ] 단계 3 (HTML): ≤ 5초
- [ ] 단계별 진행 상황이 명확히 표시됨
- [ ] 중간 결과물이 모두 보존됨

---

## 최종 결과물

### 주요 출력 파일

1. **raw_games.json** (단계 1)
   - Google Play에서 수집한 원본 게임 데이터
   - 약 120개 게임 메타데이터

2. **ranked_games.json** (단계 2)
   - 점수 계산 및 랭킹된 최종 결과
   - 상위 N개 게임 (기본 50개)

3. **game_ranking.html** (단계 3)
   - HTML 형식의 시각화 리포트
   - 브라우저에서 바로 확인 가능

### 출력 디렉토리 구조

```
outputs/
└── 20251106/                    # 실행 날짜
    └── 195530/                  # Run ID (실행 시간)
        ├── artifacts/
        │   ├── raw_games.json
        │   └── ranked_games.json
        └── reports/
            └── game_ranking.html
```

### 사용자에게 제공할 정보

1. **실행 요약**
   - 처리된 게임 수 (각 단계별)
   - 소요 시간
   - 성공/실패 통계

2. **상위 게임 리스트**
   - 순위, 제목, 점수
   - 주요 특징 (태그)

3. **결과 파일 경로**
   - 2개의 JSON 파일 (raw_games.json, ranked_games.json)
   - 1개의 HTML 리포트 (game_ranking.html)
   - 파일 크기 및 수정 시간

4. **HTML 리포트**
   - 브라우저에서 열기 버튼 제공
   - 시각화된 게임 리스트
   - 필터링 및 정렬 기능

5. **다음 단계 제안**
   - HTML 리포트 열어보기
   - 다른 쿼리로 재실행
   - 특정 장르만 필터링

---

## 보고서

### 실행 완료 메시지

```
============================================================
🎉 Game Data Pipeline 완료!
============================================================

📊 실행 통계:
총 소요 시간: 3분 15초

단계 1 - 게임 수집:
  ✓ 수집: 87개
  ⏱ 소요: 2분 38초

단계 2 - 랭킹 계산:
  ✓ 선정: 50개
  ⏱ 소요: 34초

단계 3 - HTML 리포트:
  ✓ 생성: 완료
  ⏱ 소요: 3초

🏆 상위 10개 게임:
1. [0.92] 스타듀 밸리 모바일 - ConcernedApe
   Tags: farming, rpg, indie
   
2. [0.89] 던전메이커 - GameCoaster
   Tags: roguelike, deck-building, strategy
   
3. [0.87] 쿠키런: 킹덤 - Devsisters
   Tags: rpg, gacha, story-driven
   
4. [0.85] 브롤스타즈 - Supercell
   Tags: moba, multiplayer, competitive
   
... (6개 더)

📁 결과 파일:
- 원본: C:\...\outputs\20251106\195530\artifacts\raw_games.json
- 랭킹: C:\...\outputs\20251106\195530\artifacts\ranked_games.json
- HTML: C:\...\outputs\20251106\195530\reports\game_ranking.html

💡 다음 단계:
1. HTML 리포트 열기: Start-Process outputs\20251106\195530\reports\game_ranking.html
2. JSON 확인: code outputs\20251106\195530\artifacts\ranked_games.json
3. 다른 쿼리: "puzzle" 또는 "rpg"로 재실행

============================================================
```

### 에러 발생 시

```
❌ 파이프라인 실패: 단계 2 (랭킹 계산)

원인: 필수 필드(rating, release_date)가 누락되었습니다

해결 방법:
입력 데이터 확인:
  - raw_games.json에 rating 필드 있는지 확인
  - release_date 필드 있는지 확인

다시 실행:
  game-pipeline "new games" "KR" 50

중간 결과는 보존되었습니다:
  outputs\20251106\195530\artifacts\raw_games.json (87개 게임)
```

---

## 사용 예시

### 예시 1: 기본 실행 (한국 신작 게임)
```
/game-pipeline
```
또는
```
/game-pipeline "new games" "KR" 50
```

### 예시 2: 퍼즐 게임 top 30
```
/game-pipeline "puzzle" "KR" 30
```

### 예시 3: 미국 액션 게임
```
/game-pipeline "action" "US" 50
```

### 예시 4: 일본 RPG 게임
```
/game-pipeline "rpg" "JP" 50
```

---

## 주의사항

1. **실행 시간**: 전체 파이프라인은 2-5분 소요됩니다
2. **Rate Limiting**: Google Play API 제한에 걸릴 수 있습니다
3. **결과 품질**: 검색 쿼리에 따라 게임 수집 품질이 달라집니다
4. **필수 필드**: raw_games.json에 rating, release_date, installs 필드가 필요합니다

## 개선 사항 (향후)

- [ ] 병렬 처리: 여러 쿼리를 동시에 실행
- [ ] 캐싱: 이미 분석한 게임은 재사용
- [ ] 증분 업데이트: 신규 게임만 추가 수집
- [ ] 자동 스케줄링: 매일 자동 실행
- [ ] 알림: 완료 시 이메일/Slack 알림

