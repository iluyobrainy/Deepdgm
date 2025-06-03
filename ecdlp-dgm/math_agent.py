import argparse
import logging
import os
import threading
from logging.handlers import RotatingFileHandler
from pathlib import Path

from llm_withtools import DEEPSEEK_MODEL, chat_with_agent
from utils.verification_utils import verify_mathematical_claim
from utils.progress_tracker import MathematicalProgressTracker

# Thread-local storage for logger instances
thread_local = threading.local()

def get_thread_logger():
    """Get the logger instance specific to the current thread."""
    return getattr(thread_local, 'logger', None)

def set_thread_logger(logger):
    """Set the logger instance for the current thread."""
    thread_local.logger = logger

def setup_logger(log_file='./math_history.md', level=logging.INFO):
    """Set up a logger with both file and console handlers."""
    logger = logging.getLogger(f'MathAgent-{threading.get_ident()}')
    logger.setLevel(level)
    
    # Remove existing handlers to avoid duplicates
    logger.handlers = []
    
    # Create formatters
    file_formatter = logging.Formatter('%(message)s')
    
    # Create and set up file handler
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    file_handler.setLevel(level)
    file_handler.setFormatter(file_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    
    # Store logger in thread-local storage
    set_thread_logger(logger)
    
    return logger

def safe_log(message, level=logging.INFO):
    """Thread-safe logging function."""
    logger = get_thread_logger()
    if logger:
        logger.log(level, message)
    else:
        print(f"Warning: No logger found for thread {threading.get_ident()}")

class MathematicalResearchAgent:
    def __init__(
            self,
            problem_statement,
            workspace_dir,
            research_history_file='./research_history.md',
            checkpoint_dir='./checkpoints',
            self_improve=False,
            problem_id=None,
        ):
        self.problem_statement = problem_statement
        self.workspace_dir = Path(workspace_dir)
        self.workspace_dir.mkdir(exist_ok=True)
        self.research_history_file = research_history_file
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(exist_ok=True)
        self.self_improve = self_improve
        self.problem_id = problem_id if not self_improve else 'dgm_math'
        self.model = DEEPSEEK_MODEL
        self.progress_tracker = MathematicalProgressTracker(self.checkpoint_dir)
        
        # Initialize logger
        self.logger = setup_logger(research_history_file)
        
        # Clear the log file
        with open(research_history_file, 'w') as f:
            f.write('')

    def get_current_progress(self):
        """Get current research progress and discoveries."""
        return self.progress_tracker.get_progress_summary()

    def save_discovery(self, discovery_type, content, verification_status):
        """Save a mathematical discovery with verification status."""
        discovery = {
            'type': discovery_type,
            'content': content,
            'verification_status': verification_status,
            'timestamp': os.path.getmtime(self.research_history_file)
        }
        self.progress_tracker.add_discovery(discovery)

    def forward(self):
        """Main research loop for the mathematical agent."""
        safe_log(f"Starting mathematical research on: {self.problem_statement[:100]}...")
        
        # Get current progress
        current_progress = self.get_current_progress()
        
        # Construct research prompt with current progress
        instruction = f"""You are a mathematical research agent tasked with finding a polynomial-time algorithm for the Elliptic Curve Discrete Logarithm Problem (ECDLP) on secp256k1.

<problem_statement>
{self.problem_statement}
</problem_statement>

<current_progress>
{current_progress}
</current_progress>

<workspace_directory>
{self.workspace_dir}
</workspace_directory>

Your goal is to:
1. Explore novel mathematical approaches to solve ECDLP
2. Formulate and test hypotheses using rigorous mathematical methods
3. Document all attempts, even failed ones, as they provide valuable insights
4. Use available mathematical tools to verify your claims
5. Build upon previous discoveries and failed attempts

Consider approaches from:
- Number theory (prime factorization, modular arithmetic)
- Algebraic geometry (divisors, Riemann-Roch theorem)
- p-adic analysis
- Lattice-based methods
- Quantum-inspired classical algorithms
- Novel mathematical structures beyond real/complex numbers
- Analysis of existing research for overlooked insights

Be creative, rigorous, and persistent. Every small insight could lead to a breakthrough.
"""
        
        # Run research loop
        new_msg_history = chat_with_agent(
            instruction, 
            model=self.model, 
            msg_history=[], 
            logging=safe_log
        )
        
        # Extract and verify any mathematical claims
        self._process_research_output(new_msg_history)

    def _process_research_output(self, msg_history):
        """Process research output, verify claims, and save discoveries."""
        for msg in msg_history:
            if msg['role'] == 'assistant':
                content = msg['content']
                
                # Extract mathematical claims
                claims = self._extract_mathematical_claims(content)
                
                for claim in claims:
                    # Verify the claim
                    verification_result = verify_mathematical_claim(
                        claim, 
                        workspace_dir=self.workspace_dir
                    )
                    
                    # Save the discovery
                    self.save_discovery(
                        discovery_type=claim['type'],
                        content=claim,
                        verification_status=verification_result
                    )
                    
                    safe_log(f"Discovery: {claim['type']} - Verification: {verification_result['status']}")

    def _extract_mathematical_claims(self, content):
        """Extract mathematical claims from agent output."""
        # This would use sophisticated parsing to identify:
        # - Theorems
        # - Algorithms
        # - Conjectures
        # - Computational results
        claims = []
        
        # Placeholder implementation
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and 'text' in item:
                    text = item['text']
                    if any(keyword in text.lower() for keyword in ['theorem', 'algorithm', 'conjecture', 'result']):
                        claims.append({
                            'type': 'general_claim',
                            'content': text
                        })
        
        return claims

def main():
    parser = argparse.ArgumentParser(description='Mathematical research agent for ECDLP.')
    parser.add_argument('--problem_statement', required=True, help='The mathematical problem to research')
    parser.add_argument('--workspace_dir', required=True, help='Directory for mathematical computations')
    parser.add_argument('--research_history_file', required=True, help='Path to research history file')
    parser.add_argument('--checkpoint_dir', default='./checkpoints', help='Directory for saving checkpoints')
    parser.add_argument('--self_improve', default=False, action='store_true', help='Whether in self-improvement mode')
    parser.add_argument('--problem_id', default=None, help='Problem ID for tracking')
    args = parser.parse_args()

    # Create the mathematical research agent
    agent = MathematicalResearchAgent(
        problem_statement=args.problem_statement,
        workspace_dir=args.workspace_dir,
        research_history_file=args.research_history_file,
        checkpoint_dir=args.checkpoint_dir,
        self_improve=args.self_improve,
        problem_id=args.problem_id,
    )

    # Run the research
    agent.forward()

    # Save final progress
    final_progress = agent.get_current_progress()
    progress_file = Path(args.checkpoint_dir) / 'final_progress.json'
    with open(progress_file, 'w') as f:
        import json
        json.dump(final_progress, f, indent=2)

if __name__ == "__main__":
    main()