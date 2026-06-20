from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.molecules import router as molecule_router

app = FastAPI(title="Molecule 3D & ADMET API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(molecule_router, prefix="/api/molecules", tags=["molecules"])

@app.get("/")
def root():
    return {"service": "Molecule 3D & ADMET API", "status": "running"}
