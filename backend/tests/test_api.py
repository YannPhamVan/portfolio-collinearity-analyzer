from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    """Verify healthcheck endpoint returns 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_analyze_insufficient_assets():
    """Verify validation error for single asset."""
    response = client.post("/analyze", json={"isins": ["AAPL"], "investment_horizon_years": 1})
    assert response.status_code == 422  # Pydantic validation error

def test_analyze_mock_flow():
    """
    Test the full analyze flow with mock tickers (FAKE1, FAKE2).
    This ensures data fetching (fallback to mock) and analysis logic (correlation) run without crashing.
    """
    payload = {
        "isins": ["FAKE1", "FAKE2"],
        "investment_horizon_years": 1
    }
    response = client.post("/analyze", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    # Check structure
    assert "correlation_matrix" in data
    assert "high_r_squared_pairs" in data
    
    # Check content keys
    matrix = data["correlation_matrix"]
    assert "FAKE1" in matrix
    assert "FAKE2" in matrix
