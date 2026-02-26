from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List
import pickle
import numpy as np
import os

# Load model & scaler
MODEL_PATH  = os.path.join(os.path.dirname(__file__), "..", "model", "wine_classifier.pkl")
SCALER_PATH = os.path.join(os.path.dirname(__file__), "..", "model", "scaler.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)
with open(SCALER_PATH, "rb") as f:
    scaler = pickle.load(f)

CLASS_NAMES = ["class_0", "class_1", "class_2"]

app = FastAPI(
    title="Wine Quality Classifier API",
    description="Classifies wines into 3 classes using a Random Forest model.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

@app.get("/ui", include_in_schema=False)
def ui():
    return FileResponse(os.path.join(os.path.dirname(__file__), "static", "index.html"))

# ── Schemas ──────────────────────────────────────────────────────────────────

class WineFeatures(BaseModel):
    alcohol: float              = Field(..., example=13.2)
    malic_acid: float           = Field(..., example=1.78)
    ash: float                  = Field(..., example=2.14)
    alcalinity_of_ash: float    = Field(..., example=11.2)
    magnesium: float            = Field(..., example=100.0)
    total_phenols: float        = Field(..., example=2.65)
    flavanoids: float           = Field(..., example=2.76)
    nonflavanoid_phenols: float = Field(..., example=0.26)
    proanthocyanins: float      = Field(..., example=1.28)
    color_intensity: float      = Field(..., example=4.38)
    hue: float                  = Field(..., example=1.05)
    od280_od315: float          = Field(..., example=3.40)
    proline: float              = Field(..., example=1050.0)

class PredictionResponse(BaseModel):
    predicted_class: int
    class_name: str
    probabilities: dict

class BatchRequest(BaseModel):
    samples: List[WineFeatures]

class BatchResponse(BaseModel):
    results: List[PredictionResponse]

# ── Helpers ───────────────────────────────────────────────────────────────────

FEATURE_ORDER = [
    "alcohol", "malic_acid", "ash", "alcalinity_of_ash", "magnesium",
    "total_phenols", "flavanoids", "nonflavanoid_phenols", "proanthocyanins",
    "color_intensity", "hue", "od280_od315", "proline",
]

def features_to_array(wine: WineFeatures) -> np.ndarray:
    return np.array([[getattr(wine, f) for f in FEATURE_ORDER]])

# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Wine Classifier API is running 🍷"}

@app.get("/info", tags=["Model"])
def model_info():
    return {
        "model": "RandomForestClassifier",
        "n_estimators": model.n_estimators,
        "classes": CLASS_NAMES,
        "features": FEATURE_ORDER,
    }

@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict(wine: WineFeatures):
    try:
        X = features_to_array(wine)
        X_scaled = scaler.transform(X)
        pred  = int(model.predict(X_scaled)[0])
        proba = model.predict_proba(X_scaled)[0].tolist()
        return PredictionResponse(
            predicted_class=pred,
            class_name=CLASS_NAMES[pred],
            probabilities={CLASS_NAMES[i]: round(p, 4) for i, p in enumerate(proba)},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch", response_model=BatchResponse, tags=["Prediction"])
def batch_predict(request: BatchRequest):
    results = []
    for sample in request.samples:
        X = features_to_array(sample)
        X_scaled = scaler.transform(X)
        pred  = int(model.predict(X_scaled)[0])
        proba = model.predict_proba(X_scaled)[0].tolist()
        results.append(PredictionResponse(
            predicted_class=pred,
            class_name=CLASS_NAMES[pred],
            probabilities={CLASS_NAMES[i]: round(p, 4) for i, p in enumerate(proba)},
        ))
    return BatchResponse(results=results)