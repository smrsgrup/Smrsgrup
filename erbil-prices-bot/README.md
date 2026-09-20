# 🏗 بوت أسعار أربيل | Erbil Prices Bot

بوت تيليجرام يعرض الأسعار الاسترشادية لـ **الأسمنت** و **الحديد** و **العقارات** في مدينة أربيل.

A Telegram bot that shows indicative prices for **cement**, **iron (rebar)** and **real estate** in Erbil.

## المميزات | Features

- 🏗 أسعار الأسمنت حسب النوع والماركة
- 🔩 أسعار حديد التسليح حسب القطر
- 🏠 أسعار العقارات حسب المنطقة والنوع
- 📱 قائمة تفاعلية بأزرار (Inline Keyboard) وأوامر نصية
- 🔧 تحديث الأسعار من داخل تيليجرام (للمشرفين)
- 🗂 البيانات في ملف `data/prices.json` سهل التعديل

## التشغيل | Setup

1. أنشئ بوتاً عبر [@BotFather](https://t.me/BotFather) واحصل على التوكن.
2. ثبّت المتطلبات:
   ```bash
   pip install -r requirements.txt
   ```
3. اضبط متغيرات البيئة (أو انسخ `.env.example` إلى `.env`):
   ```bash
   export BOT_TOKEN="التوكن_هنا"
   export ADMIN_IDS="معرّف_المشرف"   # اختياري لتفعيل التحديث
   ```
4. شغّل البوت:
   ```bash
   python bot.py
   ```

## الأوامر | Commands

| الأمر | الوظيفة |
|------|---------|
| `/start` | القائمة الرئيسية |
| `/cement` | أسعار الأسمنت |
| `/iron` | أسعار الحديد |
| `/realestate` | أسعار العقارات |
| `/help` | المساعدة |
| `/update <cement\|iron> <الاسم> <السعر>` | تحديث سعر (للمشرفين) |

## تحديث الأسعار | Updating prices

- **يدوياً:** عدّل ملف `data/prices.json` مباشرة.
- **من تيليجرام:** استخدم `/update` بعد ضبط `ADMIN_IDS`، مثال:
  ```
  /update cement أسمنت ماس مقاوم 150000
  ```

## هيكل المشروع | Structure

```
erbil-prices-bot/
├── bot.py                # نقطة التشغيل والمعالجات
├── config.py             # الإعدادات ومتغيرات البيئة
├── data/prices.json      # بيانات الأسعار
├── utils/
│   ├── store.py          # قراءة/حفظ البيانات
│   └── formatting.py     # تنسيق الرسائل
├── requirements.txt
└── .env.example
```

## ملاحظة | Disclaimer

الأسعار **استرشادية** لأغراض العرض وقابلة للتغيّر حسب السوق والتاجر. حدّثها بانتظام لتبقى دقيقة.

Prices are **indicative** and change with the market. Keep them updated.
