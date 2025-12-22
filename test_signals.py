#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, 'ai-engine')

import pandas as pd
from backend.core.live_engine import generate_date_signals

# Mock strategy class
class MockAlphaConfig:
    def __init__(self, enabled=True, weight=1.0):
        self.enabled = enabled
        self.weight = weight

    def dict(self):
        return {"enabled": self.enabled, "weight": self.weight}

class MockStrategy:
    def __init__(self):
        self.alphas = {
            'ml': MockAlphaConfig(enabled=True, weight=1.0)
        }

# Test the function
if __name__ == "__main__":
    strategy = MockStrategy()
    result = generate_date_signals(strategy, 5, '2025-12-16')

    print("API Response:")
    print(f"Mode: {result['mode']}")
    print(f"Date: {result['date']}")
    print(f"Target Date: {result['target_date']}")
    print(f"Signals count: {len(result['signals'])}")
    print()

    # Check CSV
    csv_file = 'ai-engine/data/result/2025-12-16_00-00-00.csv'
    if os.path.exists(csv_file):
        print("CSV Headers:")
        df = pd.read_csv(csv_file)
        print(list(df.columns))
        print()
        print("First few rows:")
        print(df.head())
    else:
        print("CSV file not found")
