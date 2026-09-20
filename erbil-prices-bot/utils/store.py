"""قراءة وحفظ بيانات الأسعار من ملف JSON."""
import json
from pathlib import Path
from threading import Lock

_lock = Lock()


def load_prices(data_file: Path) -> dict:
    with _lock:
        with open(data_file, "r", encoding="utf-8") as f:
            return json.load(f)


def save_prices(data_file: Path, data: dict) -> None:
    with _lock:
        tmp = data_file.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        tmp.replace(data_file)


def format_amount(value) -> str:
    """تنسيق المبلغ بفواصل الآلاف."""
    try:
        return f"{int(value):,}"
    except (ValueError, TypeError):
        return str(value)
