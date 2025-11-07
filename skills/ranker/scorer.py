#!/usr/bin/env python3
"""
ranker skill scorer
Calculates freshness, quality, and popularity scores for games
"""

import os
import sys
import json
import logging
import math
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Scoring weights
WEIGHT_QUALITY = 0.45
WEIGHT_FRESHNESS = 0.35
WEIGHT_POPULARITY = 0.20

# Freshness decay constant (days)
TAU = 30

# Bayesian average parameters
PRIOR_RATING = 4.0
PRIOR_COUNT = 10


def load_games(items_path: str) -> List[Dict[str, Any]]:
    """Load game data from JSON file (raw or enriched)"""
    with open(items_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def calculate_freshness(release_date_str: str) -> float:
    """
    Calculate freshness score based on release date
    Uses exponential decay: freshness = exp(-days_since_release / τ)
    """
    try:
        # Parse release date (format: YYYY-MM-DD)
        release_date = datetime.strptime(release_date_str, "%Y-%m-%d")
        today = datetime.now()
        days_since_release = (today - release_date).days

        # Exponential decay
        freshness = math.exp(-days_since_release / TAU)
        return max(0.0, min(1.0, freshness))
    except Exception as e:
        logger.warning(f"Error calculating freshness for date {release_date_str}: {e}")
        return 0.5


def calculate_quality(rating: float, ratings_count: int) -> float:
    """
    Calculate quality score using Bayesian average
    Prevents games with few ratings from being overrated
    """
    try:
        # Bayesian average
        bayesian_rating = (PRIOR_COUNT * PRIOR_RATING + ratings_count * rating) / (PRIOR_COUNT + ratings_count)

        # Normalize to 0-1 scale (assuming ratings are 0-5)
        normalized = bayesian_rating / 5.0
        return max(0.0, min(1.0, normalized))
    except Exception as e:
        logger.warning(f"Error calculating quality for rating {rating}, count {ratings_count}: {e}")
        return 0.5


def calculate_popularity(installs: int, all_installs: List[int]) -> float:
    """
    Calculate popularity score using MinMax normalization
    """
    try:
        if not all_installs:
            return 0.5

        min_installs = min(all_installs)
        max_installs = max(all_installs)

        if max_installs == min_installs:
            return 0.5

        # MinMax normalization
        popularity = (installs - min_installs) / (max_installs - min_installs)
        return max(0.0, min(1.0, popularity))
    except Exception as e:
        logger.warning(f"Error calculating popularity for installs {installs}: {e}")
        return 0.5


def score_games(games: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Calculate scores for all games
    """
    # Collect all install counts for normalization
    all_installs = [g.get('installs', 0) for g in games]

    scored_games = []
    for game in games:
        # Calculate individual scores
        freshness = calculate_freshness(game.get('release_date', '2020-01-01'))
        quality = calculate_quality(
            game.get('rating', 4.0),
            game.get('ratings_count', 0)
        )
        popularity = calculate_popularity(
            game.get('installs', 0),
            all_installs
        )

        # Calculate final score (weighted average)
        final_score = (
            WEIGHT_QUALITY * quality +
            WEIGHT_FRESHNESS * freshness +
            WEIGHT_POPULARITY * popularity
        )

        # Add scores to game data
        game_with_scores = {
            **game,
            'scores': {
                'freshness': round(freshness, 4),
                'quality': round(quality, 4),
                'popularity': round(popularity, 4)
            },
            'final_score': round(final_score, 4)
        }

        scored_games.append(game_with_scores)

    return scored_games


def rank_games(games: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    """
    Rank games by final score and select top K
    """
    # Sort by final score (descending)
    sorted_games = sorted(games, key=lambda g: g['final_score'], reverse=True)

    # Select top K
    top_games = sorted_games[:top_k]

    # Add rank
    for i, game in enumerate(top_games, 1):
        game['rank'] = i

    return top_games


def save_ranked_games(games: List[Dict[str, Any]], run_id: str) -> str:
    """Save ranked games to output file"""
    # Create output directory
    today = datetime.now().strftime("%Y%m%d")
    output_dir = Path(f"outputs/{today}/{run_id}/artifacts")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "ranked_games.json"

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(games, f, ensure_ascii=False, indent=2)

    return str(output_path.absolute())


def main():
    logger.info("=" * 60)
    logger.info("ranker - Game Ranking & Scoring")
    logger.info("=" * 60)

    # Get environment variables
    # Support both RAW_ITEMS_PATH and ENRICHED_ITEMS_PATH for backward compatibility
    items_path = os.getenv('RAW_ITEMS_PATH') or os.getenv('ENRICHED_ITEMS_PATH')
    if not items_path:
        logger.error("RAW_ITEMS_PATH or ENRICHED_ITEMS_PATH environment variable is required")
        sys.exit(1)

    top_k = int(os.getenv('TOP_K', '50'))
    run_id = os.getenv('RUN_ID', datetime.now().strftime("%H%M%S"))

    logger.info(f"Items path: {items_path}")
    logger.info(f"Top K: {top_k}")
    logger.info(f"Run ID: {run_id}")
    logger.info("=" * 60)

    # Load games
    logger.info("Step 1: Loading game data...")
    games = load_games(items_path)
    logger.info(f"Loaded {len(games)} games")

    # Calculate scores
    logger.info("Step 2: Calculating scores...")
    scored_games = score_games(games)
    logger.info(f"Scored {len(scored_games)} games")

    # Rank games
    logger.info("Step 3: Ranking and selecting top games...")
    top_games = rank_games(scored_games, top_k)
    logger.info(f"Selected top {len(top_games)} games")

    # Save results
    logger.info("Step 4: Saving results...")
    output_path = save_ranked_games(top_games, run_id)

    logger.info("=" * 60)
    logger.info("✓ Success!")
    logger.info(f"Total games ranked: {len(top_games)}")
    logger.info(f"Output file: {output_path}")
    logger.info("=" * 60)

    # Output JSON for pipeline
    result = {
        "ranked_items_path": output_path,
        "total_items": len(top_games),
        "run_id": run_id
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()
