"""
بوت تيليجرام لأسعار الأسمنت والحديد والعقارات في أربيل.
Telegram bot for cement, iron (rebar) and real estate prices in Erbil.

التشغيل:
    export BOT_TOKEN="توكن_من_BotFather"
    export ADMIN_IDS="123456789"   # اختياري: معرّفات المشرفين
    python bot.py
"""
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

import config
from utils.formatting import format_cement, format_iron, format_realestate
from utils.store import format_amount, load_prices, save_prices

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main_menu() -> InlineKeyboardMarkup:
    """لوحة الأزرار الرئيسية."""
    keyboard = [
        [InlineKeyboardButton("🏗 أسعار الأسمنت", callback_data="cement")],
        [InlineKeyboardButton("🔩 أسعار الحديد", callback_data="iron")],
        [InlineKeyboardButton("🏠 أسعار العقارات", callback_data="realestate")],
        [InlineKeyboardButton("ℹ️ حول البوت", callback_data="about")],
    ]
    return InlineKeyboardMarkup(keyboard)


def back_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("⬅️ رجوع للقائمة", callback_data="menu")]]
    )


WELCOME = (
    "👋 أهلاً بك في <b>بوت أسعار أربيل</b>\n\n"
    "يمكنك معرفة آخر أسعار:\n"
    "🏗 الأسمنت   🔩 الحديد   🏠 العقارات\n\n"
    "اختر من القائمة بالأسفل، أو استخدم الأوامر:\n"
    "/cement — أسعار الأسمنت\n"
    "/iron — أسعار الحديد\n"
    "/realestate — أسعار العقارات\n"
    "/help — المساعدة"
)

ABOUT = (
    "ℹ️ <b>حول البوت</b>\n\n"
    "بوت لعرض الأسعار الاسترشادية لمواد البناء والعقارات في مدينة أربيل.\n"
    "الأسعار تُحدَّث يدوياً وقد تختلف حسب السوق والتاجر.\n\n"
    "لإضافة أو تحديث الأسعار يتواصل المشرف مع البوت عبر أمر /update."
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        WELCOME, reply_markup=main_menu(), parse_mode=ParseMode.HTML
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "📖 <b>الأوامر المتاحة</b>\n\n"
        "/start — القائمة الرئيسية\n"
        "/cement — أسعار الأسمنت\n"
        "/iron — أسعار الحديد\n"
        "/realestate — أسعار العقارات\n"
        "/help — هذه الرسالة\n\n"
        "🔧 للمشرفين:\n"
        "/update <القسم> <الاسم> <السعر>\n"
        "مثال: <code>/update cement أسمنت ماس مقاوم 150000</code>"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)


def _prices():
    return load_prices(config.DATA_FILE)


async def cement(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        format_cement(_prices()), reply_markup=back_menu(), parse_mode=ParseMode.HTML
    )


async def iron(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        format_iron(_prices()), reply_markup=back_menu(), parse_mode=ParseMode.HTML
    )


async def realestate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        format_realestate(_prices()), reply_markup=back_menu(), parse_mode=ParseMode.HTML
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    action = query.data

    if action == "menu":
        await query.edit_message_text(
            WELCOME, reply_markup=main_menu(), parse_mode=ParseMode.HTML
        )
        return
    if action == "about":
        await query.edit_message_text(
            ABOUT, reply_markup=back_menu(), parse_mode=ParseMode.HTML
        )
        return

    formatters = {
        "cement": format_cement,
        "iron": format_iron,
        "realestate": format_realestate,
    }
    formatter = formatters.get(action)
    if formatter:
        await query.edit_message_text(
            formatter(_prices()), reply_markup=back_menu(), parse_mode=ParseMode.HTML
        )


async def update_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """تحديث سعر عنصر موجود (للمشرفين فقط).
    الصيغة: /update <cement|iron> <اسم العنصر> <السعر>
    """
    user_id = update.effective_user.id
    if config.ADMIN_IDS and user_id not in config.ADMIN_IDS:
        await update.message.reply_text("⛔ هذا الأمر مخصص للمشرفين فقط.")
        return
    if not config.ADMIN_IDS:
        await update.message.reply_text(
            "⚠️ لم يتم ضبط قائمة المشرفين (ADMIN_IDS). التحديث معطّل لأسباب أمنية."
        )
        return

    args = context.args or []
    if len(args) < 3:
        await update.message.reply_text(
            "الصيغة الصحيحة:\n"
            "<code>/update &lt;cement|iron&gt; &lt;اسم العنصر&gt; &lt;السعر&gt;</code>",
            parse_mode=ParseMode.HTML,
        )
        return

    section = args[0].lower()
    if section not in ("cement", "iron"):
        await update.message.reply_text("القسم يجب أن يكون cement أو iron.")
        return

    raw_price = args[-1].replace(",", "")
    if not raw_price.isdigit():
        await update.message.reply_text("السعر يجب أن يكون رقماً صحيحاً.")
        return
    new_price = int(raw_price)
    name = " ".join(args[1:-1]).strip()

    data = _prices()
    items = data.get(section, {}).get("items", [])
    for item in items:
        if item.get("name") == name:
            item["price"] = new_price
            data["last_updated"] = __import__("datetime").date.today().isoformat()
            save_prices(config.DATA_FILE, data)
            await update.message.reply_text(
                f"✅ تم تحديث «{name}» إلى <b>{format_amount(new_price)}</b> دينار.",
                parse_mode=ParseMode.HTML,
            )
            return

    available = "، ".join(i.get("name", "") for i in items)
    await update.message.reply_text(
        f"لم أجد عنصراً بالاسم «{name}».\nالعناصر المتاحة: {available}"
    )


def build_application() -> Application:
    if not config.BOT_TOKEN:
        raise RuntimeError(
            "متغير البيئة BOT_TOKEN غير مضبوط. احصل على التوكن من BotFather ثم:\n"
            'export BOT_TOKEN="..."'
        )
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("cement", cement))
    app.add_handler(CommandHandler("iron", iron))
    app.add_handler(CommandHandler("realestate", realestate))
    app.add_handler(CommandHandler("update", update_price))
    app.add_handler(CallbackQueryHandler(button))
    return app


def main() -> None:
    app = build_application()
    logger.info("بدء تشغيل بوت أسعار أربيل...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
