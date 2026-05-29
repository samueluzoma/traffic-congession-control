from fastapi import FastAPI
from pydantic import BaseModel, Field
import random

app = FastAPI(
    title="Traffic Congestion Control API",
    description="API for predicting intersection congestion levels to optimize traffic lights.",
    version="1.0.0"
)

# Define the expected request body structure using Pydantic
class TrafficData(BaseModel):
    vehicle_count_north: int = Field(..., ge=0, description="Vehicle count from North")
    vehicle_count_south: int = Field(..., ge=0, description="Vehicle count from South")
    vehicle_count_east: int = Field(..., ge=0, description="Vehicle count from East")
    vehicle_count_west: int = Field(..., ge=0, description="Vehicle count from West")
    pedestrian_count: int = Field(..., ge=0, description="Number of pedestrians crossing")
    emergency_vehicle: int = Field(..., ge=0, le=1, description="1 if emergency vehicle present, else 0")
    time_of_day: str = Field(..., description="Morning, Afternoon, Evening, or Night")
    weather_condition: str = Field(..., description="Sunny, Rainy, or Foggy")

@app.get("/")
def home():
    return {"status": "healthy", "message": "Traffic Congestion Control API is running."}

@app.post("/predict")
def predict_congestion(data: TrafficData):
    # Calculate total vehicles at the intersection
    total_vehicles = (
        data.vehicle_count_north + 
        data.vehicle_count_south + 
        data.vehicle_count_east + 
        data.vehicle_count_west
    )
    
    # -----------------------------------------------------------------
    # MOCK ML LOGIC (Replace this section with your trained model load/predict)
    # -----------------------------------------------------------------
    # Implementing a basic heuristic that mirrors your dataset generation
    avg_vehicles = total_vehicles / 4
    
    if avg_vehicles > 40 or data.emergency_vehicle == 1:
        prediction = "High"
    elif avg_vehicles > 20:
        prediction = "Medium"
    else:
        prediction = "Low"
        
    # Introduce small random noise to perfectly simulate your generated dataset behavior
    if random.random() < 0.05:
        prediction = random.choice(['Low', 'Medium', 'High'])
    # -----------------------------------------------------------------

    return {
        "total_vehicles": total_vehicles,
        "emergency_vehicle_present": bool(data.emergency_vehicle),
        "predicted_congestion_level": prediction
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)