import os
import shutil
import datetime
from config import Config

class BackupManager:
    @staticmethod
    def create_backup() -> str:
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_folder = os.path.join(Config.BACKUP_DIR, f"backup_{timestamp}")
        os.makedirs(backup_folder, exist_ok=True)

        for filename in os.listdir(Config.DATA_DIR):
            source_file = os.path.join(Config.DATA_DIR, filename)
            if os.path.isfile(source_file) and filename.endswith('.json'):
                target_file = os.path.join(backup_folder, filename)
                shutil.copy2(source_file, target_file)

        return backup_folder

    @staticmethod
    def list_backups() -> list:
        if not os.path.exists(Config.BACKUP_DIR):
            return []
        backups = [d for d in os.listdir(Config.BACKUP_DIR) if os.path.isdir(os.path.join(Config.BACKUP_DIR, d))]
        backups.sort(reverse=True)
        return backups
