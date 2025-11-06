"""Normalize and clean Google Play Store data."""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from dateutil import parser as date_parser

logger = logging.getLogger(__name__)


def normalize_game_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize a single game's data to standard schema.
    
    Args:
        raw_data: Raw data from google-play-scraper
        
    Returns:
        Normalized game data dictionary
    """
    try:
        # Parse release date
        release_date = None
        if raw_data.get('released'):
            try:
                # Try parsing various date formats
                parsed_date = date_parser.parse(raw_data['released'])
                release_date = parsed_date.strftime('%Y-%m-%d')
            except Exception as e:
                logger.warning(f"Failed to parse date '{raw_data.get('released')}': {e}")
        
        # Extract screenshots
        screenshots = []
        if raw_data.get('screenshots'):
            screenshots = raw_data['screenshots']
        
        # Normalize genre
        genre = raw_data.get('genre', 'Unknown')
        if isinstance(genre, list):
            genre = genre[0] if genre else 'Unknown'
        
        # Build normalized data
        normalized = {
            'package_name': raw_data.get('appId', ''),
            'title': raw_data.get('title', ''),
            'developer': raw_data.get('developer', ''),
            'genre': genre,
            'description': raw_data.get('description', ''),
            'rating': float(raw_data.get('score', 0)) if raw_data.get('score') else None,
            'ratings_count': int(raw_data.get('ratings', 0)) if raw_data.get('ratings') else 0,
            'installs': parse_installs(raw_data.get('installs')),
            'release_date': release_date,
            'icon_url': raw_data.get('icon', ''),
            'screenshots': screenshots,
            'store_url': f"https://play.google.com/store/apps/details?id={raw_data.get('appId', '')}",
            # Additional useful fields
            'price': raw_data.get('price', 0),
            'free': raw_data.get('free', True),
            'content_rating': raw_data.get('contentRating', ''),
            'updated': raw_data.get('updated'),
        }
        
        return normalized
        
    except Exception as e:
        logger.error(f"Failed to normalize data for {raw_data.get('appId')}: {e}")
        raise


def parse_installs(installs_str: Optional[str]) -> Optional[int]:
    """
    Parse install count string to integer.
    
    Args:
        installs_str: Install count string (e.g., '10,000+', '1,000,000+')
        
    Returns:
        Integer install count or None
    """
    if not installs_str:
        return None
    
    try:
        # Remove '+' and ',' characters
        clean_str = installs_str.replace('+', '').replace(',', '')
        return int(clean_str)
    except (ValueError, AttributeError):
        logger.warning(f"Failed to parse installs: {installs_str}")
        return None


def deduplicate_games(games: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Remove duplicate games based on package_name.
    
    Args:
        games: List of game dictionaries
        
    Returns:
        Deduplicated list of games
    """
    seen = set()
    unique_games = []
    
    for game in games:
        package_name = game.get('package_name')
        if not package_name:
            logger.warning(f"Game without package_name: {game.get('title')}")
            continue
        
        if package_name not in seen:
            seen.add(package_name)
            unique_games.append(game)
        else:
            logger.debug(f"Duplicate found: {package_name}")
    
    logger.info(f"Deduplication: {len(games)} -> {len(unique_games)} games")
    return unique_games


def filter_games_only(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter to keep only games (remove other apps).
    
    Args:
        items: List of app dictionaries
        
    Returns:
        Filtered list containing only games
    """
    game_genres = [
        'Action', 'Adventure', 'Arcade', 'Board', 'Card', 'Casino',
        'Casual', 'Educational', 'Music', 'Puzzle', 'Racing',
        'Role Playing', 'Simulation', 'Sports', 'Strategy', 'Trivia', 'Word'
    ]
    
    games = []
    for item in items:
        genre = item.get('genre', '')
        # Check if genre contains game-related keywords
        if any(game_genre.lower() in genre.lower() for game_genre in game_genres):
            games.append(item)
        elif 'game' in item.get('title', '').lower():
            # Also include if 'game' is in the title
            games.append(item)
    
    logger.info(f"Filtered to {len(games)} games from {len(items)} items")
    return games

