---
name: ingest_play
description: Google Play에서 신작 게임 메타데이터를 수집하여 표준 스키마로 정규화합니다. 게임 데이터 수집이 필요할 때 사용하세요.
---

# ingest_play

Google Play 스토어에서 신작 게임 메타데이터를 수집하고 정규화하는 스킬입니다.

## Metadata

- **version**: 0.2.0  
- **entry**: `python skills/ingest_play/handler.py`  
- **runtime**: python3

## When to Use This Skill

다음과 같은 경우에 이 스킬을 사용하세요:

- Google Play 스토어에서 게임 데이터를 수집해야 할 때
- 신작 게임 정보가 필요할 때
- 특정 장르나 키워드의 게임을 검색해야 할 때
- 게임 메타데이터를 표준 스키마로 정규화해야 할 때

## Directory Layout

```
skills/ingest_play/
├─ handler.py           # 실행 엔트리 (데이터 수집)
├─ normalize.py         # 필드 정규화 / 중복 제거
├─ adapters/            # 외부 API / 스크래퍼 모듈
│  └─ play_store.py    # Google Play Store 어댑터
├─ tests/              # 단위 테스트
└─ README.md           # 상세 문서
```

출력 경로: `outputs/{날짜}/{run_id}/artifacts/raw_games.json`

## Permissions

- `network` - Google Play Store API 접근
- `write(outputs)` - 결과 파일 저장

## Environment Variables

| 변수 | 필수 | 기본값 | 설명 |
|------|------|--------|------|
| `LOG_LEVEL` | No | `INFO` | 로그 레벨 (DEBUG, INFO, WARNING, ERROR) |
| `QUERY` | No | `"new games"` | 검색 쿼리 |
| `COUNTRY` | No | `"KR"` | 국가 코드 (KR, US, JP 등) |
| `LANGUAGE` | No | `"ko"` | 언어 코드 (ko, en, ja 등) |
| `LIMIT` | No | `120` | 수집할 최대 게임 수 |

## Inputs

| name | type | required | default | description |
|------|------|----------|---------|-------------|
| query | string | false | `"new games"` | 검색 쿼리 |
| country | string | false | `"KR"` | 국가 코드 |
| language | string | false | `"ko"` | 언어 코드 |
| limit | integer | false | `120` | 최대 수집 게임 수 |

## Outputs

| name | type | example |
|------|------|---------|
| `raw_items_path` | file | `outputs/20251106/142530/artifacts/raw_games.json` |

## Output Schema

배열 JSON 형식의 Google Play 게임 메타데이터:

```json
[
  {
    "package_name": "com.example.game",
    "title": "Game Title",
    "developer": "Dev Studio",
    "genre": "Action",
    "description": "게임 설명...",
    "rating": 4.6,
    "ratings_count": 1234,
    "installs": 50000,
    "release_date": "2025-11-03",
    "icon_url": "https://...",
    "screenshots": ["https://...", "..."],
    "store_url": "https://play.google.com/store/apps/details?id=com.example.game",
    "price": 0,
    "free": true,
    "content_rating": "Everyone",
    "updated": "2025-11-05"
  }
]
```

## Core Workflow

1. **데이터 수집**: Google Play Store에서 검색 쿼리로 게임 검색
2. **상세 정보 가져오기**: 각 게임의 상세 메타데이터 수집
3. **데이터 정규화**: 표준 스키마로 필드 변환
4. **게임 필터링**: 게임만 남기고 다른 앱 제거
5. **중복 제거**: package_name 기준으로 중복 제거
6. **결과 저장**: JSON 파일로 저장

## Usage Examples

### 기본 사용 (한국 신작 게임)

```bash
python skills/ingest_play/handler.py
```

### 특정 장르 검색

```bash
QUERY="rpg games" LIMIT=50 python skills/ingest_play/handler.py
```

### 다른 국가 스토어

```bash
QUERY="puzzle" COUNTRY="US" LANGUAGE="en" python skills/ingest_play/handler.py
```

### 디버그 모드

```bash
LOG_LEVEL="DEBUG" LIMIT=10 python skills/ingest_play/handler.py
```

## Best Practices

1. **적절한 LIMIT 설정**: 테스트 시에는 작은 값(10-20)으로 시작
2. **Rate Limiting 주의**: Google Play API 제한을 고려하여 적절한 간격으로 실행
3. **국가별 결과 차이**: 국가마다 다른 게임이 검색될 수 있음
4. **검색 쿼리 최적화**: 구체적인 키워드로 원하는 게임 타입 검색

## Troubleshooting

| 문제 | 원인 | 해결 방법 |
|------|------|-----------|
| 데이터 0개 수집 | 네트워크 문제, 검색 결과 없음 | 인터넷 연결 확인, 다른 쿼리 시도 |
| Rate limiting 에러 | API 요청 제한 초과 | 잠시 대기 후 재시도, LIMIT 감소 |
| ModuleNotFoundError | 의존성 미설치 | `pip install -r requirements.txt` |

## Dependencies

- `google-play-scraper>=1.2.4` - Google Play Store 데이터 수집
- `python-dateutil>=2.8.2` - 날짜 파싱
- `colorlog>=6.8.0` - 컬러 로그 출력

## Integration

이 스킬의 출력은 다음 스킬의 입력으로 사용될 수 있습니다:

- **enrich_llm**: LLM을 사용한 게임 태깅 및 요약
- **ranker**: 게임 랭킹 및 점수 계산

## Additional Notes

- 게임만 필터링되며 다른 앱은 자동 제외됨
- 중복 제거는 package_name 기준으로 수행
- 날짜 형식은 자동으로 YYYY-MM-DD로 정규화
- 설치 수는 문자열("10,000+")에서 정수로 변환

자세한 내용은 `skills/ingest_play/README.md`를 참조하세요.
