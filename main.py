from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import ApplicationRequest, SimulationResponse, TwinProfile, ScenarioResult
from profiler import generate_twin_profile
from simulation import run_monte_carlo
from scenarios import SCENARIOS

app = FastAPI()

# Enable CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow your React app
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"status": "ok", "message": "Monte Carlo Simulation API is running"}


@app.post("/analyze", response_model=SimulationResponse)
async def analyze_application(request: ApplicationRequest):
    # 1. Parse Input
    data = request.dict()

    # 2. Generate Twin Profile (Logic in profiler.py)
    # Ensure profiler.py returns raw floats for calculations
    raw_twin = generate_twin_profile(data)

    # 3. Run Simulation (Logic in simulation.py)
    # Ensure simulation.py returns score (int) and scenarios (list)
    score, scenario_results = run_monte_carlo(raw_twin, SCENARIOS)

    # 4. Format "Income Volatility" String (e.g., "High (0.35)")
    vol_val = raw_twin["income_volatility"]
    vol_str = f"High ({vol_val})" if vol_val > 0.2 else f"Low ({vol_val})"

    # 5. Format AI Narrative (Mocked or Real)
    narrative = (
        f"Applicant shows strong resilience. Despite high income volatility ({raw_twin['archetype']}), "
        f"their high Spending Elasticity ({raw_twin['spending_elasticity']}) allows them to absorb shocks. "
        "Warning: Vulnerable to extended 'Income Stops' > 4 months."
    )

    # 6. Construct Final Response
    return {
        "application_id": request.application_id,
        "name": request.applicant_details.name,
        "score": score,
        "status": "APPROVED" if score > 75 else "REJECTED",
        "twin_profile": {
            "liquidity_buffer": raw_twin["liquidity_buffer"],
            "spending_elasticity": raw_twin["spending_elasticity"],
            "burn_rate": raw_twin["burn_rate"],
            "income_volatility": vol_str,
            "archetype": raw_twin["archetype"],
        },
        "scenarios": [
            {
                "name": s["name"],
                "survival": int(s["survival_rate"]),  # Ensure it's an integer
            }
            for s in scenario_results
        ],
        "ai_narrative": narrative,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
