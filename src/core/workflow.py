"""
Price Monitoring Workflow
Handles the main workflow for price monitoring and analysis.
"""
import time
from datetime import datetime
import json
import os
from pathlib import Path

class PriceMonitorWorkflow:
    """Main workflow for price monitoring system."""
    
    def __init__(self, data_dir='data'):
        """Initialize the price monitoring workflow.
        
        Args:
            data_dir (str): Directory to store data files
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.ai_engine = None
        self.historical_prices = []
        self.price_history_file = self.data_dir / 'historical_prices.json'
        self._load_historical_data()
        
    def set_ai_engine(self, ai_engine):
        """Set the AI engine for price analysis.
        
        Args:
            ai_engine: Instance of BaseAIEngine or similar
        """
        self.ai_engine = ai_engine
        if hasattr(ai_engine, 'initialize'):
            ai_engine.initialize()
    
    def _load_historical_data(self):
        """Load historical price data from file if it exists."""
        if self.price_history_file.exists():
            try:
                with open(self.price_history_file, 'r') as f:
                    data = json.load(f)
                    self.historical_prices = data.get('prices', [])
                    print(f"Loaded {len(self.historical_prices)} historical price records.")
            except Exception as e:
                print(f"Error loading historical data: {e}")
                self.historical_prices = []
    
    def _save_historical_data(self):
        """Save current price history to file."""
        try:
            with open(self.price_history_file, 'w') as f:
                json.dump({
                    'last_updated': datetime.now().isoformat(),
                    'prices': self.historical_prices
                }, f, indent=2)
        except Exception as e:
            print(f"Error saving historical data: {e}")
    
    def fetch_current_price(self):
        """Fetch current price from data source.
        
        Returns:
            float: Current price or None if not available
        """
        # This is a placeholder implementation
        # In a real application, this would fetch from an API or database
        import random
        if not self.historical_prices:
            return round(100 + random.uniform(-10, 10), 2)
        last_price = self.historical_prices[-1]['price']
        return round(last_price * (1 + random.uniform(-0.05, 0.05)), 2)
    
    def update_price_history(self, price, timestamp=None):
        """Update price history with new price data.
        
        Args:
            price (float): Current price
            timestamp (str, optional): ISO format timestamp. Defaults to current time.
        """
        if timestamp is None:
            timestamp = datetime.now().isoformat()
            
        self.historical_prices.append({
            'timestamp': timestamp,
            'price': price
        })
        
        # Keep only the last 1000 records to prevent memory issues
        if len(self.historical_prices) > 1000:
            self.historical_prices = self.historical_prices[-1000:]
            
        self._save_historical_data()
    
    def analyze_current_trend(self):
        """Analyze current price trend using AI engine.
        
        Returns:
            dict: Analysis results
        """
        if not self.ai_engine:
            return {'error': 'AI engine not initialized'}
            
        if len(self.historical_prices) < 2:
            return {'error': 'Insufficient data for analysis'}
            
        # Extract prices for analysis
        prices = [p['price'] for p in self.historical_prices]
        
        # Get analysis from AI engine
        analysis = self.ai_engine.analyze_price_trend(prices)
        
        # Add basic statistics
        analysis['last_updated'] = datetime.now().isoformat()
        analysis['data_points'] = len(self.historical_prices)
        
        return analysis
    
    def generate_report(self, analysis):
        """Generate a report from analysis results.
        
        Args:
            analysis (dict): Analysis results from analyze_current_trend()
            
        Returns:
            str: Formatted report
        """
        if 'error' in analysis:
            return f"Error: {analysis['error']}"
            
        report = [
            "=== Price Monitoring Report ===",
            f"Generated at: {analysis.get('last_updated')}",
            f"Data points analyzed: {analysis.get('data_points', 0)}",
            "",
            "Current Analysis:",
            f"- Trend: {analysis.get('trend', 'unknown').capitalize()}",
            f"- Confidence: {analysis.get('confidence', 0) * 100:.1f}%",
            f"- Last Price: ${self.historical_prices[-1]['price']:.2f}" if self.historical_prices else ""
        ]
        
        if hasattr(self.ai_engine, 'generate_insights'):
            insights = self.ai_engine.generate_insights(analysis)
            if insights:
                report.extend(["", "Insights:", insights])
        
        return "\n".join(filter(None, report))
    
    def run_full_workflow(self):
        """Run the complete price monitoring workflow.
        
        Returns:
            dict: Results of the workflow execution
        """
        print("Starting price monitoring workflow...")
        
        # 1. Fetch current price
        current_price = self.fetch_current_price()
        print(f"Current price: ${current_price:.2f}")
        
        # 2. Update price history
        self.update_price_history(current_price)
        print(f"Updated price history with {len(self.historical_prices)} records")
        
        # 3. Analyze trend if we have enough data
        if len(self.historical_prices) >= 2:
            analysis = self.analyze_current_trend()
            report = self.generate_report(analysis)
            print("\n" + report)
            return {
                'success': True,
                'current_price': current_price,
                'analysis': analysis,
                'report': report
            }
        else:
            print("Insufficient data for trend analysis. Collecting more data...")
            return {
                'success': False,
                'message': 'Insufficient data for analysis',
                'current_price': current_price
            }
