
import psutil
import time
from typing import Dict
import json

class ResourceMonitor:
    def __init__(self, cpu_threshold: float = 40.0):
        self.cpu_threshold = cpu_threshold
        self.index_gaps = set()
        self.trending_keywords = set()

    def check_cpu_usage(self) -> bool:
        """Check if CPU usage is below threshold"""
        cpu_percent = psutil.cpu_percent(interval=1)
        return cpu_percent < self.cpu_threshold

    def check_index_gaps(self) -> bool:
        """Check if there are gaps in the affiliate program index"""
        return len(self.index_gaps) > 0

    def check_trending_keywords(self) -> bool:
        """Check if new trending keywords are detected"""
        return len(self.trending_keywords) > 0

    def should_trigger_dorking(self) -> Dict[str, bool]:
        """Determine if dorking should be triggered"""
        triggers = {
            'cpu_available': self.check_cpu_usage(),
            'index_gaps': self.check_index_gaps(),
            'trending_keywords': self.check_trending_keywords()
        }

        return {
            'should_trigger': any(triggers.values()),
            'triggers': triggers
        }

    def update_index_gaps(self, gaps: set):
        """Update known index gaps"""
        self.index_gaps = gaps

    def update_trending_keywords(self, keywords: set):
        """Update trending keywords"""
        self.trending_keywords = keywords
