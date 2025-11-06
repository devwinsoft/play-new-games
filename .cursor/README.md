# Cursor Configuration

이 디렉토리는 Cursor IDE의 프로젝트별 설정을 포함합니다.

## 파일 설명

- `config.yaml` - 프로젝트 전체 설정
- `skills.yaml` - 사용 가능한 스킬 목록
- `README.md` - 이 파일

## 스킬 탐지

Cursor는 다음 방법으로 스킬을 자동 탐지합니다:

1. `skills/` 디렉토리의 모든 하위 디렉토리 스캔
2. 각 디렉토리에서 `SKILL.md` 또는 `skill.md` 파일 검색
3. 파일 상단의 YAML 프론트매터 파싱:

```yaml
---
name: skill-name
description: Skill description and when to use it
---
```

## 스킬 사용 방법

1. 채팅에서 스킬 이름을 언급하거나
2. 스킬이 처리하는 작업을 요청하면 자동으로 매칭됩니다

예: "Google Play에서 게임 데이터를 수집해줘" → `ingest_play` 스킬 활성화

## 트러블슈팅

### 스킬이 탐지되지 않는 경우

1. **Cursor 재시작**: Cursor를 완전히 종료하고 다시 시작
2. **프로젝트 다시 열기**: File > Open Folder로 프로젝트 재오픈
3. **SKILL.md 형식 확인**: 프론트매터가 올바른 YAML 형식인지 확인
4. **캐시 삭제**: Cursor의 캐시를 삭제하고 다시 시작

### 프론트매터 형식

올바른 형식:
```yaml
---
name: my-skill
description: What this skill does
---

# Skill content starts here
```

잘못된 형식:
```markdown
# SKILL.md

```markdown
content...
```
```

## 참고 자료

- 프로젝트 README: `../README.md`
- 스킬 인덱스: `../skills/skill-index.yaml`
- Cursor Rules: `../.cursorrules`

