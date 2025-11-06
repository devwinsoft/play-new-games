"""Tests for normalize module."""
import unittest
from skills.ingest_play.normalize import (
    normalize_game_data,
    parse_installs,
    deduplicate_games,
    filter_games_only
)


class TestParseInstalls(unittest.TestCase):
    """Test parse_installs function."""
    
    def test_parse_installs_basic(self):
        """Test basic install count parsing."""
        self.assertEqual(parse_installs("10,000+"), 10000)
        self.assertEqual(parse_installs("1,000,000+"), 1000000)
        self.assertEqual(parse_installs("500+"), 500)
    
    def test_parse_installs_none(self):
        """Test None input."""
        self.assertIsNone(parse_installs(None))
    
    def test_parse_installs_empty(self):
        """Test empty string."""
        self.assertIsNone(parse_installs(""))


class TestNormalizeGameData(unittest.TestCase):
    """Test normalize_game_data function."""
    
    def test_normalize_basic(self):
        """Test basic normalization."""
        raw_data = {
            'appId': 'com.example.game',
            'title': 'Test Game',
            'developer': 'Test Studio',
            'genre': 'Action',
            'description': 'A test game',
            'score': 4.5,
            'ratings': 1000,
            'installs': '10,000+',
            'icon': 'https://example.com/icon.png',
            'screenshots': ['https://example.com/1.png'],
            'free': True,
            'price': 0
        }
        
        result = normalize_game_data(raw_data)
        
        self.assertEqual(result['package_name'], 'com.example.game')
        self.assertEqual(result['title'], 'Test Game')
        self.assertEqual(result['developer'], 'Test Studio')
        self.assertEqual(result['genre'], 'Action')
        self.assertEqual(result['rating'], 4.5)
        self.assertEqual(result['ratings_count'], 1000)
        self.assertEqual(result['installs'], 10000)
        self.assertTrue('store_url' in result)


class TestDeduplicateGames(unittest.TestCase):
    """Test deduplicate_games function."""
    
    def test_deduplicate_basic(self):
        """Test basic deduplication."""
        games = [
            {'package_name': 'com.game1', 'title': 'Game 1'},
            {'package_name': 'com.game2', 'title': 'Game 2'},
            {'package_name': 'com.game1', 'title': 'Game 1 Duplicate'},
        ]
        
        result = deduplicate_games(games)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['package_name'], 'com.game1')
        self.assertEqual(result[1]['package_name'], 'com.game2')


class TestFilterGamesOnly(unittest.TestCase):
    """Test filter_games_only function."""
    
    def test_filter_games(self):
        """Test filtering games."""
        items = [
            {'package_name': 'com.game1', 'title': 'Action Game', 'genre': 'Action'},
            {'package_name': 'com.app1', 'title': 'Calculator', 'genre': 'Tools'},
            {'package_name': 'com.game2', 'title': 'Puzzle Game', 'genre': 'Puzzle'},
        ]
        
        result = filter_games_only(items)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['genre'], 'Action')
        self.assertEqual(result[1]['genre'], 'Puzzle')


if __name__ == '__main__':
    unittest.main()

