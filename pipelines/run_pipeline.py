#!/usr/bin/env python3
"""
Game Data Pipeline Runner
Integrates ingest_play → ranker → publish_html
"""
import os
import sys
import json
import subprocess
import argparse
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(message: str):
    """Print colored header"""
    print(f"\n{Colors.OKCYAN}{'='*60}")
    print(f"{message}")
    print(f"{'='*60}{Colors.ENDC}\n")


def print_success(message: str):
    """Print success message"""
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")


def print_error(message: str):
    """Print error message"""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")


def print_info(message: str):
    """Print info message"""
    print(f"{Colors.WARNING}ℹ {message}{Colors.ENDC}")


def run_skill(skill_name: str, env_vars: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """
    Run a skill and return its JSON output
    
    Args:
        skill_name: Name of the skill (e.g., 'ingest_play')
        env_vars: Environment variables to set
        
    Returns:
        Dictionary of JSON output or None if failed
    """
    skill_path = Path(f"skills/{skill_name}/handler.py")
    if not skill_path.exists():
        # Try scorer.py for ranker
        skill_path = Path(f"skills/{skill_name}/scorer.py")
        if not skill_path.exists():
            print_error(f"Skill not found: {skill_name}")
            return None
    
    # Prepare environment
    env = os.environ.copy()
    env.update(env_vars)
    
    # Run skill
    try:
        result = subprocess.run(
            [sys.executable, str(skill_path)],
            env=env,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print_error(f"Skill {skill_name} failed")
            print(result.stderr)
            return None
        
        # Extract JSON from output (last line)
        output_lines = result.stdout.strip().split('\n')
        for line in reversed(output_lines):
            line = line.strip()
            if line.startswith('{') and line.endswith('}'):
                try:
                    return json.loads(line)
                except json.JSONDecodeError:
                    continue
        
        print_error(f"No valid JSON output from {skill_name}")
        return None
        
    except Exception as e:
        print_error(f"Failed to run {skill_name}: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description='Game Data Pipeline - Collect, Rank, and Report',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage (Korean new games, top 50)
  %(prog)s
  
  # Puzzle games, top 30
  %(prog)s --query puzzle --top-k 30
  
  # US action games, top 20, with HTML report
  %(prog)s --query action --country US --top-k 20 --html
  
  # Fast test (10 games only)
  %(prog)s --limit 10 --top-k 5 --html
        """
    )
    
    # Pipeline parameters
    parser.add_argument(
        '--query', '-q',
        default='new games',
        help='Search query (default: "new games")'
    )
    parser.add_argument(
        '--country', '-c',
        default='KR',
        help='Country code (default: "KR")'
    )
    parser.add_argument(
        '--language', '-l',
        default='ko',
        help='Language code (default: "ko")'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=120,
        help='Number of games to collect (default: 120)'
    )
    parser.add_argument(
        '--top-k', '-k',
        type=int,
        default=50,
        help='Number of top games to select (default: 50)'
    )
    
    # HTML report
    parser.add_argument(
        '--html',
        action='store_true',
        help='Generate HTML report after ranking'
    )
    parser.add_argument(
        '--open-browser',
        action='store_true',
        help='Open HTML report in browser (requires --html)'
    )
    
    # Output
    parser.add_argument(
        '--run-id',
        help='Custom run ID (default: HHMMSS)'
    )
    parser.add_argument(
        '--log-level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Logging level (default: INFO)'
    )
    
    args = parser.parse_args()
    
    # Set log level
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    # Generate run ID
    run_id = args.run_id or datetime.now().strftime("%H%M%S")
    
    # Print header
    print_header("🎮 Game Data Pipeline")
    print(f"Query:    {args.query}")
    print(f"Country:  {args.country}")
    print(f"Language: {args.language}")
    print(f"Limit:    {args.limit}")
    print(f"Top-K:    {args.top_k}")
    print(f"Run ID:   {run_id}")
    if args.html:
        print(f"HTML:     Enabled")
    print()
    
    start_time = datetime.now()
    
    # ========================================
    # Step 1: Collect games (ingest_play)
    # ========================================
    print_header("Step 1: Collecting games (ingest_play)")
    
    step1_env = {
        'QUERY': args.query,
        'COUNTRY': args.country,
        'LANGUAGE': args.language,
        'LIMIT': str(args.limit),
        'RUN_ID': run_id,
        'LOG_LEVEL': args.log_level
    }
    
    step1_start = datetime.now()
    result1 = run_skill('ingest_play', step1_env)
    
    if not result1:
        print_error("Step 1 failed")
        return 1
    
    raw_items_path = result1.get('raw_items_path')
    raw_count = result1.get('total_items', 0)
    
    step1_duration = datetime.now() - step1_start
    print_success(f"Collected {raw_count} games")
    print(f"   Output: {raw_items_path}")
    print(f"   Duration: {step1_duration.seconds}s")
    
    if raw_count == 0:
        print_error("No games collected. Try different query or country.")
        return 1
    
    # ========================================
    # Step 2: Rank games (ranker)
    # ========================================
    print_header("Step 2: Ranking games (ranker)")
    
    step2_env = {
        'RAW_ITEMS_PATH': raw_items_path,
        'TOP_K': str(args.top_k),
        'RUN_ID': run_id,
        'LOG_LEVEL': args.log_level
    }
    
    step2_start = datetime.now()
    result2 = run_skill('ranker', step2_env)
    
    if not result2:
        print_error("Step 2 failed")
        print_info(f"Raw data preserved: {raw_items_path}")
        return 1
    
    ranked_items_path = result2.get('ranked_items_path')
    ranked_count = result2.get('total_items', 0)
    
    step2_duration = datetime.now() - step2_start
    print_success(f"Ranked top {ranked_count} games")
    print(f"   Output: {ranked_items_path}")
    print(f"   Duration: {step2_duration.seconds}s")
    
    # ========================================
    # Step 3: Generate HTML report (optional)
    # ========================================
    html_report_path = None
    
    if args.html:
        print_header("Step 3: Generating HTML report (publish_html)")
        
        step3_env = {
            'RANKED_ITEMS_PATH': ranked_items_path,
            'QUERY': args.query,
            'COUNTRY': args.country,
            'RUN_ID': run_id,
            'LOG_LEVEL': args.log_level
        }
        
        step3_start = datetime.now()
        result3 = run_skill('publish_html', step3_env)
        
        if not result3:
            print_error("Step 3 failed")
            print_info("Ranking data still available")
        else:
            html_report_path = result3.get('html_report_path')
            
            step3_duration = datetime.now() - step3_start
            print_success("HTML report generated")
            print(f"   Output: {html_report_path}")
            print(f"   Duration: {step3_duration.seconds}s")
            
            # Open in browser
            if args.open_browser:
                try:
                    import webbrowser
                    webbrowser.open(f'file://{os.path.abspath(html_report_path)}')
                    print_success("Opened in browser")
                except Exception as e:
                    print_error(f"Failed to open browser: {e}")
    
    # ========================================
    # Summary
    # ========================================
    total_duration = datetime.now() - start_time
    
    print_header("📊 Pipeline Summary")
    print(f"Total duration: {total_duration.seconds}s")
    print()
    print("Step results:")
    print(f"  ✓ Collected: {raw_count} games")
    print(f"  ✓ Ranked:    {ranked_count} games")
    if html_report_path:
        print(f"  ✓ HTML:      Generated")
    print()
    
    print(f"{Colors.BOLD}📁 Output files:{Colors.ENDC}")
    print(f"  Raw data:  {raw_items_path}")
    print(f"  Rankings:  {ranked_items_path}")
    if html_report_path:
        print(f"  HTML:      {html_report_path}")
    print()
    
    # Load and display top 5 games
    try:
        with open(ranked_items_path, 'r', encoding='utf-8') as f:
            games = json.load(f)
        
        print(f"{Colors.BOLD}🏆 Top 5 Games:{Colors.ENDC}")
        for game in games[:5]:
            rank = game.get('rank', '?')
            title = game.get('title', 'Unknown')
            score = game.get('final_score', 0)
            genre = game.get('genre', 'Unknown')
            print(f"  {rank}. [{score:.3f}] {title} ({genre})")
        print()
    except Exception as e:
        logger.warning(f"Could not display top games: {e}")
    
    # Next steps
    print(f"{Colors.BOLD}💡 Next steps:{Colors.ENDC}")
    if not args.html:
        print(f"  Generate HTML: python scripts/run_pipeline.py --query \"{args.query}\" --html")
    if html_report_path and not args.open_browser:
        print(f"  Open HTML:     xdg-open {html_report_path}")
    print(f"  View JSON:     cat {ranked_items_path}")
    print(f"  Try query:     python scripts/run_pipeline.py --query puzzle --top-k 30")
    print()
    
    print_header("🎉 Pipeline completed successfully!")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n")
        print_error("Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

