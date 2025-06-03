#!/usr/bin/env python3
"""
Main script to run ECDLP research without Docker.
"""
import os
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime
import subprocess
from tqdm import tqdm

# Set up environment
os.environ['DEEPSEEK_API_KEY'] = 'sk-6c2c1ed44aa94d1a9147547b21e4340c'

def check_dependencies():
    """Check if all dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    # Check Python packages
    required_packages = ['transformers', 'torch', 'requests', 'tqdm', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} missing")
    
    # Check SageMath
    try:
        result = subprocess.run(['sage', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ SageMath installed: {result.stdout.strip()}")
        else:
            print("❌ SageMath not found")
            missing_packages.append('sagemath')
    except FileNotFoundError:
        print("❌ SageMath not found")
        missing_packages.append('sagemath')
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install " + ' '.join(p for p in missing_packages if p != 'sagemath'))
        if 'sagemath' in missing_packages:
            print("Install SageMath: sudo apt install sagemath")
        return False
    
    return True

def run_research_session(duration_hours=1, checkpoint_interval=300):
    """Run a research session with progress tracking."""
    print("\n🚀 Starting ECDLP Research Session")
    print(f"⏱️  Duration: {duration_hours} hours")
    print(f"💾 Checkpoint interval: {checkpoint_interval} seconds")
    
    start_time = time.time()
    end_time = start_time + (duration_hours * 3600)
    
    # Progress bar for overall session
    with tqdm(total=100, desc="Research Progress", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]') as pbar:
        
        iteration = 0
        while time.time() < end_time:
            iteration += 1
            
            # Update progress
            elapsed = time.time() - start_time
            progress = (elapsed / (duration_hours * 3600)) * 100
            pbar.update(progress - pbar.n)
            
            print(f"\n\n{'='*60}")
            print(f"🔬 Research Iteration {iteration}")
            print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*60}")
            
            # Run the mathematical agent
            cmd = [
                sys.executable, 'math_agent.py',
                '--problem_statement', 'Find a polynomial-time algorithm for ECDLP on secp256k1',
                '--workspace_dir', './workspace',
                '--research_history_file', f'./research_history_{iteration}.md',
                '--checkpoint_dir', './checkpoints'
            ]
            
            print(f"🧮 Running: {' '.join(cmd)}")
            
            try:
                result = subprocess.run(cmd, 
                                      capture_output=False,  # Show output in real-time
                                      text=True)
                
                if result.returncode == 0:
                    print("\n✅ Iteration completed successfully")
                else:
                    print(f"\n⚠️  Iteration failed with code {result.returncode}")
                    
            except Exception as e:
                print(f"\n❌ Error in iteration: {e}")
            
            # Checkpoint
            if iteration % 5 == 0:
                print("\n💾 Creating checkpoint...")
                checkpoint_path = Path(f"./checkpoints/checkpoint_{iteration}")
                checkpoint_path.mkdir(exist_ok=True)
                
                # Copy research history
                for hist_file in Path('.').glob('research_history_*.md'):
                    subprocess.run(['cp', str(hist_file), str(checkpoint_path)])
                
                print(f"✅ Checkpoint saved to {checkpoint_path}")
            
            # Wait before next iteration
            print(f"\n⏳ Waiting {checkpoint_interval} seconds before next iteration...")
            time.sleep(checkpoint_interval)
    
    print("\n\n🎉 Research session complete!")
    generate_final_report()

def generate_final_report():
    """Generate a final research report."""
    print("\n📝 Generating final report...")
    
    # Collect all research histories
    histories = sorted(Path('.').glob('research_history_*.md'))
    
    report_path = Path('./final_report.md')
    with open(report_path, 'w') as report:
        report.write("# ECDLP Research Report\n\n")
        report.write(f"Generated: {datetime.now()}\n\n")
        
        # Summary from checkpoints
        checkpoint_dir = Path('./checkpoints')
        if checkpoint_dir.exists():
            progress_file = checkpoint_dir / 'final_progress.json'
            if progress_file.exists():
                import json
                with open(progress_file) as f:
                    progress = json.load(f)
                
                report.write("## Summary\n\n")
                report.write(f"- Total discoveries: {progress.get('total_discoveries', 0)}\n")
                report.write(f"- Verified discoveries: {progress.get('verified_discoveries', 0)}\n")
                report.write(f"- Major breakthroughs: {len(progress.get('major_breakthroughs', []))}\n\n")
        
        # Append all research histories
        report.write("## Detailed Research Log\n\n")
        for i, hist_file in enumerate(histories):
            report.write(f"\n### Iteration {i+1}\n\n")
            with open(hist_file) as f:
                report.write(f.read())
            report.write("\n---\n")
    
    print(f"✅ Report saved to {report_path}")
    
    # Also create a discoveries summary
    discoveries_path = Path('./checkpoints/discoveries.json')
    if discoveries_path.exists():
        print(f"📊 Discoveries saved to {discoveries_path}")

def main():
    parser = argparse.ArgumentParser(description='Run ECDLP research session')
    parser.add_argument('--hours', type=float, default=1.0, 
                        help='Duration of research session in hours')
    parser.add_argument('--checkpoint-interval', type=int, default=300,
                        help='Seconds between checkpoints')
    parser.add_argument('--setup-only', action='store_true',
                        help='Only run setup and checks')
    
    args = parser.parse_args()
    
    print("""
    ╔═══════════════════════════════════════════╗
    ║     ECDLP Research System v1.0            ║
    ║     Finding Polynomial Algorithm          ║
    ║     for secp256k1                         ║
    ╚═══════════════════════════════════════════╝
    """)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies before continuing.")
        return 1
    
    if args.setup_only:
        print("\n✅ Setup complete! Ready to run research.")
        return 0
    
    # Create necessary directories
    for dir_path in ['workspace', 'checkpoints', 'output_dgm']:
        Path(dir_path).mkdir(exist_ok=True)
    
    # Run research
    try:
        run_research_session(
            duration_hours=args.hours,
            checkpoint_interval=args.checkpoint_interval
        )
    except KeyboardInterrupt:
        print("\n\n⚠️  Research interrupted by user")
        generate_final_report()
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())