from http.server import BaseHTTPRequestHandler
import json
import os
import joblib

# Load model artifacts at cold start
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), "vectorizer.pkl")

model = None
vectorizer = None

def load_artifacts():
    global model, vectorizer
    try:
        if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
            model = joblib.load(MODEL_PATH)
            vectorizer = joblib.load(VECTORIZER_PATH)
            print("ML Artifacts loaded successfully.")
        else:
            print(f"Warning: Model artifacts not found at {MODEL_PATH} or {VECTORIZER_PATH}")
    except Exception as e:
        print(f"Error loading artifacts: {e}")

# Load on import (cold start)
load_artifacts()

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        global model, vectorizer
        
        # Parse request body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            data = json.loads(body)
            message = data.get("message", "")
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())
            return
        
        if not model or not vectorizer:
            self.send_response(503)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Model not loaded"}).encode())
            return
        
        try:
            # Vectorize input
            features = vectorizer.transform([message])
            
            # Predict
            probability = model.predict_proba(features)[0][1]
            
            # HEURISTIC DAMPENING
            benign_keywords = ["catalog", "price", "how much", "policy", "handbook", "oil", "item", "where", "guide"]
            if any(kw in message.lower() for kw in benign_keywords):
                if probability > 0.5:
                    probability = 0.35
            
            prediction = 1 if probability >= 0.5 else 0
            
            result = {
                "is_malicious": bool(prediction == 1),
                "confidence_score": float(probability),
                "verdict": "MALICIOUS" if prediction == 1 else "SAFE"
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def do_GET(self):
        result = {"status": "ok", "model_loaded": model is not None}
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
