#!/usr/bin/env python3
"""
enrich_llm skill handler
Uses Claude API to enrich game metadata with tags, summaries, and keywords
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import anthropic

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_games(raw_items_path: str) -> List[Dict[str, Any]]:
    """Load raw game data from JSON file"""
    with open(raw_items_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def enrich_game(client: anthropic.Anthropic, game: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enrich a single game with LLM-generated metadata

    Returns the game dict with added fields:
    - tags: list of genre/theme tags
    - summary_kr: Korean summary (2-3 sentences)
    - keywords: list of keywords
    - safety_flags: {adult: bool, gambling: bool}
    """
    prompt = f"""게임 정보를 분석하여 다음을 제공해주세요:

게임 제목: {game.get('title', 'N/A')}
개발사: {game.get('developer', 'N/A')}
장르: {game.get('genre', 'N/A')}
설명: {game.get('description', 'N/A')[:500]}

다음 형식의 JSON으로 응답해주세요:
{{
  "tags": ["tag1", "tag2", "tag3"],
  "summary_kr": "2-3문장 요약",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "safety_flags": {{
    "adult": false,
    "gambling": false
  }}
}}

태그는 영문 소문자로, 게임의 핵심 특성을 나타내는 3-5개를 선정해주세요.
요약은 한국어로 2-3문장으로 게임의 핵심 내용을 설명해주세요.
키워드는 영문 소문자로, 게임의 주요 메커니즘이나 특징을 나타내는 3-5개를 선정해주세요.
안전성 플래그는 성인 콘텐츠나 도박 요소가 있는지 판단해주세요."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract JSON from response
        response_text = message.content[0].text

        # Try to find JSON in the response
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1

        if start_idx >= 0 and end_idx > start_idx:
            json_str = response_text[start_idx:end_idx]
            enrichment = json.loads(json_str)

            # Merge enrichment with original game data
            enriched_game = {**game, **enrichment}
            return enriched_game
        else:
            logger.warning(f"Could not extract JSON from response for game: {game.get('title')}")
            return game

    except Exception as e:
        logger.error(f"Error enriching game {game.get('title')}: {e}")
        return game


def save_enriched_games(games: List[Dict[str, Any]], run_id: str) -> str:
    """Save enriched games to output file"""
    # Create output directory
    today = datetime.now().strftime("%Y%m%d")
    output_dir = Path(f"outputs/{today}/{run_id}/artifacts")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "enriched_games.json"

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(games, f, ensure_ascii=False, indent=2)

    return str(output_path.absolute())


def main():
    logger.info("=" * 60)
    logger.info("enrich_llm - LLM Game Metadata Enrichment")
    logger.info("=" * 60)

    # Get environment variables
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        logger.error("ANTHROPIC_API_KEY environment variable is required")
        sys.exit(1)

    raw_items_path = os.getenv('RAW_ITEMS_PATH')
    if not raw_items_path:
        logger.error("RAW_ITEMS_PATH environment variable is required")
        sys.exit(1)

    run_id = os.getenv('RUN_ID', datetime.now().strftime("%H%M%S"))

    logger.info(f"Raw items path: {raw_items_path}")
    logger.info(f"Run ID: {run_id}")
    logger.info("=" * 60)

    # Load games
    logger.info("Step 1: Loading game data...")
    games = load_games(raw_items_path)
    logger.info(f"Loaded {len(games)} games")

    # Initialize Claude client
    client = anthropic.Anthropic(api_key=api_key)

    # Enrich games
    logger.info("Step 2: Enriching games with LLM...")
    enriched_games = []
    for i, game in enumerate(games, 1):
        logger.info(f"Processing game {i}/{len(games)}: {game.get('title')}")
        enriched_game = enrich_game(client, game)
        enriched_games.append(enriched_game)

    success_count = sum(1 for g in enriched_games if 'tags' in g)
    logger.info(f"Successfully enriched {success_count}/{len(games)} games")

    # Save results
    logger.info("Step 3: Saving results...")
    output_path = save_enriched_games(enriched_games, run_id)

    logger.info("=" * 60)
    logger.info("✓ Success!")
    logger.info(f"Total games enriched: {success_count}/{len(games)}")
    logger.info(f"Output file: {output_path}")
    logger.info("=" * 60)

    # Output JSON for pipeline
    result = {
        "enriched_items_path": output_path,
        "total_items": len(enriched_games),
        "success_count": success_count,
        "run_id": run_id
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()
