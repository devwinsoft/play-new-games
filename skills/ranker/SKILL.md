---
name: ranker
description: 신규성/품질/인기도 점수를 계산하고 다양성을 고려해 상위 N개를 선정합니다. 게임 랭킹이 필요할 때 사용하세요.
---

# ranker

게임의 신규성, 품질, 인기도를 기반으로 점수를 계산하고 다양성을 고려한 랭킹을 생성하는 스킬입니다.

## Metadata

- **version**: 0.1.5  
- **entry**: `python skills/ranker/scorer.py`  
- **runtime**: python3

## When to Use This Skill

다음과 같은 경우에 이 스킬을 사용하세요:

- 게임들의 순위를 매겨야 할 때
- 신규성과 품질을 동시에 고려한 추천이 필요할 때
- 다양한 장르의 게임을 균형있게 선정해야 할 때
- 상위 N개 게임만 선별해야 할 때

## Directory Layout

```
skills/ranker/
├─ scorer.py          # 점수 계산 엔트리
├─ mmr.py            # 다양성(MMR) 재랭킹 모듈
├─ utils/            # 통계 함수 / 베이지안 계산
└─ tests/            # 단위 테스트
```

출력 경로: `outputs/{날짜}/{run_id}/artifacts/ranked_games.json`

## Permissions

- `read` - 입력 파일 읽기
- `write(outputs)` - 결과 파일 저장

## Environment Variables

| 변수 | 필수 | 기본값 | 설명 |
|------|------|--------|------|
| `LOG_LEVEL` | No | `INFO` | 로그 레벨 |

## Inputs

| name | type | required | default | description |
|------|------|----------|---------|-------------|
| raw_items_path | file | true | - | ingest_play 스킬의 출력 파일 경로 (또는 enriched_items_path) |
| top_k | integer | false | 50 | 선정할 상위 게임 수 |

## Outputs

| name | type | example |
|------|------|---------|
| `ranked_items_path` | file | `outputs/20251106/142530/artifacts/ranked_games.json` |

## Output Schema

랭킹된 게임 배열 (점수 높은 순):

```json
[
  {
    "rank": 1,
    "package_name": "com.example.game",
    "title": "Game Title",
    "final_score": 0.85,
    "scores": {
      "freshness": 0.92,
      "quality": 0.85,
      "popularity": 0.78
    },
    "tags": ["roguelike", "pixel-art"],
    "summary_kr": "게임 요약...",
    "rating": 4.5,
    "release_date": "2025-11-01"
  }
]
```

## Scoring Algorithm

게임의 최종 점수는 다음 공식으로 계산됩니다:

```
freshness = exp(-days_since_release / τ)
quality = bayesian_mean(rating, ratings_count)
popularity = minmax_normalize(installs)

final_score = 0.45 × quality + 0.35 × freshness + 0.20 × popularity
```

### 점수 구성 요소

1. **신규성 (Freshness, 35%)**
   - 출시일 기준 시간 경과에 따른 감쇠
   - 최근 출시된 게임일수록 높은 점수

2. **품질 (Quality, 45%)**
   - 베이지안 평균으로 평점과 평가 수 반영
   - 평가 수가 적으면 평균으로 회귀

3. **인기도 (Popularity, 20%)**
   - 설치 수 기반 정규화
   - MinMax 스케일링 적용

### 다양성 재랭킹 (MMR)

Maximal Marginal Relevance 알고리즘으로 장르 다양성 확보:
- 이미 선정된 게임과 다른 장르 우대
- 편향 방지 (특정 장르만 선정되는 것 방지)

## Core Workflow

1. **입력 파일 읽기**: raw_items_path에서 게임 데이터 로드
2. **점수 계산**: 신규성, 품질, 인기도 점수 계산
3. **최종 점수**: 가중 평균으로 최종 점수 산출
4. **다양성 재랭킹**: MMR 알고리즘으로 장르 다양성 고려
5. **상위 선정**: top_k 개수만큼 선정
6. **결과 저장**: ranked_games.json으로 저장

## Usage Examples

### 기본 사용 (상위 50개)

```bash
RAW_ITEMS_PATH="outputs/20251106/142530/artifacts/raw_games.json" python skills/ranker/scorer.py
```

### 상위 30개 선정

```bash
RAW_ITEMS_PATH="outputs/20251106/142530/artifacts/raw_games.json" TOP_K=30 python skills/ranker/scorer.py
```

### 환경 변수로 설정

```bash
export RAW_ITEMS_PATH="outputs/20251106/142530/artifacts/raw_games.json"
export TOP_K=100
python skills/ranker/scorer.py
```

## Best Practices

1. **적절한 top_k 설정**: 용도에 맞게 상위 개수 조정
2. **다양성 확보**: MMR 알고리즘으로 장르 편향 방지
3. **가중치 조정**: 프로젝트 목적에 맞게 가중치 커스터마이징
4. **평가 수 고려**: 베이지안 평균으로 신뢰도 반영

## Troubleshooting

| 문제 | 원인 | 해결 방법 |
|------|------|-----------|
| 입력 파일 없음 | 경로 오류 | raw_items_path 확인 |
| 점수 계산 오류 | 필수 필드 누락 | 입력 데이터 스키마 확인 (rating, release_date, installs) |
| 편향된 결과 | MMR 미적용 | 다양성 파라미터 조정 |

## Customization

### 가중치 조정

`scorer.py`에서 가중치 변경 가능:

```python
WEIGHT_QUALITY = 0.45     # 품질 가중치
WEIGHT_FRESHNESS = 0.35   # 신규성 가중치
WEIGHT_POPULARITY = 0.20  # 인기도 가중치
```

### 신규성 감쇠 시간

```python
TAU = 30  # 감쇠 시간 상수 (일)
```

## Dependencies

- `numpy` - 수치 계산
- `scipy` - 통계 함수

## Integration

- **입력**: `ingest_play` 스킬의 출력 사용 (또는 `enrich_llm` 출력도 가능)
- **출력**: `publish` 스킬의 입력으로 제공

## Additional Notes

- 베이지안 평균으로 평가 수 적은 게임의 과대평가 방지
- MMR 알고리즘으로 장르 다양성 확보
- 시간 감쇠 함수로 신규성 반영
- 설치 수는 로그 스케일로 정규화 가능
