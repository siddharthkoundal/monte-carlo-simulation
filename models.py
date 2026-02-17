from pydantic import BaseModel
from typing import List, Dict

# --- INPUT SCHEMAS (From Frontend) ---
class ApplicantDetails(BaseModel):
    name: str
    age: int
    city_tier: str
    job_title: str
    stated_monthly_income: float
    housing_status: str
    education: str

class PaymentHistory(BaseModel):
    avg_payment_amount: float
    payment_type: str # "Transactor" or "Revolver"

class BureauData(BaseModel):
    credit_score: int
    total_revolving_limit: float
    current_revolving_balance: float
    utilization_ratio: float
    total_monthly_emi_obligations: float
    payment_history: PaymentHistory
    account_age_years: int

class ApplicationRequest(BaseModel):
    application_id: str
    applicant_details: ApplicantDetails
    bureau_data: BureauData

# --- OUTPUT SCHEMAS (To Frontend) ---
class TwinProfile(BaseModel):
    liquidity_buffer: float
    spending_elasticity: float
    burn_rate: float
    income_volatility: str # Changed to str to match "High (0.35)" format
    archetype: str

class ScenarioResult(BaseModel):
    name: str
    survival: int # Changed from survival_rate to survival (int)

class SimulationResponse(BaseModel):
    application_id: str
    name: str
    score: int
    status: str
    twin_profile: TwinProfile
    scenarios: List[ScenarioResult]
    ai_narrative: str