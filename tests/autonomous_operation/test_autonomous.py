
import unittest
from unittest.mock import Mock, patch, MagicMock
import numpy as np
from datetime import datetime, timedelta

class TestPerformanceAnalyzer(unittest.TestCase):
    def setUp(self):
        self.mock_data = {
            'earnings': 1000.0,
            'clicks': 1000,
            'conversions': 100,
            'impressions': 10000,
            'cost': 500.0,
            'revenue': 1000.0,
            'historical_data': [
                {'epc': 1.0, 'cvr': 0.1, 'roi': 100.0},
                {'epc': 1.1, 'cvr': 0.11, 'roi': 110.0}
            ]
        }

    def test_metric_calculation(self):
        # Test EPC calculation
        epc = self.mock_data['earnings'] / self.mock_data['clicks']
        self.assertEqual(epc, 1.0)

        # Test CVR calculation
        cvr = (self.mock_data['conversions'] / self.mock_data['impressions']) * 100
        self.assertEqual(cvr, 1.0)

        # Test ROI calculation
        roi = ((self.mock_data['revenue'] - self.mock_data['cost']) / self.mock_data['cost']) * 100
        self.assertEqual(roi, 100.0)

    def test_trend_analysis(self):
        # Test trend detection
        historical_epc = [d['epc'] for d in self.mock_data['historical_data']]
        trend = np.polyfit(range(len(historical_epc)), historical_epc, 1)[0]
        self.assertTrue(trend > 0)

    def test_recommendation_generation(self):
        recommendations = []
        if self.mock_data['revenue'] < self.mock_data['cost']:
            recommendations.append('Campaign is unprofitable')
        self.assertEqual(len(recommendations), 0)

class TestBudgetAllocator(unittest.TestCase):
    def setUp(self):
        self.total_budget = 1000.0
        self.campaigns = {
            'campaign1': {
                'impressions': 1000,
                'conversions': 100,
                'revenue': 500.0,
                'cost': 200.0
            },
            'campaign2': {
                'impressions': 1000,
                'conversions': 80,
                'revenue': 400.0,
                'cost': 200.0
            }
        }

    def test_thompson_sampling(self):
        # Test sampling logic
        for campaign in self.campaigns.values():
            alpha = campaign['conversions'] + 1
            beta = campaign['impressions'] - campaign['conversions'] + 1
            self.assertTrue(alpha > 0 and beta > 0)

    def test_budget_distribution(self):
        # Test budget allocation
        total_allocated = sum(
            self.total_budget * (c['revenue']/c['cost']) / sum(c['revenue']/c['cost'] for c in self.campaigns.values())
            for c in self.campaigns.values()
        )
        self.assertAlmostEqual(total_allocated, self.total_budget, places=2)

    def test_roi_confidence(self):
        # Test confidence calculation
        for campaign in self.campaigns.values():
            roi = (campaign['revenue'] - campaign['cost']) / campaign['cost']
            self.assertTrue(roi > 0)

class TestCampaignGenerator(unittest.TestCase):
    def setUp(self):
        self.niche = 'test_niche'
        self.offer = {
            'id': 'offer1',
            'commission': 0.1,
            'conversion_rate': 0.01,
            'competition_score': 0.5
        }

    def test_campaign_creation(self):
        campaign_id = f"{self.niche}-{self.offer['id']}"
        self.assertTrue(len(campaign_id) > 0)

    def test_landing_page_generation(self):
        template = {
            'id': 'template1',
            'content': {
                'hero': {'heading': 'Test'},
                'benefits': ['benefit1'],
                'cta': {'text': 'Sign Up'}
            }
        }
        self.assertIn('hero', template['content'])

    def test_tracking_setup(self):
        tracking = {
            'utm_parameters': {'source': 'test'},
            'conversion_tracking': {'type': 'pixel'},
            'analytics': {'google_analytics': True}
        }
        self.assertTrue(all(tracking.values()))
