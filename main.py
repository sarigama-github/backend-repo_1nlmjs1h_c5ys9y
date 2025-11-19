import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

# Import database helpers; these are safe even if DB isn't configured
from database import create_document, get_documents

app = FastAPI(title="North Indian Restaurant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic health checks
@app.get("/")
def read_root():
    return {"message": "Welcome to the North Indian Restaurant API"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        from database import db  # lazy import to read current state
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = getattr(db, "name", "✅ Connected")
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except ImportError:
        response["database"] = "❌ Database module not found"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:120]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

# -------- Menu Endpoints --------

@app.get("/api/menu")
def get_menu():
    try:
        docs = get_documents("dish")
        for d in docs:
            d["_id"] = str(d.get("_id", ""))
        return docs
    except Exception:
        # If DB isn't configured, return an empty list so frontend still loads
        return []

@app.post("/api/menu", status_code=201)
def add_dish(dish: dict):
    try:
        insert_id = create_document("dish", dish)
        return {"id": insert_id, "message": "Dish added"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database unavailable: {str(e)[:200]}")

# -------- Reservation Endpoints --------

@app.post("/api/reservations", status_code=201)
def create_reservation(reservation: dict):
    try:
        insert_id = create_document("reservation", reservation)
        return {"id": insert_id, "message": "Reservation created"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database unavailable: {str(e)[:200]}")

@app.get("/api/reservations")
def list_reservations(limit: Optional[int] = 50):
    try:
        docs = get_documents("reservation", limit=limit)
        for d in docs:
            d["_id"] = str(d.get("_id", ""))
        return docs
    except Exception:
        return []

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
