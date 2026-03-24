from sqlalchemy.orm import configure_mappers
from app.database import Base, engine
# Import all models to ensure they are registered
from app.models.user import User
from app.models.organization import Organization
from app.models.department import Department
from app.models.campaign import Campaign
from app.models.question import Question
from app.models.response import Response
from app.models.report import Report
from app.models.analytic import Analytic
from app.models.audit_log import AuditLog
from app.models.consent import Consent
from app.models.lgpd_deletion import LGPDDeletion

def check_mappers():
    print("Checking mappers...")
    try:
        configure_mappers()
        print("✅ Mappers configured successfully!")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"❌ Mapper Error: {e}")

if __name__ == "__main__":
    check_mappers()
