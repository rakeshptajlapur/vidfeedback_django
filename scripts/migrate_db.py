import os
import sys
import django
from datetime import datetime
from django.core.management import call_command
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veedfeedback.settings')
django.setup()

def migrate_to_postgres():
    from django.conf import settings
    
    # Step 1: Configure both databases
    DATABASES = {
        'sqlite': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.getenv('SQLITE_PATH'),
        },
        'postgres': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
        }
    }

    # Step 2: Create backup directory
    backup_dir = 'backups'
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(backup_dir, f'sqlite_backup_{timestamp}.json')

    print("\n🔄 Starting database migration process...")
    
    try:
        # Step 3: Backup SQLite data
        print("\n📦 Creating SQLite backup...")
        settings.DATABASES['default'] = DATABASES['sqlite']
        call_command('dumpdata', 
                    exclude=['contenttypes', 'auth.permission'], 
                    indent=2, 
                    output=backup_file)
        print(f"✅ Backup created: {backup_file}")

        # Step 4: Switch to PostgreSQL and migrate
        print("\n🔄 Switching to PostgreSQL...")
        settings.DATABASES['default'] = DATABASES['postgres']
        
        # Apply migrations
        print("\n⚙️ Applying migrations...")
        call_command('migrate')

        # Load data
        print("\n📥 Loading data into PostgreSQL...")
        call_command('loaddata', backup_file)
        
        print("\n✅ Migration completed successfully!")
        
        # Verify data
        verify_migration()

    except Exception as e:
        print(f"\n❌ Error during migration: {str(e)}")
        sys.exit(1)

def verify_migration():
    from accounts.models import BusinessOwner
    from feedback.models import FeedbackForm, FormResponse

    print("\n📊 Data Verification Report")
    print("=" * 50)
    print(f"Business Owners: {BusinessOwner.objects.count()}")
    print(f"Feedback Forms: {FeedbackForm.objects.count()}")
    print(f"Form Responses: {FormResponse.objects.count()}")
    print("=" * 50)

if __name__ == "__main__":
    migrate_to_postgres()