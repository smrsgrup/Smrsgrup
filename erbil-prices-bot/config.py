"""إعدادات بوت أسعار أربيل / Configuration for the Erbil prices bot."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "prices.json"

# توكن البوت من BotFather عبر متغير البيئة
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# معرّفات المشرفين المسموح لهم بتحديث الأسعار (أرقام Telegram user id مفصولة بفواصل)
_admins = os.environ.get("ADMIN_IDS", "")
ADMIN_IDS = {int(x) for x in _admins.replace(" ", "").split(",") if x.strip().isdigit()}
