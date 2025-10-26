from pathlib import Path
import shutil
from typing import Dict, List

from app.core.config import settings

def clear_all_data() -> Dict:
    data_dir = Path(settings.data_dir)
    idx = Path(settings.index_path)

    if idx.exists():
        shutil.rmtree(idx)

    removed_files: List[str] = []
    if data_dir.exists():
        for p in data_dir.iterdir():
            if p.is_file():
                removed_files.append(p.name)
                p.unlink()
    return {"status": "ok", "action": "clear_all_data", "removed_files": removed_files}
