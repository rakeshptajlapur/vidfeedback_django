import os
import sys
from pathlib import Path
from datetime import datetime
from django.core.management import call_command
from dotenv import load_dotenv

def setup_django():
    # Set up Django environment
    BASE_DIR = Path(__file__).resolve().parent.parent
    sys.path.append(str(BASE_DIR))
    load_dotenv()

    # Temporarily set SQLite as default database for backup
    os.environ['USE_SQLITE'] = 'True'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidfeedback.settings')
    import django
    django.setup()

def backup_sqlite_data():
    from django.conf import settings
    
    # Create backups directory
    backup_dir = Path(settings.BASE_DIR) / 'backups'
    backup_dir.mkdir(exist_ok=True)
    
    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = backup_dir / f'sqlite_backup_{timestamp}.json'
    
    print("\n📦 Creating SQLite backup...")
    try:
        call_command(
            'dumpdata',
            '--exclude', 'auth.permission',
            '--exclude', 'contenttypes',
            '--exclude', 'admin.logentry',
            '--exclude', 'sessions.session',
            '--indent', '2',
            output=str(backup_file)
        )
        print(f"✅ Backup created: {backup_file}")
        return backup_file
    except Exception as e:
        print(f"❌ Backup failed: {str(e)}")
        sys.exit(1)

def migrate_to_postgres(backup_file):
    # Switch to PostgreSQL
    os.environ.pop('USE_SQLITE', None)
    
    from django.conf import settings
    print("\n🔄 Switching to PostgreSQL...")
    
    try:
        # Apply migrations
        print("\n⚙️ Applying migrations...")
        call_command('migrate')
        
        # Load data from backup
        print("\n📥 Loading data into PostgreSQL...")
        call_command('loaddata', str(backup_file))
        
        print("\n✅ Migration completed!")
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        sys.exit(1)

def verify_data():
    print("\n🔍 Verifying data...")
    from accounts.models import BusinessOwner
    from feedback.models import FeedbackForm, FormResponse
    
    print("\n📊 Data Count Report")
    print("=" * 50)
    print(f"Business Owners: {BusinessOwner.objects.count()}")
    print(f"Feedback Forms: {FeedbackForm.objects.count()}")
    print(f"Form Responses: {FormResponse.objects.count()}")
    print("=" * 50)

if __name__ == "__main__":
    print("🚀 Starting SQLite to PostgreSQL migration...")
    
    # Step 1: Setup Django with SQLite
    setup_django()
    
    # Step 2: Backup SQLite data
    backup_file = backup_sqlite_data()
    
    # Step 3: Migrate to PostgreSQL
    migrate_to_postgres(backup_file)
    
    # Step 4: Verify data
    verify_data()