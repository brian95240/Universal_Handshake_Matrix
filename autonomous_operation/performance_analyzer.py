
import numpy as np
from typing import Dict, List
from datetime import datetime, timedelta
import pandas as pd
from scipy import stats

class PerformanceAnalyzer:
    def __init__(self):
        self.metrics = {
            'epc': [],  # Earnings Per Click
            'cvr': [],  # Conversion Rate
            'roi': []   # Return on Investment
        }
        self.trend_window = 7  # Days for trend analysis

    def calculate_epc(self, earnings: float, clicks: int) -> float:
        """Calculate Earnings Per Click"""
        return earnings / clicks if clicks > 0 else 0.0

    def calculate_cvr(self, conversions: int, impressions: int) -> float:
        """Calculate Conversion Rate"""
        return (conversions / impressions * 100) if impressions > 0 else 0.0

    def calculate_roi(self, revenue: float, cost: float) -> float:
        """Calculate ROI"""
        return ((revenue - cost) / cost * 100) if cost > 0 else 0.0

    def analyze_performance(self, campaign_data: Dict) -> Dict:
        """Comprehensive performance analysis"""
        analysis = {
            'current_metrics': self.calculate_current_metrics(campaign_data),
            'trends': self.analyze_trends(campaign_data),
            'statistical_significance': self.check_significance(campaign_data),
            'recommendations': []
        }

        # Generate recommendations based on analysis
        analysis['recommendations'] = self.generate_recommendations(analysis)

        return analysis

    def calculate_current_metrics(self, data: Dict) -> Dict:
        """Calculate current performance metrics"""
        return {
            'epc': self.calculate_epc(data['earnings'], data['clicks']),
            'cvr': self.calculate_cvr(data['conversions'], data['impressions']),
            'roi': self.calculate_roi(data['revenue'], data['cost'])
        }

    def analyze_trends(self, data: Dict) -> Dict:
        """Analyze metric trends"""
        df = pd.DataFrame(data['historical_data'])

        trends = {}
        for metric in ['epc', 'cvr', 'roi']:
            if len(df) >= self.trend_window:
                trend = np.polyfit(range(len(df[metric])), df[metric], 1)[0]
                trends[metric] = {
                    'direction': 'up' if trend > 0 else 'down',
                    'magnitude': abs(trend),
                    'significant': abs(trend) > self.get_trend_threshold(metric)
                }

        return trends

    def check_significance(self, data: Dict) -> Dict:
        """Statistical significance testing"""
        significance = {}

        # Compare against baseline/control
        for metric in ['cvr', 'epc']:
            if 'control_data' in data and 'test_data' in data:
                t_stat, p_value = stats.ttest_ind(
                    data['control_data'][metric],
                    data['test_data'][metric]
                )
                significance[metric] = {
                    'significant': p_value < 0.05,
                    'p_value': p_value,
                    'confidence': (1 - p_value) * 100
                }

        return significance

    def generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        # Check for significant negative trends
        for metric, trend in analysis['trends'].items():
            if trend['direction'] == 'down' and trend['significant']:
                recommendations.append(f'Investigate declining {metric.upper()}')

        # Check for poor performance metrics
        metrics = analysis['current_metrics']
        if metrics['roi'] < 0:
            recommendations.append('Campaign is unprofitable - consider pausing')
        elif metrics['roi'] < 50:
            recommendations.append('ROI below target - optimize targeting')

        if metrics['cvr'] < 1:
            recommendations.append('Low conversion rate - review landing page')

        return recommendations
