def generate_twin_profile(data: dict):
    app = data['applicant_details']
    bureau = data['bureau_data']

    # 1. BURN RATE (Estimated Floor)
    base_burn = 10000
    if app['city_tier'] == 'Tier_1':
        if app['housing_status'] == 'Renting_Solo': base_burn = 30000
        elif app['housing_status'] == 'Renting_Shared': base_burn = 18000
        elif app['housing_status'] == 'Living_with_Parents': base_burn = 5000

    total_burn = base_burn + bureau['total_monthly_emi_obligations']

    # 2. LIQUIDITY BUFFER
    # (Available Credit) / Monthly Burn
    available_credit = bureau['total_revolving_limit'] - bureau['current_revolving_balance']
    # If they are a "Transactor", assume they have 50% of monthly income in cash
    cash_proxy = app['stated_monthly_income'] * 0.5 if bureau['payment_history']['payment_type'] == 'Transactor' else 0

    liquidity_buffer = (available_credit + cash_proxy) / total_burn if total_burn > 0 else 1.0

    # 3. VOLATILITY (Income Risk)
    volatility = 0.05 # Low (Salaried)
    if 'Freelance' in app['job_title'] or 'Gig' in app['job_title']:
        volatility = 0.35
    elif 'Sales' in app['job_title']:
        volatility = 0.20

    # 4. ELASTICITY (Behavioral Agility)
    elasticity = 0.5
    if bureau['payment_history']['payment_type'] == 'Transactor':
        elasticity = 0.85 # Can cut spending fast
    elif bureau['payment_history']['payment_type'] == 'Revolver':
        elasticity = 0.20 # Rigid spending

    return {
        "burn_rate": total_burn,
        "liquidity_buffer": round(liquidity_buffer, 1),
        "income_volatility": volatility,
        "spending_elasticity": elasticity,
        "income_mean": app['stated_monthly_income'],
        "archetype": "High Volatility / High Resilience" if volatility > 0.2 and elasticity > 0.7 else "Standard"
    }