
from datetime import datetime
import numpy as np

class MetricsCollector:
    def __init__(self):
        self.metrics = {}

    def record_metric(self, name, value, timestamp=None):
        if timestamp is None:
            timestamp = datetime.utcnow()

        if name not in self.metrics:
            self.metrics[name] = []

        self.metrics[name].append({
            'value': value,
            'timestamp': timestamp
        })

    def get_metric_average(self, name, window=None):
        if name not in self.metrics:
            return None

        values = [m['value'] for m in self.metrics[name]]
        if window:
            values = values[-window:]

        return np.mean(values)
