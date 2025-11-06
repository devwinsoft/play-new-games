"""
ingest_play handler - Fetch new game metadata from Google Play Store.

Entry point for the ingest_play skill.
"""
import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from skills.ingest_play.adapters.play_store import PlayStoreAdapter
from skills.ingest_play.normalize import (
    normalize_game_data,
    deduplicate_games,
    filter_games_only
)


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
    return logging.getLogger(__name__)


def get_output_path(run_id: str = None) -> Path:
    """
    Get output path for artifacts.
    
    Args:
        run_id: Unique run identifier
        
    Returns:
        Path object for output directory
    """
    if not run_id:
        run_id = datetime.now().strftime('%H%M%S')
    
    date_str = datetime.now().strftime('%Y%m%d')
    output_dir = project_root / 'outputs' / date_str / run_id / 'artifacts'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    return output_dir


def save_results(data: list, output_path: Path, filename: str = "raw_games.json") -> Path:
    """
    Save results to JSON file.
    
    Args:
        data: List of game dictionaries
        output_path: Output directory path
        filename: Output filename
        
    Returns:
        Path to saved file
    """
    output_file = output_path / filename
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return output_file


def main():
    """Main execution function."""
    # Get configuration from environment
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    logger = setup_logging(log_level)
    
    # Get parameters from environment or use defaults
    query = os.getenv('QUERY', 'new games')
    country = os.getenv('COUNTRY', 'KR')
    language = os.getenv('LANGUAGE', 'ko')
    limit = int(os.getenv('LIMIT', '120'))
    run_id = os.getenv('RUN_ID', datetime.now().strftime('%H%M%S'))
    
    logger.info("=" * 60)
    logger.info("ingest_play - Google Play Game Metadata Collector")
    logger.info("=" * 60)
    logger.info(f"Query: {query}")
    logger.info(f"Country: {country}")
    logger.info(f"Language: {language}")
    logger.info(f"Limit: {limit}")
    logger.info(f"Run ID: {run_id}")
    logger.info("=" * 60)
    
    try:
        # Step 1: Fetch data from Google Play Store
        logger.info("Step 1: Fetching data from Google Play Store...")
        adapter = PlayStoreAdapter(country=country, language=language)
        raw_data = adapter.search_games(query=query, limit=limit)
        logger.info(f"Fetched {len(raw_data)} items")
        
        # Step 2: Normalize data
        logger.info("Step 2: Normalizing data...")
        normalized_data = []
        for item in raw_data:
            try:
                normalized = normalize_game_data(item)
                normalized_data.append(normalized)
            except Exception as e:
                logger.warning(f"Failed to normalize item: {e}")
                continue
        logger.info(f"Normalized {len(normalized_data)} items")
        
        # Step 3: Filter to keep only games
        logger.info("Step 3: Filtering games...")
        games_only = filter_games_only(normalized_data)
        
        # Step 4: Remove duplicates
        logger.info("Step 4: Removing duplicates...")
        unique_games = deduplicate_games(games_only)
        
        # Step 5: Save results
        logger.info("Step 5: Saving results...")
        output_dir = get_output_path(run_id)
        output_file = save_results(unique_games, output_dir)
        
        logger.info("=" * 60)
        logger.info("✓ Success!")
        logger.info(f"Total games collected: {len(unique_games)}")
        logger.info(f"Output file: {output_file}")
        logger.info("=" * 60)
        
        # Output for pipeline integration
        print(json.dumps({
            'raw_items_path': str(output_file),
            'total_items': len(unique_games),
            'run_id': run_id
        }))
        
        return 0
        
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

