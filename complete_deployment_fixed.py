# save as: complete_deployment_fixed.py
import os
import json
import subprocess
import sys
from pathlib import Path

print("🚀 COMPLETE DEPLOYMENT AUTOMATION STARTING...")
print("=" * 60)

# Check if we're in the right directory
if not os.path.exists('backend') or not os.path.exists('frontend'):
    print("❌ Error: Must run from project root directory (ProtoTypeMark1)")
    sys.exit(1)

# Create all necessary files with proper escaping
files_to_create = {
    'backend/requirements.txt': """fastapi==0.104.1
uvicorn[standard]==0.24.0
aiohttp==3.9.0
numpy>=1.26.0
scikit-learn>=1.3.0
joblib>=1.3.0
python-dotenv==1.0.0
websockets==12.0
beautifulsoup4==4.12.2
redis==5.0.1
pandas>=2.0.0
shap>=0.44.0
python-multipart==0.0.6
httpx==0.25.2""",

    '.env': """# API Keys
ODDS_API_KEY=8