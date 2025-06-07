
import numpy as np
from typing import Dict, List
from dataclasses import dataclass
from scipy.stats import beta

@dataclass
class Campaign:
    id: str
    budget: float
    impressions: int
    conversions: int
    revenue: float
    cost: float

class BudgetAllocator:
    def __init__(self, total_budget: float):
        self.total_budget = total_budget
        self.campaigns = {}
        self.min_budget_ratio = 0.1  # Minimum budget allocation per campaign
        self.exploration_ratio = 0.2  # Budget reserved for exploration

    def add_campaign(self, campaign: Campaign):
        """Add or update campaign data"""
        self.campaigns[campaign.id] = campaign

    def thompson_sampling(self) -> Dict[str, float]:
        """Perform Thompson sampling for budget allocation"""
        samples = {}

        for campaign_id, campaign in self.campaigns.items():
            alpha = campaign.conversions + 1
            beta_param = campaign.impressions - campaign.conversions + 1

            # Sample from beta distribution
            sample = beta.rvs(alpha, beta_param)
            samples[campaign_id] = sample

        return samples

    def calculate_roi_confidence(self, campaign: Campaign) -> float:
        """Calculate ROI confidence interval"""
        if campaign.cost == 0:
            return 0

        roi = (campaign.revenue - campaign.cost) / campaign.cost
        n = campaign.impressions

        # Standard error calculation
        se = np.sqrt((roi * (1 - roi)) / n) if n > 0 else float('inf')

        # 95% confidence interval
        confidence = 1 - (2 * stats.norm.cdf(-abs(roi) / se)) if se != float('inf') else 0

        return confidence

    def allocate_budget(self) -> Dict[str, float]:
        """Allocate budget using Thompson sampling and ROI confidence"""
        if not self.campaigns:
            return {}

        # Exploration budget
        exploration_budget = self.total_budget * self.exploration_ratio
        exploitation_budget = self.total_budget - exploration_budget

        # Get Thompson sampling scores
        samples = self.thompson_sampling()

        # Calculate ROI confidence scores
        roi_confidence = {
            cid: self.calculate_roi_confidence(campaign)
            for cid, campaign in self.campaigns.items()
        }

        # Combine scores
        final_scores = {
            cid: samples[cid] * roi_confidence[cid]
            for cid in self.campaigns.keys()
        }

        # Normalize scores
        score_sum = sum(final_scores.values())
        if score_sum > 0:
            normalized_scores = {
                cid: score / score_sum
                for cid, score in final_scores.items()
            }
        else:
            # Equal distribution if no scores
            normalized_scores = {
                cid: 1 / len(self.campaigns)
                for cid in self.campaigns.keys()
            }

        # Allocate exploitation budget
        allocations = {
            cid: exploitation_budget * score
            for cid, score in normalized_scores.items()
        }

        # Distribute exploration budget equally
        exploration_per_campaign = exploration_budget / len(self.campaigns)
        for cid in allocations:
            allocations[cid] += exploration_per_campaign

        return allocations
