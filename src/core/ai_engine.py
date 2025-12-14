"""
AI Engine for Price Monitoring System
Handles price analysis, trend detection, and anomaly detection.
"""

class BaseAIEngine:
    """Base class for AI-powered price analysis."""
    
    def __init__(self):
        self.initialized = False
        
    def initialize(self):
        """Initialize the AI engine with required models and resources."""
        self.initialized = True
        return True
        
    def analyze_price_trend(self, historical_prices):
        """
        Analyze price trends from historical data.
        
        Args:
            historical_prices (list): List of historical price data points
            
        Returns:
            dict: Analysis results including trend and confidence
        """
        if not self.initialized:
            self.initialize()
            
        # Simple moving average calculation as placeholder
        if not historical_prices or len(historical_prices) < 2:
            return {
                'trend': 'stable',
                'confidence': 0.0,
                'message': 'Insufficient data for analysis'
            }
            
        # Calculate simple moving average
        window_size = min(5, len(historical_prices))
        sma = sum(historical_prices[-window_size:]) / window_size
        
        # Determine trend
        if len(historical_prices) >= 2:
            if historical_prices[-1] > historical_prices[-2] * 1.05:
                trend = 'increasing'
                confidence = min(0.9, (historical_prices[-1] / historical_prices[-2] - 1) * 10)
            elif historical_prices[-1] < historical_prices[-2] * 0.95:
                trend = 'decreasing'
                confidence = min(0.9, (1 - historical_prices[-1] / historical_prices[-2]) * 10)
            else:
                trend = 'stable'
                confidence = 0.5
        else:
            trend = 'stable'
            confidence = 0.0
            
        return {
            'trend': trend,
            'confidence': confidence,
            'moving_average': sma,
            'last_price': historical_prices[-1] if historical_prices else None
        }
    
    def detect_anomalies(self, price_data, threshold=2.0):
        """
        Detect price anomalies using statistical methods.
        
        Args:
            price_data (list): List of price data points
            threshold (float): Z-score threshold for anomaly detection
            
        Returns:
            list: List of indices where anomalies were detected
        """
        if not price_data or len(price_data) < 3:
            return []
            
        import numpy as np
        
        prices = np.array(price_data)
        mean = np.mean(prices)
        std = np.std(prices)
        
        if std == 0:
            return []
            
        z_scores = np.abs((prices - mean) / std)
        anomalies = np.where(z_scores > threshold)[0].tolist()
        
        return anomalies
    
    def generate_insights(self, analysis_results):
        """
        Generate human-readable insights from analysis results.
        
        Args:
            analysis_results (dict): Results from analyze_price_trend
            
        Returns:
            str: Human-readable insights
        """
        if not analysis_results:
            return "No analysis results available."
            
        trend = analysis_results.get('trend', 'unknown')
        confidence = analysis_results.get('confidence', 0)
        last_price = analysis_results.get('last_price', 0)
        moving_avg = analysis_results.get('moving_average', 0)
        
        insights = [
            f"Current price: ${last_price:.2f}",
            f"{trend.capitalize()} trend with {confidence*100:.1f}% confidence"
        ]
        
        if trend == 'increasing':
            insights.append("Consider monitoring closely as prices are rising.")
        elif trend == 'decreasing':
            insights.append("This might be a good time to buy as prices are dropping.")
        else:
            insights.append("Prices appear to be stable.")
            
        return "\n".join(insights)
