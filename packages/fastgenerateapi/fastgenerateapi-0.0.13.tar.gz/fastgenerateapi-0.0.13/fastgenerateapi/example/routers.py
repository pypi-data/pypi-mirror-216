from fastapi import APIRouter

from modules.example.views import StaffView, CompanyView

router = APIRouter()

router.include_router(StaffView())
router.include_router(CompanyView())


