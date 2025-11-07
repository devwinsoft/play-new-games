#!/usr/bin/env python3
"""
Code Changelog 예제
멀티 에이전트 환경에서 자동 로깅 데모
"""
import sys
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from modules.code_changelog_tracker import CodeChangeLogger


def example_1_basic_logging():
    """예제 1: 기본 로깅"""
    print("\n" + "="*60)
    print("예제 1: 기본 로깅")
    print("="*60)
    
    logger = CodeChangeLogger(
        project_name="Example 1 - Basic Logging",
        user_request="Test basic changelog functionality"
    )
    
    # 파일 생성 기록
    logger.log_file_creation(
        file_path="examples/test_file.py",
        content="print('Hello, World!')",
        reason="Create test file for demonstration"
    )
    
    # 저장
    logger.save_and_build()
    
    print("✓ 변경 이력 저장 완료!")
    print(f"  파일: reviews/{logger.timestamp}.md")


def example_2_pipeline_simulation():
    """예제 2: 파이프라인 시뮬레이션"""
    print("\n" + "="*60)
    print("예제 2: 파이프라인 시뮬레이션 (3단계)")
    print("="*60)
    
    logger = CodeChangeLogger(
        project_name="Game Pipeline Simulation",
        user_request="Simulate 3-step pipeline: collect → rank → html"
    )
    
    # Step 1: Data Collection
    print("\n[Step 1] 데이터 수집...")
    logger.log_file_creation(
        file_path="outputs/20251107/103252/artifacts/raw_games.json",
        content="[87 games collected from Google Play]",
        reason="Collect 'new games' from KR Google Play Store"
    )
    
    # Step 2: Ranking
    print("[Step 2] 랭킹 계산...")
    logger.log_file_creation(
        file_path="outputs/20251107/103252/artifacts/ranked_games.json",
        content="[Top 50 games selected based on freshness, quality, popularity]",
        reason="Calculate scores and rank games"
    )
    
    # Step 3: HTML Report
    print("[Step 3] HTML 리포트 생성...")
    logger.log_file_creation(
        file_path="outputs/20251107/103252/reports/game_ranking.html",
        content="[HTML report with 50 game cards]",
        reason="Generate visual report for browser viewing"
    )
    
    # 저장
    logger.save_and_build()
    
    print("\n✓ 전체 파이프라인 로깅 완료!")
    print(f"  파일: reviews/{logger.timestamp}.md")


def example_3_file_modification():
    """예제 3: 파일 수정 추적"""
    print("\n" + "="*60)
    print("예제 3: 파일 수정 추적")
    print("="*60)
    
    logger = CodeChangeLogger(
        project_name="Bug Fix - Ranking Algorithm",
        user_request="Fix diversity scoring calculation"
    )
    
    old_code = """
def calculate_diversity_score(games):
    # Bug: incorrect diversity calculation
    return sum([g.genre for g in games])
    """.strip()
    
    new_code = """
def calculate_diversity_score(games):
    # Fixed: use set for unique genres
    unique_genres = set(g.genre for g in games)
    return len(unique_genres) / len(games)
    """.strip()
    
    logger.log_file_modification(
        file_path="skills/ranker/scorer.py",
        old_content=old_code,
        new_content=new_code,
        reason="Fix diversity score calculation to count unique genres"
    )
    
    # 저장
    logger.save_and_build()
    
    print("✓ 파일 수정 이력 저장 완료!")
    print(f"  파일: reviews/{logger.timestamp}.md")


def example_4_bug_fix():
    """예제 4: 버그 수정 추적"""
    print("\n" + "="*60)
    print("예제 4: 버그 수정 추적")
    print("="*60)
    
    logger = CodeChangeLogger(
        project_name="Bug Fix - Data Normalization",
        user_request="Fix rating score normalization"
    )
    
    logger.log_bug_fix(
        file_path="skills/ingest_play/normalize.py",
        old_content="score = rating * 0.1",
        new_content="score = rating / 5.0",
        bug_desc="Rating score was incorrectly scaled (0-5 → 0-0.5 instead of 0-1)",
        fix_desc="Changed formula to normalize rating to 0-1 range correctly"
    )
    
    # 저장
    logger.save_and_build()
    
    print("✓ 버그 수정 이력 저장 완료!")
    print(f"  파일: reviews/{logger.timestamp}.md")


def example_5_multi_agent():
    """예제 5: 멀티 에이전트 시뮬레이션"""
    print("\n" + "="*60)
    print("예제 5: 멀티 에이전트 시뮬레이션")
    print("="*60)
    
    # Agent 1: ingest_play
    print("\n[Agent 1: ingest_play] 실행...")
    logger1 = CodeChangeLogger(
        project_name="Agent 1 - Data Collection",
        user_request="Collect games from Google Play"
    )
    logger1.log_file_creation(
        file_path="outputs/20251107/agent1/raw_games.json",
        content="87 games collected",
        reason="Data collection by ingest_play agent"
    )
    logger1.save_and_build()
    print(f"  → reviews/{logger1.timestamp}.md")
    
    # Agent 2: ranker
    print("[Agent 2: ranker] 실행...")
    logger2 = CodeChangeLogger(
        project_name="Agent 2 - Game Ranking",
        user_request="Rank collected games"
    )
    logger2.log_file_creation(
        file_path="outputs/20251107/agent2/ranked_games.json",
        content="Top 50 games selected",
        reason="Ranking by ranker agent"
    )
    logger2.save_and_build()
    print(f"  → reviews/{logger2.timestamp}.md")
    
    # Agent 3: publish_html
    print("[Agent 3: publish_html] 실행...")
    logger3 = CodeChangeLogger(
        project_name="Agent 3 - HTML Report",
        user_request="Generate HTML report"
    )
    logger3.log_file_creation(
        file_path="outputs/20251107/agent3/game_ranking.html",
        content="HTML report generated",
        reason="Report generation by publish_html agent"
    )
    logger3.save_and_build()
    print(f"  → reviews/{logger3.timestamp}.md")
    
    print("\n✓ 3개 에이전트의 변경사항이 각각 기록되었습니다!")


def main():
    """메인 함수"""
    import sys
    import io
    
    # Windows 콘솔 인코딩 문제 해결
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("\n" + "🎮 Code Changelog 예제 모음")
    print("="*60)
    
    examples = [
        ("1", "기본 로깅", example_1_basic_logging),
        ("2", "파이프라인 시뮬레이션", example_2_pipeline_simulation),
        ("3", "파일 수정 추적", example_3_file_modification),
        ("4", "버그 수정 추적", example_4_bug_fix),
        ("5", "멀티 에이전트 시뮬레이션", example_5_multi_agent),
    ]
    
    print("\n실행할 예제를 선택하세요:")
    for num, desc, _ in examples:
        print(f"  {num}. {desc}")
    print("  0. 모든 예제 실행")
    print()
    
    try:
        choice = input("선택 (0-5): ").strip()
        
        if choice == "0":
            # 모든 예제 실행
            for num, desc, func in examples:
                func()
        elif choice in ["1", "2", "3", "4", "5"]:
            # 선택한 예제만 실행
            for num, desc, func in examples:
                if num == choice:
                    func()
                    break
        else:
            print("❌ 잘못된 선택입니다.")
            return
        
        # 완료 메시지
        print("\n" + "="*60)
        print("🎉 예제 실행 완료!")
        print("="*60)
        print("\n📋 생성된 문서 확인:")
        print("  1. cd reviews")
        print("  2. python3 -m http.server 4000")
        print("  3. 브라우저에서 http://localhost:4000 열기")
        print()
        
        # 자동으로 서버 실행 여부 확인
        run_server = input("지금 문서 서버를 실행하시겠습니까? (y/n): ").strip().lower()
        if run_server == 'y':
            import subprocess
            print("\n🌐 문서 서버 실행 중...")
            print("   URL: http://localhost:4000")
            print("   종료: Ctrl+C\n")
            
            reviews_dir = project_root / "reviews"
            subprocess.run(
                ["python3", "-m", "http.server", "4000"],
                cwd=reviews_dir
            )
    
    except KeyboardInterrupt:
        print("\n\n✓ 종료")
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")


if __name__ == "__main__":
    main()

