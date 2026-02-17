import numpy as np

def run_monte_carlo(twin, scenarios, iterations=1000):
    scenario_results = []
    total_weighted_survival = 0
    total_prob = 0

    for sc in scenarios:
        survived = 0
        for _ in range(iterations):
            # Init Savings
            savings = twin['liquidity_buffer'] * twin['burn_rate']

            # Run 12 Months
            is_alive = True
            for month in range(1, 13):
                # Income Logic
                income = twin['income_mean']
                if sc['type'] == 'income_stop' and month <= sc['duration']: income = 0
                elif sc['type'] == 'income_dip': income *= (1 - sc['severity'])

                # Noise
                income *= (1 + np.random.normal(0, twin['income_volatility']))

                # Expense Logic
                fixed = twin['burn_rate']
                disc = twin['income_mean'] * 0.3 # 30% discretionary

                if sc['type'] in ['inflation', 'expense_hike']:
                    fixed *= sc['severity']
                    disc *= sc['severity']

                # Elasticity Check (The Brain)
                if (income - (fixed + disc)) < 0:
                    cut = disc * twin['spending_elasticity']
                    disc -= cut

                # Update Savings
                savings += (income - (fixed + disc))

                if savings < 0:
                    is_alive = False
                    break

            if is_alive: survived += 1

        # Calc Stats
        rate = (survived / iterations) * 100
        scenario_results.append({
            "name": sc['name'],
            "probability": sc['probability'],
            "survival_rate": round(rate, 1)
        })

        total_weighted_survival += (rate * sc['probability'])
        total_prob += sc['probability']

    final_score = int(total_weighted_survival / total_prob) if total_prob > 0 else 0

    return final_score, scenario_results