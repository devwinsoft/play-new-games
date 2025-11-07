#!/usr/bin/env python3
"""
publish_html skill handler
Generate HTML report from ranked games data
"""
import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_ranked_games(ranked_items_path: str) -> List[Dict[str, Any]]:
    """Load ranked game data from JSON file"""
    with open(ranked_items_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_html(games: List[Dict[str, Any]], query: str, country: str) -> str:
    """Generate HTML page from ranked games data"""
    
    # Calculate statistics
    total_games = len(games)
    avg_score = sum(g.get('final_score', 0) for g in games) / total_games if total_games > 0 else 0
    
    # Genre distribution
    genre_counts = {}
    for game in games:
        genre = game.get('genre', 'Unknown')
        genre_counts[genre] = genre_counts.get(genre, 0) + 1
    
    top_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Generate game cards HTML
    game_cards_html = ""
    for game in games:
        rank = game.get('rank', 0)
        title = game.get('title', 'Unknown')
        developer = game.get('developer', 'Unknown')
        genre = game.get('genre', 'Unknown')
        rating = game.get('rating', 0)
        installs = game.get('installs', 0)
        release_date = game.get('release_date', 'Unknown')
        final_score = game.get('final_score', 0)
        
        scores = game.get('scores', {})
        freshness = scores.get('freshness', 0)
        quality = scores.get('quality', 0)
        popularity = scores.get('popularity', 0)
        
        # Format installs
        installs_str = f"{installs:,}" if installs else "N/A"
        
        # Badge color based on rank
        badge_color = "#FFD700" if rank <= 3 else "#C0C0C0" if rank <= 10 else "#CD7F32"
        
        game_cards_html += f'''
        <div class="game-card">
            <div class="rank-badge" style="background: {badge_color}">#{rank}</div>
            <div class="game-info">
                <h3 class="game-title">{title}</h3>
                <p class="game-developer">{developer}</p>
                <div class="game-meta">
                    <span class="badge badge-genre">{genre}</span>
                    <span class="badge badge-rating">⭐ {rating:.1f}</span>
                    <span class="badge badge-installs">📥 {installs_str}</span>
                </div>
                <p class="game-release">출시일: {release_date}</p>
            </div>
            <div class="game-scores">
                <div class="score-main">
                    <div class="score-value">{final_score:.3f}</div>
                    <div class="score-label">최종 점수</div>
                </div>
                <div class="score-breakdown">
                    <div class="score-item">
                        <div class="score-bar">
                            <div class="score-fill" style="width: {quality*100}%; background: #4CAF50"></div>
                        </div>
                        <span>품질 {quality:.2f}</span>
                    </div>
                    <div class="score-item">
                        <div class="score-bar">
                            <div class="score-fill" style="width: {freshness*100}%; background: #2196F3"></div>
                        </div>
                        <span>신규성 {freshness:.2f}</span>
                    </div>
                    <div class="score-item">
                        <div class="score-bar">
                            <div class="score-fill" style="width: {popularity*100}%; background: #FF9800"></div>
                        </div>
                        <span>인기도 {popularity:.2f}</span>
                    </div>
                </div>
            </div>
        </div>
        '''
    
    # Generate genre chart data
    genre_chart_labels = json.dumps([g[0] for g in top_genres])
    genre_chart_data = json.dumps([g[1] for g in top_genres])
    
    # Generate HTML
    html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>게임 랭킹 리포트 - {query} ({country})</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            color: #667eea;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            color: #666;
            font-size: 1.2em;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 3em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 1em;
        }}
        
        .content {{
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }}
        
        .section-title {{
            font-size: 2em;
            color: #333;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 3px solid #667eea;
        }}
        
        .game-card {{
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            display: grid;
            grid-template-columns: auto 1fr auto;
            gap: 25px;
            align-items: center;
            transition: transform 0.2s, box-shadow 0.2s;
            position: relative;
        }}
        
        .game-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }}
        
        .rank-badge {{
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5em;
            font-weight: bold;
            color: white;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        
        .game-info {{
            flex: 1;
        }}
        
        .game-title {{
            font-size: 1.5em;
            color: #333;
            margin-bottom: 5px;
        }}
        
        .game-developer {{
            color: #666;
            margin-bottom: 10px;
        }}
        
        .game-meta {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 10px;
        }}
        
        .badge {{
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 500;
        }}
        
        .badge-genre {{
            background: #e3f2fd;
            color: #1976d2;
        }}
        
        .badge-rating {{
            background: #fff3e0;
            color: #f57c00;
        }}
        
        .badge-installs {{
            background: #f3e5f5;
            color: #7b1fa2;
        }}
        
        .game-release {{
            color: #999;
            font-size: 0.9em;
        }}
        
        .game-scores {{
            min-width: 250px;
        }}
        
        .score-main {{
            text-align: center;
            margin-bottom: 15px;
        }}
        
        .score-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .score-label {{
            color: #666;
            font-size: 0.9em;
        }}
        
        .score-breakdown {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        
        .score-item {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .score-bar {{
            flex: 1;
            height: 20px;
            background: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
        }}
        
        .score-fill {{
            height: 100%;
            transition: width 0.3s ease;
        }}
        
        .score-item span {{
            min-width: 100px;
            font-size: 0.85em;
            color: #666;
        }}
        
        .chart-container {{
            margin-top: 40px;
            padding: 30px;
            background: #f8f9fa;
            border-radius: 15px;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 30px;
            background: white;
            border-radius: 15px;
            color: #666;
        }}
        
        @media (max-width: 768px) {{
            .game-card {{
                grid-template-columns: 1fr;
                text-align: center;
            }}
            
            .game-scores {{
                width: 100%;
            }}
            
            .header h1 {{
                font-size: 1.8em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎮 게임 랭킹 리포트</h1>
            <p class="subtitle">{query} · {country} · {datetime.now().strftime('%Y-%m-%d')}</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{total_games}</div>
                <div class="stat-label">총 게임 수</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{avg_score:.3f}</div>
                <div class="stat-label">평균 점수</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(genre_counts)}</div>
                <div class="stat-label">장르 수</div>
            </div>
        </div>
        
        <div class="content">
            <h2 class="section-title">🏆 상위 랭킹 게임</h2>
            {game_cards_html}
            
            <div class="chart-container">
                <h3 style="margin-bottom: 20px; color: #333;">📊 장르 분포 (상위 5개)</h3>
                <canvas id="genreChart" width="400" height="200"></canvas>
            </div>
        </div>
        
        <div class="footer">
            <p>Generated by play-new-games pipeline</p>
            <p style="margin-top: 10px; font-size: 0.9em;">
                품질 45% · 신규성 35% · 인기도 20%
            </p>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    <script>
        const ctx = document.getElementById('genreChart').getContext('2d');
        new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: {genre_chart_labels},
                datasets: [{{
                    label: '게임 수',
                    data: {genre_chart_data},
                    backgroundColor: [
                        'rgba(102, 126, 234, 0.8)',
                        'rgba(118, 75, 162, 0.8)',
                        'rgba(76, 175, 80, 0.8)',
                        'rgba(255, 152, 0, 0.8)',
                        'rgba(33, 150, 243, 0.8)'
                    ],
                    borderColor: [
                        'rgba(102, 126, 234, 1)',
                        'rgba(118, 75, 162, 1)',
                        'rgba(76, 175, 80, 1)',
                        'rgba(255, 152, 0, 1)',
                        'rgba(33, 150, 243, 1)'
                    ],
                    borderWidth: 2,
                    borderRadius: 10
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            stepSize: 1
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>'''
    
    return html


def save_html(html: str, run_id: str) -> str:
    """Save HTML to file"""
    # Create output directory
    date_str = datetime.now().strftime('%Y%m%d')
    output_dir = Path('outputs') / date_str / run_id / 'reports'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save HTML file
    output_path = output_dir / 'game_ranking.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return str(output_path.absolute())


def main():
    logger.info("=" * 60)
    logger.info("publish_html - Game Ranking HTML Report Generator")
    logger.info("=" * 60)
    
    # Get environment variables
    ranked_items_path = os.getenv('RANKED_ITEMS_PATH')
    if not ranked_items_path:
        logger.error("RANKED_ITEMS_PATH environment variable is required")
        sys.exit(1)
    
    query = os.getenv('QUERY', 'new games')
    country = os.getenv('COUNTRY', 'KR')
    run_id = os.getenv('RUN_ID', datetime.now().strftime("%H%M%S"))
    
    logger.info(f"Ranked items path: {ranked_items_path}")
    logger.info(f"Query: {query}")
    logger.info(f"Country: {country}")
    logger.info(f"Run ID: {run_id}")
    logger.info("=" * 60)
    
    # Load ranked games
    logger.info("Step 1: Loading ranked games...")
    games = load_ranked_games(ranked_items_path)
    logger.info(f"Loaded {len(games)} games")
    
    # Generate HTML
    logger.info("Step 2: Generating HTML...")
    html = generate_html(games, query, country)
    logger.info("HTML generated successfully")
    
    # Save HTML
    logger.info("Step 3: Saving HTML file...")
    output_path = save_html(html, run_id)
    
    logger.info("=" * 60)
    logger.info("✓ Success!")
    logger.info(f"HTML report: {output_path}")
    logger.info("=" * 60)
    
    # Output JSON for pipeline
    result = {
        "html_report_path": output_path,
        "total_games": len(games),
        "run_id": run_id
    }
    print(json.dumps(result))
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

