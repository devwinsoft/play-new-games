---
name: publish_html
description: 랭킹된 게임 데이터를 기반으로 시각적인 HTML 리포트를 생성합니다. 결과를 웹 페이지로 보고 싶을 때 사용하세요.
---

# publish_html

ranker 스킬의 결과를 받아 시각적이고 인터랙티브한 HTML 리포트를 생성하는 스킬입니다.

## Metadata

- **version**: 1.0.0  
- **entry**: `python skills/publish_html/handler.py`  
- **runtime**: python3

## When to Use This Skill

다음과 같은 경우에 이 스킬을 사용하세요:

- 랭킹 결과를 시각적으로 보고 싶을 때
- 웹 브라우저에서 결과를 확인하고 싶을 때
- 게임 순위, 점수, 메타데이터를 한눈에 보고 싶을 때
- 공유 가능한 HTML 리포트가 필요할 때

## Directory Layout

```
skills/publish_html/
├─ handler.py          # 메인 실행 파일
├─ tests/             # 단위 테스트
└─ SKILL.md           # 이 파일
```

출력 경로: `outputs/{날짜}/{run_id}/reports/game_ranking.html`

## Permissions

- `read` - 입력 파일 읽기
- `write(outputs)` - HTML 파일 저장

## Environment Variables

| 변수 | 필수 | 기본값 | 설명 |
|------|------|--------|------|
| `RANKED_ITEMS_PATH` | **Yes** | - | ranked_games.json 파일 경로 |
| `QUERY` | No | `"new games"` | 검색 쿼리 (헤더에 표시) |
| `COUNTRY` | No | `"KR"` | 국가 코드 (헤더에 표시) |
| `RUN_ID` | No | 자동 생성 | 실행 ID |
| `LOG_LEVEL` | No | `INFO` | 로그 레벨 |

## Inputs

| name | type | required | description |
|------|------|----------|-------------|
| ranked_items_path | file | true | ranker 스킬의 출력 파일 (ranked_games.json) |
| query | string | false | 검색 쿼리 (리포트 제목용) |
| country | string | false | 국가 코드 (리포트 제목용) |

## Outputs

| name | type | example |
|------|------|---------|
| `html_report_path` | file | `outputs/20251107/142530/reports/game_ranking.html` |

## Output Features

생성되는 HTML 리포트는 다음 기능을 포함합니다:

### 1. **헤더 섹션**
- 검색 쿼리 및 국가 정보
- 생성 날짜

### 2. **통계 카드**
- 총 게임 수
- 평균 점수
- 장르 수

### 3. **게임 카드**
각 게임마다:
- 순위 배지 (1-3위 금색, 4-10위 은색, 나머지 동색)
- 게임 제목 및 개발사
- 장르, 평점, 설치 수 배지
- 출시일
- 최종 점수 (크게 표시)
- 점수 세부사항 (품질, 신규성, 인기도 바 차트)

### 4. **장르 분포 차트**
- Chart.js를 사용한 인터랙티브 바 차트
- 상위 5개 장르 표시

### 5. **반응형 디자인**
- 모바일/태블릿/데스크톱 모두 지원
- 다크/라이트 그라디언트 배경
- 호버 효과 및 애니메이션

## Core Workflow

1. **입력 파일 읽기**: ranked_items_path에서 JSON 로드
2. **통계 계산**: 게임 수, 평균 점수, 장르 분포
3. **HTML 생성**: 템플릿 기반 HTML 생성
4. **파일 저장**: reports/ 디렉토리에 저장
5. **경로 반환**: 생성된 HTML 파일 경로 출력

## Usage Examples

### 기본 사용

```bash
RANKED_ITEMS_PATH="outputs/20251107/142530/artifacts/ranked_games.json" python skills/publish_html/handler.py
```

### 파라미터 지정

```bash
RANKED_ITEMS_PATH="outputs/20251107/142530/artifacts/ranked_games.json" \
QUERY="puzzle" \
COUNTRY="KR" \
python skills/publish_html/handler.py
```

### 환경 변수로 설정

```bash
export RANKED_ITEMS_PATH="outputs/20251107/142530/artifacts/ranked_games.json"
export QUERY="action games"
export COUNTRY="US"
python skills/publish_html/handler.py
```

## Best Practices

1. **브라우저에서 바로 열기**: 생성된 HTML은 외부 의존성 없이 작동 (CDN 사용)
2. **공유**: HTML 파일을 이메일이나 웹 서버로 공유 가능
3. **아카이브**: 각 실행마다 새로운 디렉토리에 저장되어 히스토리 유지
4. **커스터마이징**: handler.py의 CSS/HTML을 수정하여 디자인 변경 가능

## Troubleshooting

| 문제 | 원인 | 해결 방법 |
|------|------|-----------|
| 입력 파일 없음 | 경로 오류 | ranked_items_path 확인 |
| HTML 깨짐 | 특수문자 | UTF-8 인코딩 확인 |
| 차트 안 나옴 | 네트워크 | Chart.js CDN 접근 확인 |

## Dependencies

- **없음** - Python 표준 라이브러리만 사용
- **Chart.js** (CDN) - 차트 렌더링용 (HTML 내 CDN 링크)

## Integration

- **입력**: `ranker` 스킬의 출력 사용
- **출력**: 독립적인 HTML 파일 (공유 가능)

## HTML Preview

생성되는 HTML은 다음과 같은 구조입니다:

```
┌─────────────────────────────────────┐
│  🎮 게임 랭킹 리포트                │
│  puzzle · KR · 2025-11-07           │
├─────────────────────────────────────┤
│  [50]  [0.845]  [15]                │
│  게임수  평균점수  장르수            │
├─────────────────────────────────────┤
│  🏆 상위 랭킹 게임                  │
│                                     │
│  ┌───┬─────────────────┬────────┐  │
│  │#1 │ 게임 제목       │ 0.920 │  │
│  │   │ 개발사          │────── │  │
│  │   │ [장르][⭐4.5]   │ 품질  │  │
│  │   │ 출시일          │ 신규성│  │
│  └───┴─────────────────┴────────┘  │
│  ...                                │
├─────────────────────────────────────┤
│  📊 장르 분포                       │
│  [인터랙티브 바 차트]               │
└─────────────────────────────────────┘
```

## Customization

### 색상 변경

`handler.py`의 `generate_html` 함수에서 CSS 수정:

```python
# 그라디언트 배경
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

# 순위 배지 색상
badge_color = "#FFD700"  # 금색
```

### 차트 타입 변경

HTML 내 Chart.js 설정 수정:

```javascript
type: 'bar'  // 'pie', 'doughnut', 'line' 등으로 변경 가능
```

### 표시 게임 수 제한

상위 N개만 표시하려면:

```python
game_cards_html = ""
for game in games[:20]:  # 상위 20개만
    ...
```

## Additional Notes

- HTML 파일은 완전히 독립적 (외부 CSS/JS 파일 불필요, CDN만 필요)
- 모든 스타일이 인라인으로 포함되어 있어 단일 파일로 공유 가능
- Chart.js는 CDN에서 로드 (인터넷 연결 필요)
- UTF-8 인코딩으로 한글 완벽 지원
- 반응형 디자인으로 모든 기기에서 작동

## Example Output

생성된 HTML을 브라우저에서 열면:
- 상단에 그라디언트 배경
- 카드 형식의 게임 목록
- 호버 시 카드가 살짝 올라오는 효과
- 각 게임의 점수가 컬러풀한 바로 시각화
- 하단에 장르 분포 차트

파일 경로:
```
outputs/20251107/142530/reports/game_ranking.html
```

브라우저로 열기:
```powershell
# Windows
start outputs\20251107\142530\reports\game_ranking.html

# 또는 VSCode에서
code outputs\20251107\142530\reports\game_ranking.html
```

