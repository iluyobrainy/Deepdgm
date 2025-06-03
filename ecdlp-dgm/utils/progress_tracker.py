import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import hashlib

class MathematicalProgressTracker:
    """Track research progress and discoveries."""
    
    def __init__(self, checkpoint_dir: Path):
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(exist_ok=True)
        
        self.progress_file = self.checkpoint_dir / 'progress.json'
        self.discoveries_file = self.checkpoint_dir / 'discoveries.json'
        
        self.load_progress()
        
    def load_progress(self):
        """Load existing progress from disk."""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                self.progress = json.load(f)
        else:
            self.progress = {
                'start_time': datetime.now().isoformat(),
                'total_discoveries': 0,
                'verified_discoveries': 0,
                'major_breakthroughs': [],
                'research_paths': [],
                'failed_attempts': []
            }
        
        if self.discoveries_file.exists():
            with open(self.discoveries_file, 'r') as f:
                self.discoveries = json.load(f)
        else:
            self.discoveries = []
    
    def save_progress(self):
        """Save progress to disk."""
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
        
        with open(self.discoveries_file, 'w') as f:
            json.dump(self.discoveries, f, indent=2)
    
    def add_discovery(self, discovery: Dict):
        """Add a new discovery to the tracker."""
        # Generate unique ID for discovery
        discovery_str = json.dumps(discovery, sort_keys=True)
        discovery_id = hashlib.sha256(discovery_str.encode()).hexdigest()[:16]
        
        discovery['id'] = discovery_id
        discovery['timestamp'] = datetime.now().isoformat()
        
        # Add to discoveries list
        self.discoveries.append(discovery)
        
        # Update progress stats
        self.progress['total_discoveries'] += 1
        
        if discovery.get('verification_status', {}).get('status') == 'verified':
            self.progress['verified_discoveries'] += 1
            
            # Check if major breakthrough
            if discovery.get('verification_status', {}).get('confidence', 0) > 0.9:
                self.progress['major_breakthroughs'].append({
                    'id': discovery_id,
                    'timestamp': discovery['timestamp'],
                    'summary': self._summarize_discovery(discovery)
                })
        
        self.save_progress()
        
    def add_failed_attempt(self, attempt: Dict):
        """Track failed attempts for learning."""
        attempt['timestamp'] = datetime.now().isoformat()
        self.progress['failed_attempts'].append(attempt)
        self.save_progress()
    
    def add_research_path(self, path: Dict):
        """Track research paths explored."""
        path['timestamp'] = datetime.now().isoformat()
        self.progress['research_paths'].append(path)
        self.save_progress()
    
    def get_progress_summary(self) -> str:
        """Get a human-readable progress summary."""
        summary = []
        
        summary.append(f"Research Progress Summary")
        summary.append(f"========================")
        summary.append(f"Total Discoveries: {self.progress['total_discoveries']}")
        summary.append(f"Verified Discoveries: {self.progress['verified_discoveries']}")
        summary.append(f"Major Breakthroughs: {len(self.progress['major_breakthroughs'])}")
        summary.append(f"Research Paths Explored: {len(self.progress['research_paths'])}")
        summary.append(f"Failed Attempts: {len(self.progress['failed_attempts'])}")
        
        if self.progress['major_breakthroughs']:
            summary.append("\nMajor Breakthroughs:")
            for breakthrough in self.progress['major_breakthroughs'][-5:]:  # Last 5
                summary.append(f"- {breakthrough['summary']} ({breakthrough['timestamp']})")
        
        # Recent focus areas
        recent_paths = self.progress['research_paths'][-3:]
        if recent_paths:
            summary.append("\nRecent Research Focus:")
            for path in recent_paths:
                summary.append(f"- {path.get('description', 'Unknown path')}")
        
        return "\n".join(summary)
    
    def _summarize_discovery(self, discovery: Dict) -> str:
        """Create a brief summary of a discovery."""
        disc_type = discovery.get('type', 'unknown')
        content = discovery.get('content', {})
        
        if disc_type == 'algorithm':
            return f"New algorithm: {content.get('algorithm_name', 'unnamed')}"
        elif disc_type == 'theorem':
            return f"Theorem: {content.get('statement', 'unnamed')[:50]}..."
        elif disc_type == 'computation':
            return f"Computational result: {content.get('result', 'unknown')}"
        else:
            return f"{disc_type}: {str(content)[:50]}..."
    
    def get_best_discoveries(self, n: int = 10) -> List[Dict]:
        """Get the n best discoveries based on verification confidence."""
        verified_discoveries = [
            d for d in self.discoveries 
            if d.get('verification_status', {}).get('status') == 'verified'
        ]
        
        # Sort by confidence
        verified_discoveries.sort(
            key=lambda d: d.get('verification_status', {}).get('confidence', 0),
            reverse=True
        )
        
        return verified_discoveries[:n]
    
    def export_research_report(self, output_file: str):
        """Export a comprehensive research report."""
        report = {
            'metadata': {
                'generated': datetime.now().isoformat(),
                'research_duration': self._calculate_duration(),
                'total_discoveries': self.progress['total_discoveries']
            },
            'summary': self.get_progress_summary(),
            'best_discoveries': self.get_best_discoveries(),
            'all_discoveries': self.discoveries,
            'research_paths': self.progress['research_paths'],
            'failed_attempts': self.progress['failed_attempts']
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
    
    def _calculate_duration(self) -> str:
        """Calculate total research duration."""
        start = datetime.fromisoformat(self.progress['start_time'])
        duration = datetime.now() - start
        
        days = duration.days
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        
        return f"{days} days, {hours} hours, {minutes} minutes"