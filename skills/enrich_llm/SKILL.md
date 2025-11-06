---
name: enrich_llm
description: Claude를 사용해 게임에 장르/테마 태깅, 2-3줄 요약, 키워드 추출을 수행합니다. 수집된 게임 데이터를 풍부하게 만들 때 사용하세요.
---

# enrich_llm

LLM(Claude)을 사용하여 게임 메타데이터를 풍부하게 만드는 스킬입니다.

## Metadata

- **version**: 0.3.1  
- **entry**: `python skills/enrich_llm/handler.py`  
- **runtime**: python3

## When to Use This Skill

다음과 같은 경우에 이 스킬을 사용하세요:

- 게임에 태그를 자동으로 추가해야 할 때
- 게임 설명을 요약해야 할 때
- 게임의 핵심 키워드를 추출해야 할 때
- 게임의 안전성 플래그(성인/도박 콘텐츠)를 판단해야 할 때

## Directory Layout

```
skills/enrich_llm/
├─ handler.py          # 메인 로직 (Claude 호출)
├─ prompts/           # 프롬프트 템플릿
├─ schema.py          # 출력 스키마 정의
├─ adapters/          # API 요청/응답 헬퍼
└─ tests/            # 단위 테스트
```

출력 경로: `outputs/{날짜}/{run_id}/artifacts/enriched_games.json`

## Permissions

- `network` - Claude API 호출
- `read` - 입력 파일 읽기
- `write(outputs)` - 결과 파일 저장

## Environment Variables

| 변수 | 필수 | 기본값 | 설명 |
|------|------|--------|------|
| `ANTHROPIC_API_KEY` | **Yes** | - | Claude API 키 |
| `LOG_LEVEL` | No | `INFO` | 로그 레벨 |

## Inputs

| name | type | required | description |
|------|------|----------|-------------|
| raw_items_path | file | true | ingest_play 스킬의 출력 파일 경로 |

## Outputs

| name | type | example |
|------|------|---------|
| `enriched_items_path` | file | `outputs/20251106/142530/artifacts/enriched_games.json` |

## Output Schema

배열 JSON. 원본 필드 + LLM 생성 필드:

```json
[
  {
    "package_name": "com.example.game",
    "title": "Game Title",
    "developer": "Dev Studio",
    "genre": "Action",
    "description": "게임 설명...",
    "rating": 4.5,
    
    "tags": ["roguelike", "pixel-art", "indie"],
    "summary_kr": "덱 빌딩과 로그라이크 요소가 결합된 픽셀 아트 게임입니다.",
    "keywords": ["deck-building", "permadeath", "procedural-generation"],
    "safety_flags": {
      "adult": false,
      "gambling": false
    }
  }
]
```

## Core Workflow

1. **입력 파일 읽기**: raw_items_path에서 게임 데이터 로드
2. **Claude API 호출**: 각 게임에 대해 태깅, 요약, 키워드 추출
3. **결과 병합**: 원본 데이터 + LLM 생성 데이터 결합
4. **결과 저장**: enriched_games.json으로 저장

## Usage Examples

### 기본 사용

```bash
ANTHROPIC_API_KEY="sk-..." raw_items_path="outputs/20251106/142530/artifacts/raw_games.json" python skills/enrich_llm/handler.py
```

### 환경 변수로 설정

```bash
export ANTHROPIC_API_KEY="sk-..."
export RAW_ITEMS_PATH="outputs/20251106/142530/artifacts/raw_games.json"
python skills/enrich_llm/handler.py
```

## Best Practices

1. **API 키 보안**: 환경 변수로 관리, 코드에 직접 포함하지 말 것
2. **배치 처리**: 대량 게임 처리 시 적절한 간격 설정
3. **에러 처리**: 일부 게임 처리 실패해도 계속 진행
4. **요약 품질**: 한국어 요약이 필요하면 프롬프트 조정

## Troubleshooting

| 문제 | 원인 | 해결 방법 |
|------|------|-----------|
| API 키 에러 | 환경 변수 미설정 | `ANTHROPIC_API_KEY` 설정 확인 |
| Rate limit 에러 | API 요청 한도 초과 | 잠시 대기 후 재시도 |
| 입력 파일 없음 | 경로 오류 | raw_items_path 경로 확인 |

## Dependencies

- `anthropic` - Claude API 클라이언트

## Integration

- **입력**: `ingest_play` 스킬의 출력 사용
- **출력**: `ranker` 스킬의 입력으로 제공

## Additional Notes

- 병렬 처리로 여러 게임 동시 처리 가능
- 프롬프트 템플릿은 `prompts/` 디렉토리에서 커스터마이징
- 안전성 플래그는 설명 기반으로 자동 판단
