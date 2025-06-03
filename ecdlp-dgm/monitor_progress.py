#!/usr/bin/env python3
"""Real-time monitoring of research progress."""
import time
import json
from pathlib import Path
from datetime import datetime
import os

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def monitor():
    """Monitor research progress in real-time."""
    while True:
        clear_screen()
        
        print("""
╔════════════════════════════════════════════╗
║       ECDLP Research Monitor               ║
╚════════════════════════════════════════════╝
        """)
        
        # Check latest checkpoint
        checkpoint_dir = Path('./checkpoints')
        if checkpoint_dir.exists():
            progress_file = checkpoint_dir / 'progress.json'
            if progress_file.exists():
                with open(progress_file) as f:
                    progress = json.load(f)
                
                print(f"📊 Progress Statistics:")
                print(f"   Total Discoveries: {progress.get('total_discoveries', 0)}")
                print(f"   Verified: {progress.get('verified_discoveries', 0)}")
                print(f"   Major Breakthroughs: {len(progress.get('major_breakthroughs', []))}")
                
                # Show recent breakthroughs
                breakthroughs = progress.get('major_breakthroughs', [])
                if breakthroughs:
                    print(f"\n🌟 Recent Breakthroughs:")
                    for bt in breakthroughs[-3:]:
                        print(f"   - {bt['summary']}")
        
        # Check latest research history
        histories = sorted(Path('.').glob('research_history_*.md'))
        if histories:
            latest = histories[-1]
            print(f"\n📝 Latest Activity: {latest.name}")
            print(f"   Modified: {datetime.fromtimestamp(latest.stat().st_mtime)}")
            
            # Show last few lines
            with open(latest) as f:
                lines = f.readlines()
                if len(lines) > 5:
                    print("\n   Last entries:")
                    for line in lines[-5:]:
                        print(f"   {line.strip()[:60]}...")
        
        print(f"\n🕐 Updated: {datetime.now().strftime('%H:%M:%S')}")
        print("Press Ctrl+C to exit")
        
        time.sleep(5)  # Update every 5 seconds

if __name__ == "__main__":
    try:
        monitor()
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")