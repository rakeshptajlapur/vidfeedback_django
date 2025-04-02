import os
import sys
from pathlib import Path

# Add project directory to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Set up Django
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidfeedback.settings')
django.setup()

from accounts.models import BusinessOwner
from feedback.models import FeedbackForm, FormResponse

def verify_migration():
    print("\n📊 Data Verification Report")
    print("=" * 50)
    
    try:
        owners = BusinessOwner.objects.count()
        forms = FeedbackForm.objects.count()
        responses = FormResponse.objects.count()
        
        print(f"Business Owners: {owners}")
        print(f"Feedback Forms: {forms}")
        print(f"Form Responses: {responses}")
        print("=" * 50)
        
        return all([owners > 0, forms >= 0, responses >= 0])
    
    except Exception as e:
        print(f"❌ Error during verification: {str(e)}")
        return False

if __name__ == "__main__":
    success = verify_migration()
    if not success:
        sys.exit(1)