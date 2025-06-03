import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

class ECDLPProgressMetrics:
    """Track and evaluate progress on ECDLP research."""
    
    def __init__(self, benchmark_file: str = "benchmarks.json"):
        self.benchmark_file = Path(benchmark_file)
        self.load_benchmarks()
        self.progress_history = []
        
    def load_benchmarks(self):
        """Load ECDLP benchmarks and metrics."""
        with open(self.benchmark_file, 'r') as f:
            data = json.load(f)
            self.benchmarks = data['benchmarks']
            self.metrics = data['progress_metrics']
    
    def evaluate_discovery(self, discovery: Dict) -> Dict:
        """Evaluate a mathematical discovery and assign scores."""
        scores = {
            'theoretical_value': 0,
            'computational_value': 0,
            'novelty': 0,
            'correctness': 0,
            'total': 0
        }
        
        discovery_type = discovery.get('type', '')
        
        # Theoretical advances
        if 'algorithm' in discovery_type:
            if self._is_novel_algorithm(discovery):
                scores['theoretical_value'] = self.metrics['theoretical_advances']['new_algorithm']
                scores['novelty'] = 90
            elif self._is_improved_algorithm(discovery):
                scores['theoretical_value'] = self.metrics['theoretical_advances']['improved_complexity']
                scores['novelty'] = 60
        
        # Computational advances
        if 'solution' in discovery_type:
            difficulty = discovery.get('difficulty', '')
            if difficulty in ['toy', 'small']:
                scores['computational_value'] = self.metrics['computational_advances'][f'solve_{difficulty}']
            elif 'partial' in discovery_type:
                scores['computational_value'] = self.metrics['computational_advances']['partial_solution']
        
        # Correctness based on verification
        verification = discovery.get('verification_status', {})
        if verification.get('status') == 'verified':
            scores['correctness'] = 100
        elif verification.get('status') == 'partial':
            scores['correctness'] = 50
        
        # Total score
        scores['total'] = (
            scores['theoretical_value'] * 0.4 +
            scores['computational_value'] * 0.3 +
            scores['novelty'] * 0.2 +
            scores['correctness'] * 0.1
        )
        
        return scores
    
    def _is_novel_algorithm(self, discovery: Dict) -> bool:
        """Check if the discovery represents a novel algorithm."""
        # Check against known algorithms
        known_algorithms = [
            'baby_giant_step', 'pollard_rho', 'pollard_lambda',
            'index_calculus', 'pohlig_hellman', 'mov_attack', 'sssa_attack'
        ]
        
        algorithm_name = discovery.get('algorithm_name', '').lower()
        return not any(known in algorithm_name for known in known_algorithms)
    
    def _is_improved_algorithm(self, discovery: Dict) -> bool:
        """Check if the discovery improves upon existing algorithms."""
        complexity = discovery.get('complexity', {})
        existing_best = discovery.get('improves_upon', {})
        
        if complexity and existing_best:
            # Compare complexities
            return self._compare_complexity(complexity, existing_best)
        return False
    
    def _compare_complexity(self, new_complexity: Dict, old_complexity: Dict) -> bool:
        """Compare algorithm complexities."""
        # Simplified comparison - would be more sophisticated in practice
        new_ops = new_complexity.get('operations', float('inf'))
        old_ops = old_complexity.get('operations', float('inf'))
        return new_ops < old_ops * 0.9  # At least 10% improvement
    
    def add_progress(self, discovery: Dict, scores: Dict):
        """Add a discovery to the progress history."""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'discovery': discovery,
            'scores': scores
        }
        self.progress_history.append(entry)
    
    def get_total_progress(self) -> Dict:
        """Calculate total progress across all discoveries."""
        total_scores = {
            'theoretical_value': 0,
            'computational_value': 0,
            'best_algorithm_complexity': None,
            'solved_instances': [],
            'major_breakthroughs': []
        }
        
        for entry in self.progress_history:
            scores = entry['scores']
            total_scores['theoretical_value'] += scores['theoretical_value']
            total_scores['computational_value'] += scores['computational_value']
            
            # Track solved instances
            if 'solution' in entry['discovery'].get('type', ''):
                instance_id = entry['discovery'].get('instance_id')
                if instance_id:
                    total_scores['solved_instances'].append(instance_id)
            
            # Track major breakthroughs
            if scores['total'] > 80:
                total_scores['major_breakthroughs'].append(entry)
        
        return total_scores
    
    def export_progress(self, output_file: str):
        """Export progress history to file."""
        with open(output_file, 'w') as f:
            json.dump({
                'progress_history': self.progress_history,
                'total_progress': self.get_total_progress(),
                'export_date': datetime.now().isoformat()
            }, f, indent=2)