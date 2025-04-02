import os
import sys
import django
from datetime import datetime
from django.conf import settings

def backup_sqlite():
    # Temporarily switch to SQLite
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }

    # Create backups directory
    backup_dir = 'backups'
    os.makedirs(backup_dir, exist_ok=True)

    # Generate backup filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(backup_dir, f'sqlite_backup_{timestamp}.json')

    print("🔄 Creating SQLite backup...")
    command = f'python manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > {backup_file}'
    os.system(command)
    print(f"✅ Backup completed: {backup_file}")

    return backup_file