"""Admin routes - placeholder"""
from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def admin_dashboard():
    return {"message": "Admin endpoint - to be implemented"}
