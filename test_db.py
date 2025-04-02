import os
import django
from django.conf import settings

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veedfeedback.settings')
django.setup()

# Now test the connection
from django.db import connections
from django.db.utils import OperationalError

try:
    connection = connections['default']
    connection.cursor()
    print("✅ Successfully connected to PostgreSQL!")
    
    # Print connection info
    db_settings = settings.DATABASES['default']
    print(f"\nDatabase Info:")
    print(f"Name: {db_settings['NAME']}")
    print(f"Host: {db_settings['HOST']}")
    print(f"Port: {db_settings['PORT']}")
    
except OperationalError as e:
    print(f"❌ Could not connect to PostgreSQL: {e}")
except Exception as e:
    print(f"❌ An error occurred: {e}")