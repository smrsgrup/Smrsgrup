"""تنسيق رسائل الأسعار بصيغة نصية مرتبة."""
from .store import format_amount

CURRENCY_LABEL = "دينار"


def _header(title: str, data: dict) -> str:
    updated = data.get("last_updated", "")
    return f"📊 <b>{title}</b>\n🗓 آخر تحديث: {updated}\n"


def format_cement(data: dict) -> str:
    section = data.get("cement", {})
    unit = section.get("unit", "")
    lines = [_header("أسعار الأسمنت في أربيل", data), f"السعر لكل: <b>{unit}</b>\n"]
    for item in section.get("items", []):
        price = format_amount(item.get("price"))
        lines.append(f"🏗 {item.get('name')}: <b>{price}</b> {CURRENCY_LABEL}")
    lines.append(f"\nℹ️ {data.get('note', '')}")
    return "\n".join(lines)


def format_iron(data: dict) -> str:
    section = data.get("iron", {})
    unit = section.get("unit", "")
    lines = [_header("أسعار الحديد في أربيل", data), f"السعر لكل: <b>{unit}</b>\n"]
    for item in section.get("items", []):
        price = format_amount(item.get("price"))
        lines.append(f"🔩 {item.get('name')}: <b>{price}</b> {CURRENCY_LABEL}")
    lines.append(f"\nℹ️ {data.get('note', '')}")
    return "\n".join(lines)


def format_realestate(data: dict) -> str:
    section = data.get("realestate", {})
    lines = [_header("أسعار العقارات في أربيل", data)]
    for item in section.get("items", []):
        price = format_amount(item.get("price"))
        punit = item.get("price_unit", "")
        lines.append(
            f"🏠 {item.get('district')} — {item.get('type')}: "
            f"<b>{price}</b> {CURRENCY_LABEL} / {punit}"
        )
    lines.append(f"\nℹ️ {data.get('note', '')}")
    return "\n".join(lines)
