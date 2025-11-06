"""Google Play Store adapter using google-play-scraper."""
import logging
from typing import List, Dict, Any, Optional
from google_play_scraper import search, app

logger = logging.getLogger(__name__)


class PlayStoreAdapter:
    """Adapter for fetching game data from Google Play Store."""
    
    def __init__(self, country: str = "KR", language: str = "ko"):
        """
        Initialize PlayStoreAdapter.
        
        Args:
            country: Country code (e.g., 'KR', 'US')
            language: Language code (e.g., 'ko', 'en')
        """
        self.country = country
        self.language = language
    
    def search_games(self, query: str, limit: int = 120) -> List[Dict[str, Any]]:
        """
        Search for games on Google Play Store.
        
        Args:
            query: Search query (e.g., 'new games')
            limit: Maximum number of results to fetch
            
        Returns:
            List of game metadata dictionaries
        """
        logger.info(f"Searching for '{query}' in {self.country}/{self.language}, limit={limit}")
        
        try:
            # Search for apps
            results = search(
                query,
                lang=self.language,
                country=self.country,
                n_hits=min(limit, 250)  # API limit
            )
            
            logger.info(f"Found {len(results)} results")
            
            # Fetch detailed information for each app
            detailed_results = []
            for idx, result in enumerate(results[:limit]):
                try:
                    app_id = result.get('appId')
                    if not app_id:
                        logger.warning(f"Skipping result {idx}: no appId")
                        continue
                    
                    logger.debug(f"Fetching details for {app_id} ({idx+1}/{len(results)})")
                    details = app(
                        app_id,
                        lang=self.language,
                        country=self.country
                    )
                    detailed_results.append(details)
                    
                except Exception as e:
                    logger.warning(f"Failed to fetch details for {result.get('appId')}: {e}")
                    continue
            
            logger.info(f"Successfully fetched {len(detailed_results)} detailed results")
            return detailed_results
            
        except Exception as e:
            logger.error(f"Failed to search games: {e}")
            raise
    
    def get_app_details(self, app_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information for a specific app.
        
        Args:
            app_id: Package name (e.g., 'com.example.game')
            
        Returns:
            App metadata dictionary or None if failed
        """
        try:
            return app(app_id, lang=self.language, country=self.country)
        except Exception as e:
            logger.error(f"Failed to fetch app details for {app_id}: {e}")
            return None

