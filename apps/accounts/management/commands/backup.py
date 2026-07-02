import shutil
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

RETENTION = 10


class Command(BaseCommand):
    help = "Cria um backup do banco SQLite em DATA_DIR/backups/"

    def handle(self, *args, **options):
        db_path = Path(settings.DATABASES["default"]["NAME"])
        backup_dir = settings.DATA_DIR / "backups"

        if not db_path.exists():
            self.stdout.write(
                self.style.WARNING(
                    "Banco de dados não encontrado. Nenhum backup criado."
                )
            )
            return

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_name = f"database-{timestamp}.sqlite3"
        backup_path = backup_dir / backup_name

        shutil.copy2(db_path, backup_path)
        self.stdout.write(self.style.SUCCESS(f"Backup criado: {backup_path}"))

        self._apply_retention(backup_dir)

    def _apply_retention(self, backup_dir: Path) -> None:
        backups = sorted(backup_dir.glob("database-*.sqlite3"))
        excess = backups[: max(0, len(backups) - RETENTION)]
        for old in excess:
            old.unlink()
            self.stdout.write(f"Backup antigo removido: {old.name}")
