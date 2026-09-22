import os
import asyncio
import subprocess
import sys
from datetime import datetime

# Telegram modülünü kontrol et, yoksa otomatik yükle
try:
    import telegram
except ImportError:
    print("⚠️ python-telegram-bot bulunamadı, yükleniyor...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot>=20.0"])
    import telegram

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ========== KONFİGÜRASYON ==========
BOT_TOKEN = "8994341857:AAHczknYGFT5aKKcVnSaBzKPpfoWtiDSaKU"
ADMIN_ID = 8768563610
ADMIN_USERNAME = "SiberYagiz"
FORCE_CHANNEL_LINK = "https://t.me/Yxgizkrallik, https://t.me/kratosalsat"
FORCE_CHANNEL_ID = "-1004421527862, -1002695111119"
SUPPORT_USERNAME = "YxgizPy"

# Klasörler
DATA_FOLDER = "user_files"
PENDING_FOLDER = "pending_files"
RUNNING_FOLDER = "running_scripts"
LOG_FOLDER = "script_logs"

for folder in [DATA_FOLDER, PENDING_FOLDER, RUNNING_FOLDER, LOG_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# Veri yapıları
user_data = {}
running_processes = {}
script_logs = {}

# ========== ÇOK DİLLİ METİNLER ==========
LANGUAGES = {
    'tr': {
        'choose_lang': "🌍 Lütfen dilinizi seçin:",
        'welcome': "🚀 *Merhaba {name}!*\nBen *YXGİZ-VDS* 🤖\nÜcretsiz sanal VDS! Python scriptini yükle, admin onaylasın → sen başlat 🚀",
        'rules': "📌 Sadece `.py` dosyası\n⏳ Admin onayı zorunlu\n📊 Normal: 5 dosya | 💎 Premium: 10 dosya",
        'upload_btn': "📤 Dosya Yükle",
        'myfiles_btn': "📂 Dosyalarım",
        'help_btn': "ℹ️ Yardım",
        'support_btn': "🆘 Destek / İletişim",
        'premium_btn': "💎 Premium Satın Al",
        'admin_btn': "👤 Admin",
        'change_lang_btn': "🌍 Dil Değiştir",
        'back_btn': "🔙 Ana Menü",
        'upload_prompt': "📤 Gönder `.py` dosyanı! Admin onayı sonrası çalıştırabilirsin 🚀",
        'file_uploaded': "📤 {file} yüklendi!\n⏳ Admin onayı bekleniyor...",
        'file_approved': "✅ {file} onaylandı! Artık başlatabilirsin.",
        'file_rejected': "❌ {file} dosyası reddedildi.",
        'max_files': "⚠️ Maksimum dosya limitine ulaştın! (Limit: {limit})",
        'only_py': "❌ Sadece `.py` dosyası kabul ediyorum!",
        'permission_req': "Merhaba @{username}!\n\n🚀 Botu kullanabilmek için admin onayı gerekiyor.\nTalebin @{admin}'a gönderildi. Beklemede kal! ⏳",
        'permission_approved': "✅ Tebrikler! Artık YXGİZ-VDS'i tam olarak kullanabilirsin! 🚀",
        'permission_rejected': "❌ Üzgünüm, talebin reddedildi.",
        'banned_msg': "🚫 Bu botu kullanman yasaklandı. Admin ile iletişime geç.",
        'help_text': "ℹ️ *YXGİZ-VDS*\n\n📤 .py dosyası yükle → admin onaylasın → sen başlat/durdur/log gör\n📊 Normal: 5 dosya | Premium: 10 dosya\n🗑 Dosyalarını sil\n👤 Admin: @{admin}",
        'force_sub': "🔒 Botu kullanmak için önce **kanalımıza** katılman gerekiyor!",
        'join_channel': "📢 Kanala Katıl",
        'i_joined': "✅ Katıldım, Kontrol Et",
        'premium_buy_text': "💎 Premium almak için admin ile iletişime geç!\n\n@{support}",
        'support_text': "🆘 Destek / İletişim için admin ile konuş:\n\n@{support}",
        'pending': "⏳ Onay Bekliyor",
        'running': "✅ Çalışıyor",
        'approved': "✅ Onaylı",
        'stopped': "⏸️ Durduruldu",
        'start_btn': "▶️ Başlat",
        'stop_btn': "⏹️ Durdur",
        'log_btn': "📄 Log",
        'delete_btn': "🗑 Sil",
        'no_logs': "📄 Henüz log yok.",
        'started': "✅ {file} başlatılıyor...",
        'stopped_msg': "⏸️ {file} durduruldu.",
        'deleted_msg': "🗑 {file} silindi.",
        'admin_panel_title': "🔧 *Admin Paneli*\nNe yapmak istiyorsun?",
        'stats_btn': "📊 İstatistikler",
        'logs_btn': "📋 Logları Gönder",
        'running_btn': "▶️ Çalışan Scriptler",
        'users_btn': "👥 Onaylı Kullanıcılar",
        'stop_all_btn': "🛑 Tüm Scriptleri Durdur",
        'msg_user_btn': "✉️ Kullanıcıya Mesaj",
        'announce_btn': "📢 Toplu Duyuru",
        'give_premium_btn': "💎 Premium Ver",
        'remove_premium_btn': "💎 Premium Kaldır",
        'install_module_btn': "📦 Modül Yükle",
        'ban_btn': "🚫 Ban At",
        'unban_btn': "✅ Ban Kaldır",
        'back_admin': "🔙 Ana Menüye Dön",
        'stats_text': "📊 *İstatistikler*\n\n👥 Toplam: {total}\n✅ Onaylı: {approved}\n💎 Premium: {premium}\n🚫 Banlı: {banned}\n⏳ Bekleyen: {pending}\n▶️ Çalışan: {running}\n📁 Toplam dosya: {total_files}",
        'no_logs_file': "Henüz log yok.",
        'running_title': "✅ *Çalışan Scriptler*",
        'no_running': "Hiç çalışan script yok.",
        'users_title': "👥 *Onaylı Kullanıcılar*",
        'no_users': "Onaylı kullanıcı yok.",
        'announce_prompt': "📢 Duyuru mesajını yaz:",
        'announce_sent': "📢 Duyuru {count} kişiye gönderildi!",
        'msg_prompt': "✉️ Kullanıcı ID'sini yaz:",
        'msg_text_prompt': "✉️ Mesajı yaz (ID: {uid}):",
        'msg_sent': "✅ Mesaj gönderildi!",
        'ban_prompt': "🚫 Banlanacak ID:",
        'unban_prompt': "✅ Banı kaldırılacak ID:",
        'banned': "🚫 Kullanıcı banlandı!",
        'unbanned': "✅ Ban kaldırıldı!",
        'all_stopped': "🛑 {count} script durduruldu.",
        'nothing_to_stop': "⚠️ Çalışan script yok.",
        'premium_given': "💎 Premium verildi!",
        'premium_removed': "💎 Premium kaldırıldı!",
        'module_prompt': "📦 Modül adını yaz (örn: requests):",
        'module_success': "✅ Modül yüklendi:\n{output}",
        'module_error': "❌ Hata:\n{error}",
        'invalid_id': "❌ Geçersiz ID!",
        'file_not_found': "❌ Dosya bulunamadı.",
    },
    'en': {
        'choose_lang': "🌍 Please select your language:",
        'welcome': "🚀 *Hello {name}!*\nI am *VEXORPVIP-VDS* 🤖\nFree virtual VDS! Upload Python script → admin approves → you start 🚀",
        'rules': "📌 Only `.py` files\n⏳ Admin approval required\n📊 Normal: 5 files | 💎 Premium: 10 files",
        'upload_btn': "📤 Upload File",
        'myfiles_btn': "📂 My Files",
        'help_btn': "ℹ️ Help",
        'support_btn': "🆘 Support",
        'premium_btn': "💎 Buy Premium",
        'admin_btn': "👤 Admin",
        'change_lang_btn': "🌍 Change Language",
        'back_btn': "🔙 Main Menu",
        'upload_prompt': "📤 Send your `.py` file! 🚀",
        'file_uploaded': "📤 {file} uploaded!\n⏳ Waiting for admin approval...",
        'file_approved': "✅ {file} approved! You can now start it.",
        'file_rejected': "❌ {file} rejected.",
        'max_files': "⚠️ File limit reached! (Limit: {limit})",
        'only_py': "❌ Only `.py` files accepted!",
        'permission_req': "Hello @{username}!\n\n🚀 Admin approval required.\nRequest sent to @{admin}. Please wait! ⏳",
        'permission_approved': "✅ Congratulations! You can now use VEXORPVIP-VDS! 🚀",
        'permission_rejected': "❌ Sorry, request rejected.",
        'banned_msg': "🚫 You are banned. Contact admin.",
        'help_text': "ℹ️ *YXGİZ-VDS*\n\n📤 Upload .py → admin approves → start/stop/log\n📊 Normal: 5 | Premium: 10\n🗑 Delete files\n👤 Admin: @{admin}",
        'force_sub': "🔒 You must join our **channel** first!",
        'join_channel': "📢 Join Channel",
        'i_joined': "✅ I Joined, Check",
        'premium_buy_text': "💎 Contact admin to buy Premium:\n\n@{support}",
        'support_text': "🆘 Contact admin:\n\n@{support}",
        'pending': "⏳ Pending",
        'running': "✅ Running",
        'approved': "✅ Approved",
        'stopped': "⏸️ Stopped",
        'start_btn': "▶️ Start",
        'stop_btn': "⏹️ Stop",
        'log_btn': "📄 Log",
        'delete_btn': "🗑 Delete",
        'no_logs': "📄 No logs yet.",
        'started': "✅ {file} starting...",
        'stopped_msg': "⏸️ {file} stopped.",
        'deleted_msg': "🗑 {file} deleted.",
        'admin_panel_title': "🔧 *Admin Panel*\nWhat to do?",
        'stats_btn': "📊 Stats",
        'logs_btn': "📋 Send Logs",
        'running_btn': "▶️ Running Scripts",
        'users_btn': "👥 Approved Users",
        'stop_all_btn': "🛑 Stop All",
        'msg_user_btn': "✉️ Message User",
        'announce_btn': "📢 Broadcast",
        'give_premium_btn': "💎 Give Premium",
        'remove_premium_btn': "💎 Remove Premium",
        'install_module_btn': "📦 Install Module",
        'ban_btn': "🚫 Ban",
        'unban_btn': "✅ Unban",
        'back_admin': "🔙 Back",
        'stats_text': "📊 *Stats*\n\n👥 Total: {total}\n✅ Approved: {approved}\n💎 Premium: {premium}\n🚫 Banned: {banned}\n⏳ Pending: {pending}\n▶️ Running: {running}\n📁 Total files: {total_files}",
        'no_logs_file': "No logs yet.",
        'running_title': "✅ *Running Scripts*",
        'no_running': "No running scripts.",
        'users_title': "👥 *Approved Users*",
        'no_users': "No approved users.",
        'announce_prompt': "📢 Write announcement:",
        'announce_sent': "📢 Sent to {count} users!",
        'msg_prompt': "✉️ Enter user ID:",
        'msg_text_prompt': "✉️ Write message (ID: {uid}):",
        'msg_sent': "✅ Message sent!",
        'ban_prompt': "🚫 Enter user ID to ban:",
        'unban_prompt': "✅ Enter user ID to unban:",
        'banned': "🚫 User banned!",
        'unbanned': "✅ User unbanned!",
        'all_stopped': "🛑 {count} scripts stopped.",
        'nothing_to_stop': "⚠️ No running scripts.",
        'premium_given': "💎 Premium granted!",
        'premium_removed': "💎 Premium removed!",
        'module_prompt': "📦 Enter module name (e.g., requests):",
        'module_success': "✅ Module installed:\n{output}",
        'module_error': "❌ Error:\n{error}",
        'invalid_id': "❌ Invalid ID!",
        'file_not_found': "❌ File not found.",
    },
    'ar': {
        'choose_lang': "🌍 الرجاء اختيار لغتك:",
        'welcome': "🚀 *مرحباً {name}!*\Yxgiz-VDS* 🤖\nVDS افتراضي مجاني! 🚀",
        'rules': "📌 ملفات `.py` فقط\n⏳ موافقة المشرف\n📊 عادي: 5 | 💎 بريميوم: 10",
        'upload_btn': "📤 رفع ملف",
        'myfiles_btn': "📂 ملفاتي",
        'help_btn': "ℹ️ مساعدة",
        'support_btn': "🆘 دعم",
        'premium_btn': "💎 بريميوم",
        'admin_btn': "👤 المشرف",
        'change_lang_btn': "🌍 تغيير اللغة",
        'back_btn': "🔙 القائمة الرئيسية",
        'upload_prompt': "📤 أرسل ملف `.py` الخاص بك! 🚀",
        'file_uploaded': "📤 تم رفع {file}!\n⏳ انتظار الموافقة...",
        'file_approved': "✅ تمت الموافقة على {file}!",
        'file_rejected': "❌ تم رفض {file}.",
        'max_files': "⚠️ وصلت للحد الأقصى! (الحد: {limit})",
        'only_py': "❌ فقط ملفات `.py`!",
        'permission_req': "مرحباً @{username}!\n\n🚀 مطلوب موافقة المشرف.\nتم إرسال طلبك إلى @{admin}. ⏳",
        'permission_approved': "✅ تمت الموافقة! 🚀",
        'permission_rejected': "❌ تم رفض الطلب.",
        'banned_msg': "🚫 تم حظرك. اتصل بالمشرف.",
        'help_text': "ℹ️ *VEXORPVIP-VDS*\n\n📤 رفع .py → موافقة → تشغيل/إيقاف/سجل\n📊 عادي: 5 | بريميوم: 10\n👤 المشرف: @{admin}",
        'force_sub': "🔒 يجب الاشتراك في **القناة** أولاً!",
        'join_channel': "📢 اشترك في القناة",
        'i_joined': "✅ اشتركت، تحقق",
        'premium_buy_text': "💎 للشراء اتصل بالمشرف:\n\n@{support}",
        'support_text': "🆘 للدعم اتصل بالمشرف:\n\n@{support}",
        'pending': "⏳ قيد الانتظار",
        'running': "✅ يعمل",
        'approved': "✅ موافق",
        'stopped': "⏸️ متوقف",
        'start_btn': "▶️ تشغيل",
        'stop_btn': "⏹️ إيقاف",
        'log_btn': "📄 سجل",
        'delete_btn': "🗑 حذف",
        'no_logs': "📄 لا توجد سجلات",
        'started': "✅ جاري تشغيل {file}...",
        'stopped_msg': "⏸️ تم إيقاف {file}.",
        'deleted_msg': "🗑 تم حذف {file}.",
        'admin_panel_title': "🔧 *لوحة المشرف*",
        'stats_btn': "📊 إحصائيات",
        'logs_btn': "📋 إرسال السجلات",
        'running_btn': "▶️ البرامج العاملة",
        'users_btn': "👥 المستخدمين",
        'stop_all_btn': "🛑 إيقاف الكل",
        'msg_user_btn': "✉️ رسالة لمستخدم",
        'announce_btn': "📢 إعلان",
        'give_premium_btn': "💎 منح بريميوم",
        'remove_premium_btn': "💎 إزالة بريميوم",
        'install_module_btn': "📦 تثبيت وحدة",
        'ban_btn': "🚫 حظر",
        'unban_btn': "✅ إلغاء الحظر",
        'back_admin': "🔙 رجوع",
        'stats_text': "📊 *الإحصائيات*\n\n👥 المجموع: {total}\n✅ الموافق: {approved}\n💎 بريميوم: {premium}\n🚫 المحظور: {banned}\n⏳ المعلق: {pending}\n▶️ يعمل: {running}\n📁 الملفات: {total_files}",
        'no_logs_file': "لا توجد سجلات",
        'running_title': "✅ *البرامج العاملة*",
        'no_running': "لا توجد برامج عاملة",
        'users_title': "👥 *المستخدمين*",
        'no_users': "لا يوجد مستخدمين",
        'announce_prompt': "📢 اكتب الإعلان:",
        'announce_sent': "📢 تم الإرسال لـ {count} مستخدم!",
        'msg_prompt': "✉️ أدخل معرف المستخدم:",
        'msg_text_prompt': "✉️ اكتب الرسالة (ID: {uid}):",
        'msg_sent': "✅ تم الإرسال!",
        'ban_prompt': "🚫 معرف المستخدم للحظر:",
        'unban_prompt': "✅ معرف المستخدم لإلغاء الحظر:",
        'banned': "🚫 تم الحظر!",
        'unbanned': "✅ تم إلغاء الحظر!",
        'all_stopped': "🛑 تم إيقاف {count} برنامج.",
        'nothing_to_stop': "⚠️ لا توجد برامج عاملة.",
        'premium_given': "💎 تم منح بريميوم!",
        'premium_removed': "💎 تم إزالة بريميوم!",
        'module_prompt': "📦 اسم الوحدة (مثال: requests):",
        'module_success': "✅ تم التثبيت:\n{output}",
        'module_error': "❌ خطأ:\n{error}",
        'invalid_id': "❌ معرف غير صالح!",
        'file_not_found': "❌ الملف غير موجود.",
    },
    'ru': {
        'choose_lang': "🌍 Пожалуйста, выберите язык:",
        'welcome': "🚀 *Привет {name}!*\nЯ *YXGİZ-VDS* 🤖\nБесплатный виртуальный VDS! 🚀",
        'rules': "📌 Только `.py` файлы\n⏳ Требуется одобрение\n📊 Обычный: 5 | 💎 Премиум: 10",
        'upload_btn': "📤 Загрузить",
        'myfiles_btn': "📂 Мои файлы",
        'help_btn': "ℹ️ Помощь",
        'support_btn': "🆘 Поддержка",
        'premium_btn': "💎 Премиум",
        'admin_btn': "👤 Админ",
        'change_lang_btn': "🌍 Сменить язык",
        'back_btn': "🔙 Главное меню",
        'upload_prompt': "📤 Отправьте `.py` файл! 🚀",
        'file_uploaded': "📤 {file} загружен!\n⏳ Ожидание одобрения...",
        'file_approved': "✅ {file} одобрен!",
        'file_rejected': "❌ {file} отклонён.",
        'max_files': "⚠️ Лимит файлов! (Лимит: {limit})",
        'only_py': "❌ Только `.py` файлы!",
        'permission_req': "Привет @{username}!\n\n🚀 Требуется одобрение админа.\nЗапрос отправлен @{admin}. ⏳",
        'permission_approved': "✅ Одобрено! 🚀",
        'permission_rejected': "❌ Отказано.",
        'banned_msg': "🚫 Вы забанены. Свяжитесь с админом.",
        'help_text': "ℹ️ *VEXORPVIP-VDS*\n\n📤 Загрузите .py → одобрение → запуск/остановка/лог\n📊 Обычный: 5 | Премиум: 10\n👤 Админ: @{admin}",
        'force_sub': "🔒 Подпишитесь на **канал** сначала!",
        'join_channel': "📢 Подписаться",
        'i_joined': "✅ Подписался, проверить",
        'premium_buy_text': "💎 Для покупки свяжитесь с админом:\n\n@{support}",
        'support_text': "🆘 Для поддержки свяжитесь с админом:\n\n@{support}",
        'pending': "⏳ Ожидает",
        'running': "✅ Работает",
        'approved': "✅ Одобрен",
        'stopped': "⏸️ Остановлен",
        'start_btn': "▶️ Запустить",
        'stop_btn': "⏹️ Остановить",
        'log_btn': "📄 Лог",
        'delete_btn': "🗑 Удалить",
        'no_logs': "📄 Логов нет",
        'started': "✅ Запуск {file}...",
        'stopped_msg': "⏸️ {file} остановлен.",
        'deleted_msg': "🗑 {file} удалён.",
        'admin_panel_title': "🔧 *Панель админа*",
        'stats_btn': "📊 Статистика",
        'logs_btn': "📋 Отправить логи",
        'running_btn': "▶️ Работающие скрипты",
        'users_btn': "👥 Пользователи",
        'stop_all_btn': "🛑 Остановить все",
        'msg_user_btn': "✉️ Сообщение",
        'announce_btn': "📢 Рассылка",
        'give_premium_btn': "💎 Выдать премиум",
        'remove_premium_btn': "💎 Убрать премиум",
        'install_module_btn': "📦 Установить модуль",
        'ban_btn': "🚫 Забанить",
        'unban_btn': "✅ Разбанить",
        'back_admin': "🔙 Назад",
        'stats_text': "📊 *Статистика*\n\n👥 Всего: {total}\n✅ Одобрено: {approved}\n💎 Премиум: {premium}\n🚫 Забанено: {banned}\n⏳ Ожидает: {pending}\n▶️ Работает: {running}\n📁 Файлов: {total_files}",
        'no_logs_file': "Логов нет",
        'running_title': "✅ *Работающие скрипты*",
        'no_running': "Нет работающих скриптов",
        'users_title': "👥 *Одобренные пользователи*",
        'no_users': "Нет пользователей",
        'announce_prompt': "📢 Напишите объявление:",
        'announce_sent': "📢 Отправлено {count} пользователям!",
        'msg_prompt': "✉️ Введите ID пользователя:",
        'msg_text_prompt': "✉️ Напишите сообщение (ID: {uid}):",
        'msg_sent': "✅ Сообщение отправлено!",
        'ban_prompt': "🚫 ID для бана:",
        'unban_prompt': "✅ ID для разбана:",
        'banned': "🚫 Пользователь забанен!",
        'unbanned': "✅ Пользователь разбанен!",
        'all_stopped': "🛑 Остановлено {count} скриптов.",
        'nothing_to_stop': "⚠️ Нет работающих скриптов.",
        'premium_given': "💎 Премиум выдан!",
        'premium_removed': "💎 Премиум удалён!",
        'module_prompt': "📦 Введите имя модуля (например, requests):",
        'module_success': "✅ Модуль установлен:\n{output}",
        'module_error': "❌ Ошибка:\n{error}",
        'invalid_id': "❌ Неверный ID!",
        'file_not_found': "❌ Файл не найден.",
    }
}

# ========== YARDIMCI FONKSİYONLAR ==========
def get_lang(user_id):
    return user_data.get(user_id, {}).get('lang', 'tr')

def t(user_id, key, **kwargs):
    lang = get_lang(user_id)
    text = LANGUAGES.get(lang, LANGUAGES['tr']).get(key, LANGUAGES['tr'].get(key, key))
    return text.format(**kwargs, admin=ADMIN_USERNAME, support=SUPPORT_USERNAME)

def get_max_files(user_id):
    return 10 if user_data.get(user_id, {}).get('premium', False) else 5

def is_banned(user_id):
    return user_data.get(user_id, {}).get('banned', False)

async def check_subscription(user_id, context):
    if user_id == ADMIN_ID:
        return True
    try:
        member = await context.bot.get_chat_member(FORCE_CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# ========== SCRIPT YÖNETİMİ ==========
async def run_script(file_path, user_id, filename, context):
    if file_path in running_processes:
        return
    try:
        proc = await asyncio.create_subprocess_exec(
            sys.executable, file_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        running_processes[file_path] = proc
        script_logs.setdefault(file_path, []).append(f"[{datetime.now()}] ✅ Bot started")
        
        async def read_stream(stream, log_type):
            while True:
                line = await stream.readline()
                if not line:
                    break
                text = line.decode().strip()
                if text:
                    script_logs[file_path].append(f"[{log_type}] {text}")
        
        asyncio.create_task(read_stream(proc.stdout, "STDOUT"))
        asyncio.create_task(read_stream(proc.stderr, "STDERR"))
        asyncio.create_task(wait_and_cleanup(proc, file_path))
    except Exception as e:
        script_logs.setdefault(file_path, []).append(f"[{datetime.now()}] ❌ Error: {e}")

async def wait_and_cleanup(proc, file_path):
    await proc.wait()
    if file_path in running_processes:
        del running_processes[file_path]
    script_logs.setdefault(file_path, []).append(f"[{datetime.now()}] ⏸️ Bot stopped")

async def stop_script(file_path):
    proc = running_processes.get(file_path)
    if proc:
        try:
            proc.terminate()
            await asyncio.sleep(1)
            if proc.returncode is None:
                proc.kill()
        except:
            pass
        del running_processes[file_path]
    script_logs.setdefault(file_path, []).append(f"[{datetime.now()}] ⏸️ Bot stopped")

def get_logs(file_path, lines=50):
    logs = script_logs.get(file_path, [])
    return "\n".join(logs[-lines:]) if logs else ""

# ========== KLAVYELER ==========
def get_language_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🇹🇷 Türkçe", callback_data="lang_tr"),
         InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar"),
         InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")]
    ])

def get_main_menu(user_id):
    lang = get_lang(user_id)
    is_premium = user_data.get(user_id, {}).get('premium', False)
    status_text = "💎 Premium" if is_premium else "👤 Normal"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(LANGUAGES[lang]['upload_btn'], callback_data="upload")],
        [InlineKeyboardButton(LANGUAGES[lang]['myfiles_btn'], callback_data="myfiles")],
        [InlineKeyboardButton(LANGUAGES[lang]['help_btn'], callback_data="help")],
        [InlineKeyboardButton(LANGUAGES[lang]['support_btn'], callback_data="support")],
        [InlineKeyboardButton(LANGUAGES[lang]['premium_btn'], callback_data="buy_premium")],
        [InlineKeyboardButton(f"👤 @{ADMIN_USERNAME}", url=f"https://t.me/{ADMIN_USERNAME}")],
        [InlineKeyboardButton(LANGUAGES[lang]['change_lang_btn'], callback_data="change_lang")],
        [InlineKeyboardButton(status_text, callback_data="none")]
    ])

def get_admin_panel_menu(user_id):
    lang = get_lang(user_id)
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(LANGUAGES[lang]['stats_btn'], callback_data="admin_stats"),
         InlineKeyboardButton(LANGUAGES[lang]['running_btn'], callback_data="admin_running")],
        [InlineKeyboardButton(LANGUAGES[lang]['give_premium_btn'], callback_data="admin_give_premium"),
         InlineKeyboardButton(LANGUAGES[lang]['remove_premium_btn'], callback_data="admin_remove_premium")],
        [InlineKeyboardButton(LANGUAGES[lang]['users_btn'], callback_data="admin_users"),
         InlineKeyboardButton(LANGUAGES[lang]['msg_user_btn'], callback_data="admin_msg_user")],
        [InlineKeyboardButton(LANGUAGES[lang]['announce_btn'], callback_data="admin_announce"),
         InlineKeyboardButton(LANGUAGES[lang]['logs_btn'], callback_data="admin_logs")],
        [InlineKeyboardButton(LANGUAGES[lang]['stop_all_btn'], callback_data="admin_stop_all"),
         InlineKeyboardButton(LANGUAGES[lang]['install_module_btn'], callback_data="admin_install_module")],
        [InlineKeyboardButton(LANGUAGES[lang]['ban_btn'], callback_data="admin_ban"),
         InlineKeyboardButton(LANGUAGES[lang]['unban_btn'], callback_data="admin_unban")],
        [InlineKeyboardButton(LANGUAGES[lang]['back_admin'], callback_data="back")]
    ])

async def myfiles_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id):
    lang = get_lang(user_id)
    files = user_data[user_id].get('files', [])
    pending = user_data[user_id].get('pending', [])
    keyboard = []
    
    for f in pending:
        keyboard.append([InlineKeyboardButton(f"⏳ {f} ({LANGUAGES[lang]['pending']})", callback_data="none")])
    
    for f in files:
        file_path = os.path.join(DATA_FOLDER, f"{user_id}_{f}")
        is_running = file_path in running_processes
        status_icon = LANGUAGES[lang]['running'] if is_running else LANGUAGES[lang]['stopped']
        keyboard.append([InlineKeyboardButton(f"{status_icon} {f}", callback_data="none")])
        
        row = []
        if not is_running:
            row.append(InlineKeyboardButton(LANGUAGES[lang]['start_btn'], callback_data=f"start_{user_id}_{f}"))
        else:
            row.append(InlineKeyboardButton(LANGUAGES[lang]['stop_btn'], callback_data=f"stop_{user_id}_{f}"))
        row.append(InlineKeyboardButton(LANGUAGES[lang]['log_btn'], callback_data=f"log_{user_id}_{f}"))
        row.append(InlineKeyboardButton(LANGUAGES[lang]['delete_btn'], callback_data=f"delete_{user_id}_{f}"))
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton(LANGUAGES[lang]['back_btn'], callback_data="back")])
    
    await update.callback_query.edit_message_text(
        f"📂 {LANGUAGES[lang]['myfiles_btn']} ({len(files)+len(pending)}/{get_max_files(user_id)})",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ========== KOMUTLAR ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    username = user.username or user.first_name

    if is_banned(user_id):
        await update.message.reply_text(t(user_id, 'banned_msg'))
        return

    if not await check_subscription(user_id, context):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(t(user_id, 'join_channel'), url=FORCE_CHANNEL_LINK)],
            [InlineKeyboardButton(t(user_id, 'i_joined'), callback_data="check_sub")]
        ])
        await update.message.reply_text(t(user_id, 'force_sub'), reply_markup=keyboard)
        return

    if user_id not in user_data:
        await update.message.reply_text(t(user_id, 'choose_lang'), reply_markup=get_language_keyboard())
        return

    if user_id != ADMIN_ID and not user_data[user_id].get('approved', False):
        await update.message.reply_text(t(user_id, 'permission_req', username=username))
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Onayla", callback_data=f"perm_approve_{user_id}"),
             InlineKeyboardButton("❌ Reddet", callback_data=f"perm_reject_{user_id}")]
        ])
        await context.bot.send_message(ADMIN_ID, f"🆕 Yeni kullanıcı:\n👤 @{username}\n🆔 {user_id}", reply_markup=keyboard)
        return

    await update.message.reply_text(
        t(user_id, 'welcome', name=user.first_name) + "\n\n" + t(user_id, 'rules'),
        parse_mode='Markdown',
        reply_markup=get_main_menu(user_id)
    )

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Bu komut sadece admin içindir!")
        return
    await update.message.reply_text(t(ADMIN_ID, 'admin_panel_title'), parse_mode='Markdown', reply_markup=get_admin_panel_menu(ADMIN_ID))

# ========== CALLBACK HANDLER'LAR ==========
async def language_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    username = query.from_user.username or query.from_user.first_name

    if query.data == "check_sub":
        if await check_subscription(user_id, context):
            if user_id not in user_data:
                await query.edit_message_text(t(user_id, 'choose_lang'), reply_markup=get_language_keyboard())
            else:
                await query.edit_message_text(
                    t(user_id, 'welcome', name=query.from_user.first_name) + "\n\n" + t(user_id, 'rules'),
                    parse_mode='Markdown',
                    reply_markup=get_main_menu(user_id)
                )
        else:
            await query.answer("❌ Hala kanala katılmadın!", show_alert=True)
        return

    if query.data.startswith("lang_"):
        lang_code = query.data.split("_")[1]
        user_data.setdefault(user_id, {})['lang'] = lang_code
        user_data[user_id].setdefault('files', [])
        user_data[user_id].setdefault('pending', [])
        user_data[user_id]['approved'] = (user_id == ADMIN_ID)
        user_data[user_id]['premium'] = False
        user_data[user_id]['banned'] = False
        user_data[user_id]['username'] = username

        if user_id != ADMIN_ID and not user_data[user_id]['approved']:
            await query.edit_message_text(t(user_id, 'permission_req', username=username))
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Onayla", callback_data=f"perm_approve_{user_id}"),
                 InlineKeyboardButton("❌ Reddet", callback_data=f"perm_reject_{user_id}")]
            ])
            await context.bot.send_message(ADMIN_ID, f"🆕 Yeni kullanıcı dil seçti:\n👤 @{username}\n🆔 {user_id}", reply_markup=keyboard)
        else:
            await query.edit_message_text(
                t(user_id, 'welcome', name=query.from_user.first_name) + "\n\n" + t(user_id, 'rules'),
                parse_mode='Markdown',
                reply_markup=get_main_menu(user_id)
            )
    elif query.data == "change_lang":
        await query.edit_message_text("🌍 Yeni dilinizi seçin:", reply_markup=get_language_keyboard())

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if is_banned(user_id):
        await query.edit_message_text(t(user_id, 'banned_msg'))
        return

    if user_id != ADMIN_ID and not user_data.get(user_id, {}).get('approved', False):
        await query.edit_message_text(t(user_id, 'permission_req', username=query.from_user.username or "user"))
        return

    if data.startswith("start_"):
        _, uid_str, filename = data.split("_", 2)
        if int(uid_str) != user_id:
            await query.answer(t(user_id, 'invalid_id'), show_alert=True)
            return
        file_path = os.path.join(DATA_FOLDER, f"{user_id}_{filename}")
        if not os.path.exists(file_path):
            await query.edit_message_text(t(user_id, 'file_not_found'))
            return
        await run_script(file_path, user_id, filename, context)
        await query.edit_message_text(t(user_id, 'started', file=filename))
        await myfiles_menu(update, context, user_id)

    elif data.startswith("stop_"):
        _, uid_str, filename = data.split("_", 2)
        if int(uid_str) != user_id:
            await query.answer(t(user_id, 'invalid_id'), show_alert=True)
            return
        file_path = os.path.join(DATA_FOLDER, f"{user_id}_{filename}")
        await stop_script(file_path)
        await query.edit_message_text(t(user_id, 'stopped_msg', file=filename))
        await myfiles_menu(update, context, user_id)

    elif data.startswith("log_"):
        _, uid_str, filename = data.split("_", 2)
        if int(uid_str) != user_id:
            await query.answer(t(user_id, 'invalid_id'), show_alert=True)
            return
        file_path = os.path.join(DATA_FOLDER, f"{user_id}_{filename}")
        logs = get_logs(file_path)
        if not logs:
            await query.edit_message_text(t(user_id, 'no_logs'))
        else:
            if len(logs) > 4000:
                logs = logs[-4000:]
            await query.edit_message_text(f"📄 {filename} logs:\n\n{logs}")

    elif data.startswith("delete_"):
        _, uid_str, filename = data.split("_", 2)
        if int(uid_str) != user_id:
            await query.answer(t(user_id, 'invalid_id'), show_alert=True)
            return
        file_path = os.path.join(DATA_FOLDER, f"{user_id}_{filename}")
        await stop_script(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        if filename in user_data[user_id].get('files', []):
            user_data[user_id]['files'].remove(filename)
        await query.edit_message_text(t(user_id, 'deleted_msg', file=filename))
        await myfiles_menu(update, context, user_id)

    elif data == "myfiles":
        await myfiles_menu(update, context, user_id)

    elif data == "upload":
        total = len(user_data[user_id].get('files', [])) + len(user_data[user_id].get('pending', []))
        max_limit = get_max_files(user_id)
        if total >= max_limit:
            await query.edit_message_text(t(user_id, 'max_files', limit=max_limit), reply_markup=get_main_menu(user_id))
            return
        await query.edit_message_text(t(user_id, 'upload_prompt'), reply_markup=get_main_menu(user_id))

    elif data == "help":
        await query.edit_message_text(
            t(user_id, 'help_text'),
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t(user_id, 'back_btn'), callback_data="back")]])
        )

    elif data == "support":
        await query.edit_message_text(t(user_id, 'support_text'), reply_markup=get_main_menu(user_id))

    elif data == "buy_premium":
        await query.edit_message_text(t(user_id, 'premium_buy_text'), reply_markup=get_main_menu(user_id))

    elif data == "back":
        await query.edit_message_text(
            t(user_id, 'welcome', name=query.from_user.first_name).split('\n\n')[0],
            reply_markup=get_main_menu(user_id)
        )

    elif data == "none":
        await query.answer()

async def admin_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.from_user.id != ADMIN_ID:
        await query.answer("Sadece admin!")
        return
    await query.answer()
    user_id = ADMIN_ID
    data = query.data

    if data == "admin_stats":
        total = len(user_data)
        approved = sum(1 for d in user_data.values() if d.get('approved') and not d.get('banned'))
        premium = sum(1 for d in user_data.values() if d.get('premium'))
        banned = sum(1 for d in user_data.values() if d.get('banned'))
        pending = sum(len(d.get('pending', [])) for d in user_data.values())
        running = len(running_processes)
        total_files = sum(len(d.get('files', [])) + len(d.get('pending', [])) for d in user_data.values())
        text = t(user_id, 'stats_text', total=total, approved=approved, premium=premium, banned=banned, pending=pending, running=running, total_files=total_files)
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=get_admin_panel_menu(user_id))

    elif data == "admin_logs":
        log_text = ""
        for uid, data in user_data.items():
            log_text += f"ID: {uid} | @{data.get('username', '?')} | Premium: {data.get('premium', False)} | Dosya: {len(data.get('files', []))}\n"
        if log_text:
            with open("backup.txt", "w", encoding="utf-8") as f:
                f.write(log_text)
            await context.bot.send_document(ADMIN_ID, open("backup.txt", "rb"), caption="📊 Kullanıcı Verileri")
        await query.edit_message_text("✅ Loglar gönderildi!", reply_markup=get_admin_panel_menu(user_id))

    elif data == "admin_running":
        lines = []
        for path in running_processes.keys():
            parts = os.path.basename(path).split("_", 1)
            if len(parts) == 2:
                uid, fname = parts
                username = user_data.get(int(uid), {}).get('username', '?')
                lines.append(f"👤 @{username} (ID: {uid}) | 📄 {fname}")
        if not lines:
            await query.edit_message_text(t(user_id, 'no_running'), reply_markup=get_admin_panel_menu(user_id))
        else:
            text = f"{t(user_id, 'running_title')}\n\n" + "\n".join(lines)
            await query.edit_message_text(text, parse_mode='Markdown', reply_markup=get_admin_panel_menu(user_id))

    elif data == "admin_stop_all":
        count = len(running_processes)
        for path in list(running_processes.keys()):
            await stop_script(path)
        await query.edit_message_text(t(user_id, 'all_stopped', count=count), reply_markup=get_admin_panel_menu(user_id))

    elif data == "admin_users":
        approved_users = [(uid, d.get('username', '?')) for uid, d in user_data.items() if d.get('approved') and not d.get('banned')]
        if not approved_users:
            await query.edit_message_text(t(user_id, 'no_users'), reply_markup=get_admin_panel_menu(user_id))
        else:
            lines = [f"👤 @{username} | ID: {uid}" for uid, username in approved_users]
            text = f"{t(user_id, 'users_title')} ({len(lines)}):\n\n" + "\n".join(lines)
            await query.edit_message_text(text, parse_mode='Markdown', reply_markup=get_admin_panel_menu(user_id))

    elif data == "admin_give_premium":
        context.user_data['awaiting_give_premium'] = True
        await query.edit_message_text(t(user_id, 'give_premium_btn') + "\n" + t(user_id, 'msg_prompt'))

    elif data == "admin_remove_premium":
        context.user_data['awaiting_remove_premium'] = True
        await query.edit_message_text(t(user_id, 'remove_premium_btn') + "\n" + t(user_id, 'msg_prompt'))

    elif data == "admin_msg_user":
        context.user_data['awaiting_msg_user'] = True
        await query.edit_message_text(t(user_id, 'msg_prompt'))

    elif data == "admin_announce":
        context.user_data['awaiting_announce'] = True
        await query.edit_message_text(t(user_id, 'announce_prompt'))

    elif data == "admin_ban":
        context.user_data['awaiting_ban'] = True
        await query.edit_message_text(t(user_id, 'ban_prompt'))

    elif data == "admin_unban":
        context.user_data['awaiting_unban'] = True
        await query.edit_message_text(t(user_id, 'unban_prompt'))

    elif data == "admin_install_module":
        context.user_data['awaiting_module'] = True
        await query.edit_message_text(t(user_id, 'module_prompt'))

    elif data == "back":
        await query.edit_message_text(t(user_id, 'admin_panel_title'), parse_mode='Markdown', reply_markup=get_admin_panel_menu(user_id))

async def permission_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.from_user.id != ADMIN_ID:
        return
    await query.answer()
    data = query.data

    if data.startswith("perm_approve_"):
        uid = int(data.split("_")[2])
        user_data.setdefault(uid, {})['approved'] = True
        user_data[uid]['banned'] = False
        await context.bot.send_message(uid, t(uid, 'permission_approved'))
        await query.edit_message_text(query.message.text + "\n\n✅ Onaylandı!")
    elif data.startswith("perm_reject_"):
        uid = int(data.split("_")[2])
        user_data.setdefault(uid, {})['banned'] = True
        user_data[uid]['approved'] = False
        await context.bot.send_message(uid, t(uid, 'permission_rejected'))
        await query.edit_message_text(query.message.text + "\n\n❌ Reddedildi!")

async def file_approval_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.from_user.id != ADMIN_ID:
        return
    await query.answer()
    data = query.data

    if data.startswith("approve_file_"):
        _, _, uid_str, filename = data.split("_", 3)
        uid = int(uid_str)
        pending_path = os.path.join(PENDING_FOLDER, f"{uid}_{filename}")
        final_path = os.path.join(DATA_FOLDER, f"{uid}_{filename}")
        if os.path.exists(pending_path):
            os.rename(pending_path, final_path)
        if filename in user_data[uid].get('pending', []):
            user_data[uid]['pending'].remove(filename)
        user_data[uid].setdefault('files', []).append(filename)
        await context.bot.send_message(uid, t(uid, 'file_approved', file=filename))
        await query.edit_message_caption(caption=query.message.caption + "\n\n✅ Onaylandı!")
    elif data.startswith("reject_file_"):
        _, _, uid_str, filename = data.split("_", 3)
        uid = int(uid_str)
        path = os.path.join(PENDING_FOLDER, f"{uid}_{filename}")
        if os.path.exists(path):
            os.remove(path)
        if filename in user_data[uid].get('pending', []):
            user_data[uid]['pending'].remove(filename)
        await context.bot.send_message(uid, t(uid, 'file_rejected', file=filename))
        await query.edit_message_caption(caption=query.message.caption + "\n\n❌ Reddedildi!")

# ========== DOSYA YÜKLEME ==========
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name

    if is_banned(user_id):
        await update.message.reply_text(t(user_id, 'banned_msg'))
        return

    if user_id != ADMIN_ID and not user_data.get(user_id, {}).get('approved', False):
        await update.message.reply_text(t(user_id, 'permission_req', username=username))
        return

    doc = update.message.document
    if not doc.file_name.lower().endswith('.py'):
        await update.message.reply_text(t(user_id, 'only_py'))
        return

    total = len(user_data[user_id].get('files', [])) + len(user_data[user_id].get('pending', []))
    max_limit = get_max_files(user_id)
    if total >= max_limit:
        await update.message.reply_text(t(user_id, 'max_files', limit=max_limit))
        return

    file = await doc.get_file()
    safe_name = f"{user_id}_{doc.file_name}"
    pending_path = os.path.join(PENDING_FOLDER, safe_name)
    await file.download_to_drive(pending_path)

    user_data[user_id].setdefault('pending', []).append(doc.file_name)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Onayla", callback_data=f"approve_file_{user_id}_{doc.file_name}"),
         InlineKeyboardButton("❌ Reddet", callback_data=f"reject_file_{user_id}_{doc.file_name}")]
    ])
    await context.bot.send_document(
        ADMIN_ID,
        doc,
        caption=f"🆕 Yeni dosya!\n👤 @{username}  ID: {user_id}\n📄 {doc.file_name}\nToplam: {total + 1}/{max_limit}",
        reply_markup=keyboard
    )
    await update.message.reply_text(t(user_id, 'file_uploaded', file=doc.file_name), reply_markup=get_main_menu(user_id))

# ========== ADMİN METİN İŞLEMLERİ ==========
async def handle_admin_actions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    text = update.message.text.strip()
    user_id = ADMIN_ID

    if context.user_data.get('awaiting_give_premium'):
        try:
            uid = int(text)
            user_data.setdefault(uid, {})['premium'] = True
            user_data[uid]['approved'] = True
            await context.bot.send_message(uid, "🎉 Tebrikler! Artık Premium kullanıcısın!")
            await update.message.reply_text(t(user_id, 'premium_given'), reply_markup=get_admin_panel_menu(user_id))
        except:
            await update.message.reply_text(t(user_id, 'invalid_id'), reply_markup=get_admin_panel_menu(user_id))
        context.user_data['awaiting_give_premium'] = False

    elif context.user_data.get('awaiting_remove_premium'):
        try:
            uid = int(text)
            if uid in user_data:
                user_data[uid]['premium'] = False
            await context.bot.send_message(uid, "❌ Premium hesabınız kaldırıldı.")
            await update.message.reply_text(t(user_id, 'premium_removed'), reply_markup=get_admin_panel_menu(user_id))
        except:
            await update.message.reply_text(t(user_id, 'invalid_id'), reply_markup=get_admin_panel_menu(user_id))
        context.user_data['awaiting_remove_premium'] = False

    elif context.user_data.get('awaiting_msg_user'):
        try:
            uid = int(text)
            context.user_data['msg_target'] = uid
            context.user_data['awaiting_msg_user'] = False
            context.user_data['awaiting_msg_text'] = True
            await update.message.reply_text(t(user_id, 'msg_text_prompt', uid=uid))
        except:
            await update.message.reply_text(t(user_id, 'invalid_id'), reply_markup=get_admin_panel_menu(user_id))

    elif context.user_data.get('awaiting_msg_text'):
        target = context.user_data.pop('msg_target', None)
        context.user_data['awaiting_msg_text'] = False
        try:
            await context.bot.send_message(target, f"✉️ *Admin'den mesaj:*\n\n{text}", parse_mode='Markdown')
            await update.message.reply_text(t(user_id, 'msg_sent'), reply_markup=get_admin_panel_menu(user_id))
        except:
            await update.message.reply_text("❌ Gönderilemedi.", reply_markup=get_admin_panel_menu(user_id))

    elif context.user_data.get('awaiting_announce'):
        approved = [uid for uid, d in user_data.items() if d.get('approved') and not d.get('banned')]
        count = 0
        for uid in approved:
            try:
                await context.bot.send_message(uid, f"📢 *DUYURU*\n\n{text}", parse_mode='Markdown')
                count += 1
            except:
                pass
        await update.message.reply_text(t(user_id, 'announce_sent', count=count), reply_markup=get_admin_panel_menu(user_id))
        context.user_data['awaiting_announce'] = False

    elif context.user_data.get('awaiting_ban'):
        try:
            uid = int(text)
            user_data.setdefault(uid, {})['banned'] = True
            user_data[uid]['approved'] = False
            await context.bot.send_message(uid, t(uid, 'banned_msg'))
            await update.message.reply_text(t(user_id, 'banned'), reply_markup=get_admin_panel_menu(user_id))
        except:
            await update.message.reply_text(t(user_id, 'invalid_id'), reply_markup=get_admin_panel_menu(user_id))
        context.user_data['awaiting_ban'] = False

    elif context.user_data.get('awaiting_unban'):
        try:
            uid = int(text)
            if uid in user_data:
                user_data[uid]['banned'] = False
                user_data[uid]['approved'] = True
            await context.bot.send_message(uid, t(uid, 'permission_approved'))
            await update.message.reply_text(t(user_id, 'unbanned'), reply_markup=get_admin_panel_menu(user_id))
        except:
            await update.message.reply_text(t(user_id, 'invalid_id'), reply_markup=get_admin_panel_menu(user_id))
        context.user_data['awaiting_unban'] = False

    elif context.user_data.get('awaiting_module'):
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "install", text], capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                msg = t(user_id, 'module_success', output=result.stdout[-500:])
            else:
                msg = t(user_id, 'module_error', error=result.stderr[-500:])
            await update.message.reply_text(msg, reply_markup=get_admin_panel_menu(user_id))
        except Exception as e:
            await update.message.reply_text(t(user_id, 'module_error', error=str(e)), reply_markup=get_admin_panel_menu(user_id))
        context.user_data['awaiting_module'] = False

# ========== MAIN ==========
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))

    app.add_handler(CallbackQueryHandler(language_handler, pattern="^(lang_|change_lang|check_sub)"))
    app.add_handler(CallbackQueryHandler(button_handler, pattern="^(upload|myfiles|help|back|delete_|buy_premium|support|start_|stop_|log_)"))
    app.add_handler(CallbackQueryHandler(admin_button_handler, pattern="^admin_"))
    app.add_handler(CallbackQueryHandler(permission_handler, pattern="^perm_"))
    app.add_handler(CallbackQueryHandler(file_approval_handler, pattern="^(approve_file_|reject_file_)"))

    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_admin_actions))

    print("🤖 VEXORPVIP-VDS 4 Dilli Bot Başlatıldı!")
    print(f"Admin ID: {ADMIN_ID}")
    print(f"Zorunlu Kanal: {FORCE_CHANNEL_LINK}")
    app.run_polling()

if __name__ == '__main__':
    main()