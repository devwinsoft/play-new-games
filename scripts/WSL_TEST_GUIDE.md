# WSL 환경 테스트 가이드

Ubuntu WSL 환경에서 파이프라인을 테스트하는 가이드입니다.

## 🎯 사전 요구사항

### 1. WSL 설치 확인

```bash
# WSL 버전 확인
wsl --version

# Ubuntu 실행
wsl
```

### 2. Python 설치 (Ubuntu)

```bash
# Python 3 설치 확인
python3 --version

# pip 설치 확인
pip3 --version

# 없으면 설치
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

---

## 🚀 빠른 시작

### 1. 프로젝트로 이동

```bash
# WSL에서 Windows 드라이브로 이동
cd /mnt/c/Users/USER/Documents/Projects/play-new-games

# 또는 프로젝트 경로로 직접 이동
cd ~/play-new-games
```

### 2. 가상환경 설정

```bash
# 가상환경 생성 (Linux용)
python3 -m venv .venv

# 활성화
source .venv/bin/activate

# 프롬프트가 (.venv)로 시작하는지 확인
```

### 3. 의존성 설치

```bash
# pip 업그레이드
pip install --upgrade pip

# 의존성 설치
pip install -r requirements.txt

# 설치 확인
pip list | grep google-play-scraper
```

### 4. 파이프라인 실행

#### 방법 1: Python 직접 실행

```bash
# 기본 실행 (HTML 리포트 포함)
python scripts/run_pipeline.py --html

# 파라미터 지정
python scripts/run_pipeline.py \
  --query "new games" \
  --country KR \
  --top-k 50 \
  --html
```

#### 방법 2: Bash 스크립트 실행

```bash
# 실행 권한 부여 (처음 한 번만)
chmod +x scripts/run_pipeline.sh

# 실행
./scripts/run_pipeline.sh --html

# 파라미터 전달
./scripts/run_pipeline.sh --query puzzle --top-k 30 --html
```

---

## 🧪 테스트 시나리오

### 테스트 1: 빠른 테스트 (1-2분)

```bash
# 5개 게임만 수집, top 3 선정, HTML 생성
python scripts/run_pipeline.py \
  --limit 5 \
  --top-k 3 \
  --html \
  --log-level DEBUG
```

**기대 결과:**
- `outputs/20251107/HHMMSS/artifacts/raw_games.json` (5개 게임)
- `outputs/20251107/HHMMSS/artifacts/ranked_games.json` (3개 게임)
- `outputs/20251107/HHMMSS/reports/game_ranking.html`

### 테스트 2: 표준 테스트 (3-5분)

```bash
# 기본 설정으로 실행
python scripts/run_pipeline.py --html
```

**기대 결과:**
- 약 120개 게임 수집
- Top 50 선정
- HTML 리포트 생성

### 테스트 3: 특정 카테고리 (3-5분)

```bash
# 퍼즐 게임 탐색
python scripts/run_pipeline.py \
  --query puzzle \
  --country US \
  --language en \
  --top-k 30 \
  --html
```

### 테스트 4: 에러 처리

```bash
# 잘못된 국가 코드 (에러 핸들링 확인)
python scripts/run_pipeline.py \
  --query "test" \
  --country XX \
  --limit 5
```

---

## 📊 결과 확인

### 1. JSON 결과 확인

```bash
# 최신 결과 디렉토리 찾기
ls -lt outputs/$(date +%Y%m%d)/

# 특정 Run ID의 결과 확인
RUN_ID="103252"
cat outputs/$(date +%Y%m%d)/$RUN_ID/artifacts/raw_games.json | jq '.[0]'
cat outputs/$(date +%Y%m%d)/$RUN_ID/artifacts/ranked_games.json | jq '.[0]'
```

### 2. HTML 리포트 열기

#### WSL에서 Windows 브라우저로 열기:

```bash
# explorer.exe 사용
explorer.exe outputs/$(date +%Y%m%d)/103252/reports/game_ranking.html

# 또는 wslview 사용 (wslu 패키지 필요)
wslview outputs/$(date +%Y%m%d)/103252/reports/game_ranking.html
```

#### 리포트 내용 미리보기:

```bash
# HTML 파일 크기 확인
ls -lh outputs/$(date +%Y%m%d)/*/reports/*.html

# head 20 줄 확인
head -20 outputs/$(date +%Y%m%d)/103252/reports/game_ranking.html
```

### 3. 통계 확인

```bash
# 수집된 게임 수
cat outputs/$(date +%Y%m%d)/103252/artifacts/raw_games.json | jq 'length'

# 랭킹된 게임 수
cat outputs/$(date +%Y%m%d)/103252/artifacts/ranked_games.json | jq 'length'

# Top 5 게임 제목
cat outputs/$(date +%Y%m%d)/103252/artifacts/ranked_games.json | jq '.[0:5] | .[] | .title'

# 평균 점수 계산
cat outputs/$(date +%Y%m%d)/103252/artifacts/ranked_games.json | \
  jq '[.[] | .final_score] | add / length'
```

---

## 🔧 트러블슈팅

### 문제 1: 가상환경 활성화 실패

```bash
# Python 버전 확인
python3 --version

# venv 모듈 설치 확인
python3 -m venv --help

# 없으면 설치
sudo apt install python3-venv
```

### 문제 2: 의존성 설치 실패

```bash
# pip 업그레이드
pip install --upgrade pip

# 개별 패키지 설치 시도
pip install google-play-scraper
pip install python-dateutil
pip install colorlog
```

### 문제 3: 스크립트 실행 권한 없음

```bash
# 권한 부여
chmod +x scripts/run_pipeline.sh

# 권한 확인
ls -l scripts/run_pipeline.sh
```

### 문제 4: HTML 리포트가 안 열림

```bash
# wslu 패키지 설치 (wslview를 위해)
sudo apt install wslu

# 또는 Windows 경로로 직접 열기
powershell.exe start outputs/20251107/103252/reports/game_ranking.html
```

### 문제 5: 프로젝트 경로 못 찾음

```bash
# Windows 드라이브는 /mnt/ 아래에 마운트됨
cd /mnt/c/Users/USER/Documents/Projects/play-new-games

# 현재 디렉토리 확인
pwd

# 파일 목록 확인
ls -la
```

### 문제 6: 인코딩 에러

```bash
# 로케일 설정 확인
locale

# UTF-8 로케일 설정
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

# 영구 설정 (선택사항)
echo 'export LC_ALL=C.UTF-8' >> ~/.bashrc
echo 'export LANG=C.UTF-8' >> ~/.bashrc
```

---

## 🎯 고급 사용법

### 1. 별칭 설정

```bash
# ~/.bashrc 또는 ~/.zshrc에 추가
alias game-pipeline='python scripts/run_pipeline.py'

# 적용
source ~/.bashrc

# 사용
game-pipeline --query puzzle --html
```

### 2. 배치 실행

```bash
# 여러 쿼리 순차 실행
for query in "puzzle" "action" "rpg"; do
  echo "Processing: $query"
  python scripts/run_pipeline.py \
    --query "$query" \
    --top-k 20 \
    --html
done
```

### 3. 결과 백업

```bash
# 오늘 실행 결과 압축
tar -czf game-results-$(date +%Y%m%d).tar.gz outputs/$(date +%Y%m%d)/

# 백업 확인
ls -lh game-results-*.tar.gz
```

### 4. 로그 저장

```bash
# 실행 로그 파일로 저장
python scripts/run_pipeline.py --html 2>&1 | tee pipeline.log

# 로그 확인
less pipeline.log
```

---

## 📈 성능 최적화

### 1. 병렬 처리 (미래 기능)

```bash
# 여러 쿼리 병렬 실행 (GNU parallel)
parallel -j 3 'python scripts/run_pipeline.py --query {} --html' ::: puzzle action rpg
```

### 2. 캐시 활용

```bash
# 이전 결과 재사용
# 예: raw data 재활용하여 다른 top-k로 재랭킹
python skills/ranker/scorer.py
```

### 3. 리소스 모니터링

```bash
# CPU/메모리 사용량 확인
top

# 또는 htop
sudo apt install htop
htop
```

---

## 📚 추가 자료

- **Python 스크립트 문서**: `scripts/README.md`
- **스킬 문서**: `skills/*/SKILL.md`
- **전체 테스트 가이드**: `TEST_GUIDE.md`

---

## 🎉 성공 기준

다음을 모두 확인하면 테스트 성공입니다:

- [ ] 가상환경 활성화 완료
- [ ] 의존성 설치 완료
- [ ] 파이프라인 실행 성공
- [ ] `raw_games.json` 생성 확인
- [ ] `ranked_games.json` 생성 확인
- [ ] `game_ranking.html` 생성 확인
- [ ] HTML 리포트를 브라우저에서 열어서 확인

---

Happy Testing in WSL! 🐧🎮

