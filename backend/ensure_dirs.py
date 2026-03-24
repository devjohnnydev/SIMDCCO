"""Create reports directory"""
import os
from app.config import settings

def ensure_reports_dir():
    """Ensure reports directory exists"""
    if not os.path.exists(settings.REPORTS_DIR):
        os.makedirs(settings.REPORTS_DIR)
        print(f"✅ Created reports directory: {settings.REPORTS_DIR}")

if __name__ == "__main__":
    ensure_reports_dir()
