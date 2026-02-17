# List of 2026 Economic Scenarios
SCENARIOS = [
    {
        "name": "Tech Hiring Freeze",
        "probability": 0.75,
        "type": "income_dip",
        "severity": 0.20, # Income drops 20%
        "duration": 12
    },
    {
        "name": "Rent Spike (+20%)",
        "probability": 0.85,
        "type": "expense_hike",
        "severity": 1.20, # Fixed costs x 1.2
        "duration": 12
    },
    {
        "name": "GenAI Gig Drought",
        "probability": 0.40,
        "type": "income_stop",
        "severity": 0.0, # Income becomes 0
        "duration": 4 # For 4 months
    },
    {
        "name": "Urban Stagflation",
        "probability": 0.70,
        "type": "inflation",
        "severity": 1.10, # All costs x 1.1
        "duration": 12
    },
    {
        "name": "Medical Emergency",
        "probability": 0.20,
        "type": "one_time_shock",
        "severity": 50000, # Flat cost
        "duration": 1 # One month hit
    }
]