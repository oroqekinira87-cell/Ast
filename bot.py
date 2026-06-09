"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║   𓆩♛𓆪  PyHost Pro Ultra  𓆩♛𓆪                                                      ║
║   ───※ · بوت استضافة Python & PHP المتكامل · ※───                                  ║
║   ════════════════ v8.3 PAID-ACCESS EDITION ════════════════                             ║
║                                                                                      ║
║   【 ✅ دعم Python + PHP كامل — تشغيل واستضافة                         】           ║
║   【 ✅ نظام الموافقة على الرفع — فحص إداري قبل الاستضافة              】           ║
║   【 ✅ حماية AI متقدمة — يحلل الكود فوراً ويكشف الاختراقات            】           ║
║   【 ✅ واجهة مزخرفة جميلة — رموز وأيقونات احترافية                    】           ║
║   【 ✅ حماية مطلقة للمشرف — لا يُحظر المشرف أبداً                     】           ║
║   【 ✅ حماية API متقدمة — يمنع سرقة التوكن والاختراق                  】           ║
║   【 ✅ لوحة إدارة شاملة — مستخدمون + ملفات + إجراءات                  】           ║
║   【 ✅ مراقبة الموارد CPU/RAM/Disk في الوقت الفعلي                     】           ║
║   【 ✅ Rate Limiting متقدم ضد الفلود                                   】           ║
║   【 ✅ نظام Premium متطور — منح/سحب/انتهاء تلقائي                      】           ║
║   【 ✅ Leaderboard — ترتيب المستخدمين نقاطاً ورفعاً                    】           ║
║   【 ✅ جدولة تشغيل الملفات بوقت محدد                                   】           ║
║   【 ✅ بث متقدم — كل/Premium/جدد                                       】           ║
║   【 ✅ تثبيت مكتبات Python/Composer PHP تلقائياً                       】           ║
║   【 ✅ نسخ احتياطية تلقائية + استعادة                                  】           ║
║   【 ✅ يعمل على VPS/Railway/Render/Replit/Termux                       】           ║
║                                                                                      ║
║   ───※ · التشغيل: python bot.py · ※───                                             ║
║   ───※ · المتطلبات: pip install -r requirements.txt · ※───                         ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
"""

# ══════════════════════════════════════════════════════════════════════════════
# 📦  الاستيرادات
# ══════════════════════════════════════════════════════════════════════════════
import os, re, io, sys, ast, json, time, math, uuid, html, base64, shutil
import signal, random, hashlib, zipfile, asyncio, logging, platform, tempfile
import threading, subprocess, traceback, urllib.parse, copy, struct
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, List, Any, Tuple, Set, Union, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
from functools import wraps, lru_cache
from collections import defaultdict, Counter, deque
from pathlib import Path
from datetime import datetime
import os
from threading import Thread
from flask import Flask

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    # Render يمرر المنفذ تلقائياً عبر متغير البيئة PORT
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# تشغيل السيرفر الوهمي في مسار منفصل (Thread) حتى لا يعطل البوت
def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# استدعاء الدالة لتشغيل السيرفر
keep_alive()
def now_iso():
    return datetime.utcnow().isoformat()
try:
    from telegram import (
        Update, InlineKeyboardButton,
        InlineKeyboardMarkup as TelegramInlineKeyboardMarkup,
        InputFile, BotCommand, BotCommandScopeDefault,
        ChatMember, LabeledPrice, ReplyKeyboardRemove, Message,
    )
    from telegram.ext import (
        Application, CommandHandler, CallbackQueryHandler,
        MessageHandler, filters, ContextTypes,
        PreCheckoutQueryHandler, JobQueue,
    )
    from telegram.constants import ParseMode, ChatAction, ChatMemberStatus
    from telegram.error import TelegramError, BadRequest, Forbidden, Conflict, TimedOut, NetworkError
except ImportError:
    print("❌  مكتبة python-telegram-bot غير مثبتة.\n   نفّذ:  pip install -r requirements.txt")
    raise

# ══════════════════════════════════════════════════════════════════════════════
# ⚙️  الإعدادات الأساسية
# ══════════════════════════════════════════════════════════════════════════════

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "8745850621:AAGgZBPXoGg-e0RX921WF50RAnM9bbNY_MA")
MAIN_BOT_TOKEN_FINGERPRINT: str = hashlib.sha256(BOT_TOKEN.encode("utf-8", errors="ignore")).hexdigest()[:12]
_TOKEN_AUDIT_MAX_BYTES = 2_000_000
_TOKEN_AUDIT_EXTENSIONS = {".py", ".txt", ".env", ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".md"}
_TELEGRAM_TOKEN_RE = re.compile(r"(?<![A-Za-z0-9_])([0-9]{7,12}:[A-Za-z0-9_-]{30,80})(?![A-Za-z0-9_-])")
_LAST_CONFLICT_LOG_TS = 0.0
_LAST_TOKEN_GUARD_TS = 0.0

_admin_env = os.getenv("ADMIN_IDS", "8018653004")
ADMIN_IDS: List[int] = []
for _x in _admin_env.split(","):
    _x = _x.strip()
    if _x.lstrip("-").isdigit():
        ADMIN_IDS.append(int(_x))
if not ADMIN_IDS:
    ADMIN_IDS = [8018653004]

DEFAULT_STARS_PER_10_POINTS: int = 15
DATABASE_FILE: str  = os.getenv("DATABASE_FILE",  "bot_database.json")
FILES_DIR: str      = os.getenv("FILES_DIR",      "hosted_files")
LOGS_DIR: str       = os.getenv("LOGS_DIR",       "bot_logs")
BACKUP_DIR: str     = os.getenv("BACKUP_DIR",     "backups")
TEMP_DIR: str       = os.getenv("TEMP_DIR",       "temp_work")
PENDING_DIR: str    = os.getenv("PENDING_DIR",    "pending_files")

MAX_FILE_SIZE_MB: int        = int(os.getenv("MAX_FILE_SIZE_MB",        "1000"))
MAX_PROCESSES_PER_USER: int  = int(os.getenv("MAX_PROCESSES_PER_USER",  "3"))
RUN_TIMEOUT_SECONDS: int     = int(os.getenv("RUN_TIMEOUT_SECONDS",     "0"))
INSTALL_TIMEOUT_SECONDS: int = int(os.getenv("INSTALL_TIMEOUT_SECONDS", "600"))
RATE_LIMIT_MESSAGES: int     = int(os.getenv("RATE_LIMIT_MESSAGES",     "10"))
RATE_LIMIT_WINDOW: int       = int(os.getenv("RATE_LIMIT_WINDOW",       "10"))

BOT_VERSION: str      = "9.0.0-VIP-ULTRA-PLUS"
BOT_NAME: str         = "𓆩♛𓆪 PyHost Pro Ultra PLUS 𓆩♛𓆪"
SUPPORT_USERNAME: str = os.getenv("SUPPORT_USERNAME", "og4_z")
VIP_SUPPORT_USERNAME: str = "og4_z"  # قناة دعم VIP الرسمية
PAYMENT_PROVIDER_TOKEN: str = ""

STICKERS: Dict[str, str] = {
    "upload_success":   "",
    "login_success":    "CAACAgQAAxkBAxvcqmoHqBAYg1w5e-KMgCVC-Lh8WK_uAAIWAANf_gYhgW1qULu_b787BA",
    "hosting_started":  "",
    "installing_libs":  "AAMCBAADGQEDG92sageqByBwwcqhgeL2o9qY_Ej1AT8AAhoGAAItglRSvVvA4nVI0vcBAAdtAAM7BA",
    "share_link":       "",
    "points_added":     "",
    "security_blocked": "",
    "support_error":    "",
    "admin_action":     "",
    "subscription_ok":  "AAMCBAADGQEDHEtaaghlSir59abfiRa7xzqQzphFgOkAAvECAAKMI1xTvn9SAAGq3m0oAQAHbQADOwQ",
    "premium_granted":  "",
    "leaderboard":      "",
    "new_user":         "",
    "ai_analysis":      "",
    "pending_review":   "",
    "approved":         "",
    "rejected":         "",
    "php_upload":       "",
}

for _d in (FILES_DIR, LOGS_DIR, BACKUP_DIR, TEMP_DIR, PENDING_DIR):
    os.makedirs(_d, exist_ok=True)

# ══════════════════════════════════════════════════════════════════════════════
# 📝  السجلات
# ══════════════════════════════════════════════════════════════════════════════
_log_path = os.path.join(LOGS_DIR, f"bot_{datetime.now().strftime('%Y%m%d')}.log")
logging.basicConfig(
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(_log_path, encoding="utf-8"),
    ],
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("apscheduler").setLevel(logging.WARNING)
logger = logging.getLogger("PyHostBot")


# ══════════════════════════════════════════════════════════════════════════════
# 🛡️ حارس البوت الرئيسي ومنع تضارب التوكنات
# ══════════════════════════════════════════════════════════════════════════════

def _mask_token(token: str) -> str:
    """يعرض التوكن بشكل آمن بدون كشفه كاملاً داخل الرسائل."""
    if not token or ":" not in token:
        return "غير معروف"
    left, right = token.split(":", 1)
    return f"{left}:{right[:6]}…{right[-4:]}"


def _file_contains_token(path: str, token: str) -> bool:
    try:
        if not path or not os.path.isfile(path):
            return False
        if os.path.getsize(path) > _TOKEN_AUDIT_MAX_BYTES:
            return False
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            return token in fh.read(_TOKEN_AUDIT_MAX_BYTES)
    except Exception:
        return False


def _tree_contains_token(root: str, token: str) -> bool:
    try:
        if os.path.isfile(root):
            return _file_contains_token(root, token)
        for base, _dirs, files in os.walk(root):
            for name in files[:250]:
                path = os.path.join(base, name)
                if os.path.splitext(name.lower())[1] in _TOKEN_AUDIT_EXTENSIONS and _file_contains_token(path, token):
                    return True
    except Exception:
        pass
    return False


def _kill_local_token_conflicts(reason: str = "") -> int:
    """يحاول إيقاف أي عملية محلية تستخدم توكن البوت الرئيسي حتى يبقى هذا البوت هو الرئيسي."""
    killed = 0
    try:
        import psutil
    except Exception:
        return 0
    current_pid = os.getpid()
    protected = {current_pid, os.getppid()}
    for proc in psutil.process_iter(["pid", "name", "cmdline", "environ"]):
        try:
            pid = int(proc.info.get("pid") or 0)
            if pid <= 0 or pid in protected:
                continue
            cmdline = proc.info.get("cmdline") or []
            joined_cmd = " ".join(str(x) for x in cmdline)
            env = proc.info.get("environ") or {}
            joined_env = "\n".join(f"{k}={v}" for k, v in env.items()) if isinstance(env, dict) else str(env)
            matched = BOT_TOKEN and (BOT_TOKEN in joined_cmd or BOT_TOKEN in joined_env)
            if not matched:
                for arg in cmdline:
                    arg_s = str(arg)
                    if arg_s.endswith((".py", ".pyw")) and _file_contains_token(arg_s, BOT_TOKEN):
                        matched = True
                        break
            if not matched:
                continue
            logger.warning("🛑 إيقاف عملية متضاربة تستخدم توكن البوت الرئيسي PID=%s %s", pid, f"({reason})" if reason else "")
            try:
                proc.terminate()
                proc.wait(timeout=4)
            except Exception:
                try:
                    proc.kill()
                except Exception:
                    pass
            killed += 1
        except Exception:
            continue
    if killed:
        logger.warning("✅ تم إيقاف %s عملية محلية متضاربة — هذا البوت يبقى الرئيسي.", killed)
    return killed


def _start_primary_token_guard() -> None:
    """حارس خلفي يكرر فحص التضارب محلياً أثناء عمل البوت."""
    def _loop():
        while True:
            try:
                _kill_local_token_conflicts("حارس دوري")
            except Exception:
                pass
            time.sleep(20)
    try:
        threading.Thread(target=_loop, daemon=True).start()
        logger.info("🛡️ تم تشغيل حارس البوت الرئيسي ضد أي نسخة محلية متضاربة.")
    except Exception as exc:
        logger.warning("تعذّر تشغيل حارس البوت الرئيسي: %s", exc)


def _extract_telegram_tokens_from_path(path: str) -> List[str]:
    """يستخرج توكنات Telegram من ملف أو مجلد، مع تجنب الملفات الكبيرة والثنائية."""
    found: List[str] = []
    seen: Set[str] = set()

    def scan_file(fp: str) -> None:
        try:
            if not os.path.isfile(fp):
                return
            ext = os.path.splitext(fp.lower())[1]
            if ext not in _TOKEN_AUDIT_EXTENSIONS:
                return
            if os.path.getsize(fp) > _TOKEN_AUDIT_MAX_BYTES:
                return
            with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                data = fh.read(_TOKEN_AUDIT_MAX_BYTES)
            for token in _TELEGRAM_TOKEN_RE.findall(data):
                if token not in seen:
                    seen.add(token)
                    found.append(token)
        except Exception:
            pass

    if os.path.isfile(path):
        scan_file(path)
    else:
        scanned = 0
        for base, _dirs, files in os.walk(path):
            for name in files:
                scan_file(os.path.join(base, name))
                scanned += 1
                if scanned >= 250:
                    return found
    return found


def _inspect_telegram_token(token: str) -> Dict[str, Any]:
    """يفحص التوكن عبر getMe ويُرجع بيانات البوت إن كان صالحاً."""
    info: Dict[str, Any] = {"token_masked": _mask_token(token), "ok": False}
    try:
        import urllib.request
        url = f"https://api.telegram.org/bot{token}/getMe"
        with urllib.request.urlopen(url, timeout=8) as resp:
            raw = resp.read(65536).decode("utf-8", errors="replace")
        data = json.loads(raw)
        if data.get("ok") and isinstance(data.get("result"), dict):
            r = data["result"]
            info.update({
                "ok": True,
                "bot_id": r.get("id"),
                "username": r.get("username") or "",
                "first_name": r.get("first_name") or "",
                "is_main": token == BOT_TOKEN,
            })
    except Exception as exc:
        info["error"] = str(exc)[:120]
    return info


def _format_token_audit(owner_id: int, file_name: str, infos: List[Dict[str, Any]]) -> str:
    rows = []
    for idx, info in enumerate(infos, 1):
        user = f"@{escape_html(info.get('username') or '')}" if info.get("username") else "—"
        bot_id = escape_html(str(info.get("bot_id") or "غير معروف"))
        name = escape_html(str(info.get("first_name") or "غير معروف"))
        status = "✅ صالح" if info.get("ok") else "⚠️ غير مؤكد"
        main = "\n   🚫 <b>يطابق توكن البوت الرئيسي — تم منعه لمنع التضارب</b>" if info.get("is_main") else ""
        rows.append(
            f"<b>{idx})</b> {status}\n"
            f"   🔐 التوكن: <code>{escape_html(info.get('token_masked', 'مخفي'))}</code>\n"
            f"   🆔 ID: <code>{bot_id}</code>\n"
            f"   👤 User: <b>{user}</b>\n"
            f"   🤖 Name: <b>{name}</b>{main}"
        )
    return (
        "𓆩🔐𓆪 <b>تقرير توكنات Telegram داخل ملف مرفوع</b>\n"
        f"{SEP_MAIN}\n"
        f"👤 صاحب الملف: <code>{owner_id}</code>\n"
        f"📄 الملف: <code>{escape_html(file_name)}</code>\n"
        f"🔎 العدد: <b>{len(infos)}</b>\n"
        f"{SEP_THIN}\n" + "\n\n".join(rows)
    )


async def _notify_token_audit(update: Update, context: ContextTypes.DEFAULT_TYPE, owner_id: int, file_name: str, tokens: List[str]) -> List[Dict[str, Any]]:
    """يرسل تقريراً منظماً عند العثور على توكنات، بدون كشف التوكن كاملاً حمايةً لصاحب الملف."""
    if not tokens:
        return []
    infos = [_inspect_telegram_token(t) for t in tokens[:8]]
    text = _format_token_audit(owner_id, file_name, infos)
    try:
        await update.message.reply_text(text, parse_mode=ParseMode.HTML)
    except Exception:
        pass
    for adm in ADMIN_IDS:
        try:
            await context.bot.send_message(adm, text, parse_mode=ParseMode.HTML)
        except Exception:
            pass
    return infos

# ══════════════════════════════════════════════════════════════════════════════
# 🎨  الأيقونات والزخارف
# ══════════════════════════════════════════════════════════════════════════════
class Icon:
    # ─── أساسية ───
    BOT     = "🤖";  FIRE    = "🔥";  STAR    = "⭐";  DIAMOND = "💎";  ROCKET  = "🚀"
    LOCK    = "🔒";  UNLOCK  = "🔓";  KEY     = "🔑";  CHECK   = "✅";  CROSS   = "❌"
    WARN    = "⚠️"; INFO    = "ℹ️"; GIFT    = "🎁";  CROWN   = "👑";  USER    = "👤"
    USERS   = "👥";  SETTINGS= "⚙️"; STATS   = "📊";  FILE    = "📄";  FOLDER  = "📁"
    UPLOAD  = "📤";  DOWNLOAD= "📥";  PLAY    = "▶️"; STOP    = "⏹";  RESTART = "🔄"
    DELETE  = "🗑";  EDIT    = "✏️"; SEARCH  = "🔍";  BELL    = "🔔";  BROADCAST="📢"
    LINK    = "🔗";  BACK    = "⬅️"; NEXT    = "➡️"; PREV    = "◀️"; HOME    = "🏠"
    SUPPORT = "💬";  HEART   = "❤️"; CHANNEL = "📣";  PIN     = "📌";  CLOCK   = "⏰"
    NOTE    = "📝";  TASK    = "✔️"; TOOLS   = "🛠";  LIGHT   = "💡";  SHIELD  = "🛡"
    BAN     = "🚫";  UNBAN   = "🟢";  CODE    = "💻";  TERMINAL= "📺";  INBOX   = "📬"
    PLUS    = "➕";  MINUS   = "➖";  LIST    = "📋";  REFRESH = "🔁";  CHART   = "📈"
    TROPHY  = "🏆";  MEDAL   = "🥇";  PREMIUM = "💫";  SERVER  = "🖥";  MEMORY  = "🧠"
    CPU     = "⚡";  DISK    = "💽";  NETWORK = "🌐";  TIMER   = "⏱";  CALENDAR= "📅"
    ALERT   = "🚨";  SUCCESS = "🟢";  PRIMARY = "🔵";  DANGER  = "🔴";  WARNING = "🟡"
    FLASH   = "⚡";  MAGIC   = "✨";  POWER   = "💪";  FAST    = "🚀";  NEW_ICO = "🆕"
    ZIP     = "🗜";  LOG     = "📋";  EXPORT  = "📤";  IMPORT  = "📥";  COPY_IC = "📋"
    TAG     = "🏷";  CATEGORY= "📂";  WORLD   = "🌍";  PUBLIC  = "🌐";  PRIVATE = "🔏"
    AI      = "🧠";  ANALYZE = "🔬";  SCAN    = "🔭";  QUALITY = "⭐";  BUG     = "🐛"
    API_PR  = "🔐";  TOKEN_S = "🛡";  CLEAN   = "✨";  RISK    = "⚠️"
    # ─── PHP ───
    PHP     = "🐘";  PYTHON  = "🐍";  LANG    = "💬";  WEB     = "🌐";  SERVER2 = "🖥"
    # ─── الموافقة ───
    PENDING = "⏳";  APPROVE = "✅";  REJECT  = "❌";  REVIEW  = "🔎";  WAITING = "🕐"
    SAFE    = "🟢";  UNSAFE  = "🔴";  CAUTION = "🟡";  INSPECT = "🔍";  GUARD   = "🛡"
    # ─── زخرفية ───
    CROWN2  = "♛";  DIAMOND2= "♦";  STAR2   = "★";  FLOWER  = "❀";  SPARK   = "✦"

# ──────────────────────────────────────────────────────────────────────────────
# الأقسام المزخرفة (فواصل بصرية جميلة)
# ──────────────────────────────────────────────────────────────────────────────
SEP_MAIN   = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
SEP_THIN   = "┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈"
SEP_DOUBLE = "══════════════════════════════"
SEP_STAR   = "━━━━━━━━ ✦ ★ ✦ ━━━━━━━━"
SEP_ROYAL  = "───※ · ※───"
SEP_FANCY  = "𐄁𐄁𐄁𐄁𐄁𐄁𐄁𐄁𐄁𐄁𐄁𐄁𐄁𐄁𐄁𐄁𐄁𐄁𐄁𐄁"
SEP_CROWN  = "【 ✦═══════════════════✦ 】"

def hdr(title: str, icon: str = "✦") -> str:
    """رأس قسم مزخرف جميل"""
    return f"𓆩{icon}𓆪 <b>{title}</b>\n{SEP_MAIN}"

def hdr2(title: str) -> str:
    return f"╔══ {title} ══╗"

def footer_line() -> str:
    return SEP_MAIN

# ══════════════════════════════════════════════════════════════════════════════
# 🎨  نظام أزرار Inline Keyboard المحترف
# ══════════════════════════════════════════════════════════════════════════════

BUTTON_STYLES = ("success", "primary", "danger")

_EMOJI_RE = re.compile(
    "["
    "\U0001F1E6-\U0001F1FF"
    "\U0001F300-\U0001FAFF"
    "\U00002190-\U000021FF"
    "\U00002300-\U000023FF"
    "\U00002460-\U000024FF"
    "\U000025A0-\U000025FF"
    "\U00002600-\U000027BF"
    "\U00002B00-\U00002BFF"
    "\u200d\ufe0e\ufe0f"
    "]+",
    flags=re.UNICODE,
)

_DANGER_HINTS = (
    "حذف","إيقاف","ايقاف","حظر","إلغاء","الغاء","خصم","محظور",
    "خطر","إزالة","مسح","رفض","stop","del","delete","ban","remove",
    "cancel","danger","kill","block","bwords","stop_all","reject",
)
_SUCCESS_HINTS = (
    "تشغيل","تفعيل","تأكيد","نعم","إضافة","اضافة","رفع","شراء",
    "دعوة","ادع","تحققت","نسخة احتياطية","مشاركة","استرداد","حفظ",
    "قبول","منح","فك الحظر","run","play","add","buy","invite","backup",
    "share","confirm","redeem","save","unban","upload","grant","تحليل",
    "approve","موافقة","قبول",
)
_PRIMARY_HINTS = (
    "رجوع","الرئيسية","القائمة","لوحة","تفاصيل","معلومات","إحصائيات",
    "احصائيات","الملفات","ملفاتي","الإعدادات","الاعدادات","الدعم",
    "السجل","تحديث","بحث","عرض","تحميل","التالي","السابق","page",
    "menu","stats","settings","support","log","refresh","search","open",
    "download","files","user","info","about","noop","analyze","ai","pending",
)

_FALLBACK_LABELS: Dict[str, str] = {
    "del":"حذف","delete":"حذف","stop":"إيقاف","restart":"إعادة تشغيل",
    "run":"تشغيل","play":"تشغيل","log":"السجل","download":"تحميل",
    "zip":"تحميل ZIP","user":"المستخدم","open":"عرض",
    "back":"رجوع","cancel":"إلغاء","noop":"عرض","analyze":"تحليل AI",
    "approve":"موافقة","reject":"رفض","pending":"قيد المراجعة",
}


def _normalize_style(style: str) -> str:
    style = (style or "primary").lower().strip()
    return style if style in BUTTON_STYLES else "primary"


def _clean_button_label(label: str) -> str:
    label = str(label or "")
    label = re.sub(r"\s+", " ", label).strip(" ·|-–—")
    return label.strip() or "زر"


def _label_from_context(context_key: str) -> str:
    key = str(context_key or "").lower()
    for hint, fallback in _FALLBACK_LABELS.items():
        if hint in key:
            return fallback
    return "إجراء"


def _style_from_context(label: str, context_key: str = "", preferred: str = "primary") -> str:
    haystack = f"{label} {context_key}".lower()
    if any(h in haystack for h in _DANGER_HINTS):
        return "danger"
    if any(h in haystack for h in _SUCCESS_HINTS):
        return "success"
    if any(h in haystack for h in _PRIMARY_HINTS):
        return "primary"
    return _normalize_style(preferred)


def _styled_button(label: str, style: str = "primary", *,
                   callback_data: Optional[str] = None,
                   url: Optional[str] = None) -> InlineKeyboardButton:
    clean_label = _clean_button_label(label)
    if clean_label == "زر":
        clean_label = _label_from_context(callback_data or url or "")
    final_style = _normalize_style(style)
    kwargs: Dict[str, Any] = {"api_kwargs": {"style": final_style}}
    if url is not None:
        kwargs["url"] = url
    else:
        kwargs["callback_data"] = callback_data or "noop"
    return InlineKeyboardButton(clean_label, **kwargs)


def _button_style(button: InlineKeyboardButton) -> str:
    try:
        return _normalize_style((button.to_dict() or {}).get("style", "primary"))
    except Exception:
        return "primary"


def _ensure_button_style(button: InlineKeyboardButton, index: int) -> InlineKeyboardButton:
    try:
        existing_api = dict(getattr(button, "api_kwargs", None) or {})
        if existing_api.get("style") in BUTTON_STYLES:
            return button
        data = button.to_dict() or {}
    except Exception:
        return button
    if data.get("style") in BUTTON_STYLES:
        return button
    text = _clean_button_label(data.get("text", ""))
    cb   = str(data.get("callback_data") or data.get("url") or "")
    style = _style_from_context(text, cb, BUTTON_STYLES[index % len(BUTTON_STYLES)])
    data.pop("text", None)
    data.pop("style", None)
    existing_api["style"] = style
    try:
        return InlineKeyboardButton(text, api_kwargs=existing_api, **data)
    except Exception:
        return _styled_button(text, style, callback_data=cb or "noop")


def _normalize_keyboard_layout(rows: List[List[InlineKeyboardButton]]) -> List[List[InlineKeyboardButton]]:
    result: List[List[InlineKeyboardButton]] = []
    idx = 0
    for row in rows or []:
        new_row: List[InlineKeyboardButton] = []
        for button in row or []:
            new_row.append(_ensure_button_style(button, idx))
            idx += 1
        if new_row:
            result.append(new_row)
    return result


class InlineKeyboardMarkup(TelegramInlineKeyboardMarkup):
    """لوحة أزرار ذكية: تضيف style وتحافظ على التنسيق الأصلي للصفوف."""
    def __init__(self, inline_keyboard: List[List[InlineKeyboardButton]], *args, **kwargs):
        super().__init__(_normalize_keyboard_layout(inline_keyboard), *args, **kwargs)


def btn_success(label: str, cb: str)   -> InlineKeyboardButton: return _styled_button(label, "success", callback_data=cb)
def btn_primary(label: str, cb: str)   -> InlineKeyboardButton: return _styled_button(label, "primary", callback_data=cb)
def btn_danger(label: str, cb: str)    -> InlineKeyboardButton: return _styled_button(label, "danger",  callback_data=cb)
def btn_warning(label: str, cb: str)   -> InlineKeyboardButton: return _styled_button(label, "primary", callback_data=cb)
def btn_secondary(label: str, cb: str) -> InlineKeyboardButton: return _styled_button(label, "primary", callback_data=cb)
def btn_url_success(label: str, url: str) -> InlineKeyboardButton: return _styled_button(label, "success", url=url)
def btn_url_primary(label: str, url: str) -> InlineKeyboardButton: return _styled_button(label, "primary", url=url)
def btn_url_danger(label: str, url: str)  -> InlineKeyboardButton: return _styled_button(label, "danger",  url=url)
def btn_toggle(label: str, cb: str, active: bool) -> InlineKeyboardButton:
    return _styled_button(label, "success" if active else "danger", callback_data=cb)
def btn_noop(label: str) -> InlineKeyboardButton: return _styled_button(label, "primary", callback_data="noop")

# ══════════════════════════════════════════════════════════════════════════════
# 💾  نماذج البيانات
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class User:
    user_id: int
    username: str = ""
    first_name: str = ""
    last_name: str = ""
    points: int = 0
    free_uploads: int = 1
    total_uploads: int = 0
    total_downloads: int = 0
    total_runs: int = 0
    invited_users: List[int] = field(default_factory=list)
    invited_by: Optional[int] = None
    invite_reward_given_for: List[int] = field(default_factory=list)
    agreed_to_terms: bool = False
    is_banned: bool = False
    ban_reason: str = ""
    ban_until: str = ""
    is_premium: bool = False
    premium_until: str = ""
    premium_granted_by: int = 0
    join_date: str = ""
    last_active: str = ""
    files: List[str] = field(default_factory=list)
    settings: Dict[str, Any] = field(default_factory=dict)
    language: str = "ar"
    purchases_total_stars: int = 0
    notifications_enabled: bool = True
    is_admin: bool = False
    login_count: int = 0
    last_ip: str = ""
    tags: List[str] = field(default_factory=list)
    notes: str = ""
    rate_violations: int = 0
    total_points_earned: int = 0
    scheduled_runs: List[Dict[str, Any]] = field(default_factory=list)
    pending_uploads: List[str] = field(default_factory=list)
    total_python_files: int = 0
    total_php_files: int = 0
    access_unlocked: bool = False
    access_granted_by: int = 0
    access_granted_at: str = ""
    access_source: str = ""


@dataclass
class HostedFile:
    file_id: str
    file_name: str
    owner_id: int
    upload_date: str
    size: int = 0
    downloads: int = 0
    libraries: List[str] = field(default_factory=list)
    is_active: bool = True
    description: str = ""
    category: str = "general"
    process_id: Optional[int] = None
    run_count: int = 0
    last_run: str = ""
    last_stop: str = ""
    auto_restart: bool = False
    is_public: bool = False
    install_log: str = ""
    runtime_log: str = ""
    stored_path: str = ""
    entry_file: str = ""
    is_zip: bool = False
    tags: List[str] = field(default_factory=list)
    version: int = 1
    start_time: str = ""
    total_runtime_seconds: int = 0
    ai_analysis: str = ""
    file_type: str = "python"        # "python" | "php"
    php_version: str = ""
    approved_by: int = 0
    approved_at: str = ""
    security_score: int = 0
    security_notes: str = ""


@dataclass
class PendingUpload:
    pending_id: str
    file_name: str
    owner_id: int
    submitted_at: str
    size: int = 0
    stored_path: str = ""
    file_type: str = "python"        # "python" | "php"
    is_zip: bool = False
    ai_report: str = ""
    security_blocked: bool = False
    security_reasons: str = ""
    security_warnings: str = ""
    security_score: int = 0
    status: str = "pending"          # "pending" | "approved" | "rejected"
    reviewed_by: int = 0
    reviewed_at: str = ""
    reject_reason: str = ""
    description: str = ""
    libraries: List[str] = field(default_factory=list)


@dataclass
class Channel:
    chat_id: str
    title: str = ""
    invite_link: str = ""
    added_by: int = 0
    added_at: str = ""
    enabled: bool = True


@dataclass
class ScheduledTask:
    task_id: str
    file_id: str
    owner_id: int
    run_at: str
    repeat: str = "once"
    enabled: bool = True
    created_at: str = ""
    last_triggered: str = ""


# ══════════════════════════════════════════════════════════════════════════════
# 💾  قاعدة البيانات
# ══════════════════════════════════════════════════════════════════════════════

class Database:
    """قاعدة بيانات JSON مع قفل خيطي وحفظ تلقائي"""

    DEFAULT_SETTINGS: Dict[str, Any] = {
        "maintenance_mode": False,
        "require_subscription": True,
        "points_per_invite": 2,
        "upload_cost": 1,
        "stars_per_10_points": DEFAULT_STARS_PER_10_POINTS,
        "max_file_size_mb": MAX_FILE_SIZE_MB,
        "allowed_extensions": [".py", ".zip", ".php"],
        "welcome_message": "𓆩♛𓆪 أهلاً بك في PyHost Pro Ultra 𓆩♛𓆪\nأقوى بوت استضافة Python و PHP!",
        "bot_active": True,
        "auto_install_libs": True,
        "auto_run_after_upload": True,
        "auto_restart_default": False,
        "send_zip_if_run_fails": True,
        "strict_hosting_security": True,
        "ban_on_confirmed_danger": True,
        "max_processes_per_user": MAX_PROCESSES_PER_USER,
        "run_timeout_seconds": RUN_TIMEOUT_SECONDS,
        "first_upload_free": True,
        "broadcast_throttle_ms": 50,
        "log_runtime_lines": 300,
        "public_files_enabled": True,
        "support_username": SUPPORT_USERNAME,
        "stickers": dict(STICKERS),
        "notify_admin_on_join": True,
        "notify_admin_on_upload": True,
        "notify_admin_on_ban": True,
        "premium_upload_free": True,
        "premium_max_processes": 10,
        "rate_limit_enabled": True,
        "rate_limit_messages": RATE_LIMIT_MESSAGES,
        "rate_limit_window": RATE_LIMIT_WINDOW,
        "auto_cleanup_days": 30,
        "vip_mode_enabled": False,
        "leaderboard_enabled": True,
        "schedule_enabled": True,
        "admin_immortal": True,
        "ai_analysis_enabled": True,
        "api_protection_enabled": True,
        "require_admin_approval": True,    # نظام الموافقة
        "php_support_enabled": True,       # دعم PHP
        "php_executable": "php",           # مسار تنفيذ PHP
        "composer_path": "composer",       # مسار Composer
        "approval_notify_user": True,      # إشعار المستخدم بنتيجة المراجعة
        "auto_approve_safe_files": False,  # موافقة تلقائية للملفات الآمنة
        "max_pending_per_user": 5,         # أقصى ملفات معلقة للمستخدم
    }

    def __init__(self):
        self._lock = threading.RLock()
        self.users: Dict[int, User] = {}
        self.files: Dict[str, HostedFile] = {}
        self.channels: Dict[str, Channel] = {}
        self.settings: Dict[str, Any] = dict(self.DEFAULT_SETTINGS)
        self.stats: Dict[str, Any] = {}
        self.promo_codes: Dict[str, Any] = {}
        self.pending_payments: Dict[int, Any] = {}
        self.broadcast_history: List[Dict[str, Any]] = []
        self.banned_words: List[str] = []
        self.security_events: List[Dict[str, Any]] = []
        self.activity_log: List[Dict[str, Any]] = []
        self.scheduled_tasks: Dict[str, ScheduledTask] = {}
        self.pending_uploads: Dict[str, PendingUpload] = {}   # نظام الموافقة
        self._dirty = False
        self._last_save = 0.0
        self.load()

    # ─── تحميل وحفظ ───────────────────────────────────────────────────────
    def load(self) -> None:
        with self._lock:
            if not os.path.exists(DATABASE_FILE):
                self.stats = {"created_at": now_iso()}
                self.save(force=True)
                return
            try:
                with open(DATABASE_FILE, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                for uid_s, ud in raw.get("users", {}).items():
                    try:
                        u = User(**{k: v for k, v in ud.items() if k in User.__dataclass_fields__})
                        self.users[int(uid_s)] = u
                    except Exception as e:
                        logger.warning("خطأ تحميل مستخدم %s: %s", uid_s, e)
                for fid, fd in raw.get("files", {}).items():
                    try:
                        f = HostedFile(**{k: v for k, v in fd.items() if k in HostedFile.__dataclass_fields__})
                        self.files[fid] = f
                    except Exception as e:
                        logger.warning("خطأ تحميل ملف %s: %s", fid, e)
                for cid, cd in raw.get("channels", {}).items():
                    try:
                        self.channels[cid] = Channel(**{k: v for k, v in cd.items() if k in Channel.__dataclass_fields__})
                    except: pass
                for tid, td in raw.get("scheduled_tasks", {}).items():
                    try:
                        self.scheduled_tasks[tid] = ScheduledTask(**{k: v for k, v in td.items() if k in ScheduledTask.__dataclass_fields__})
                    except: pass
                for pid, pd in raw.get("pending_uploads", {}).items():
                    try:
                        self.pending_uploads[pid] = PendingUpload(**{k: v for k, v in pd.items() if k in PendingUpload.__dataclass_fields__})
                    except: pass
                s = raw.get("settings", {})
                for k, v in self.DEFAULT_SETTINGS.items():
                    if k not in s:
                        s[k] = v
                self.settings           = s
                self.stats              = raw.get("stats", {"created_at": now_iso()})
                self.promo_codes        = raw.get("promo_codes", {})
                self.pending_payments   = {int(k): v for k, v in raw.get("pending_payments", {}).items()}
                self.broadcast_history  = raw.get("broadcast_history", [])
                self.banned_words       = raw.get("banned_words", [])
                self.security_events    = raw.get("security_events", [])
                self.activity_log       = raw.get("activity_log", [])
            except Exception as e:
                logger.error("فشل تحميل قاعدة البيانات: %s", e)

    def save(self, force: bool = False) -> None:
        now = time.time()
        if not force and not self._dirty and now - self._last_save < 5:
            return
        with self._lock:
            try:
                data = {
                    "users":           {str(uid): asdict(u) for uid, u in self.users.items()},
                    "files":           {fid: asdict(f) for fid, f in self.files.items()},
                    "channels":        {cid: asdict(c) for cid, c in self.channels.items()},
                    "scheduled_tasks": {tid: asdict(t) for tid, t in self.scheduled_tasks.items()},
                    "pending_uploads": {pid: asdict(p) for pid, p in self.pending_uploads.items()},
                    "settings":        self.settings,
                    "stats":           self.stats,
                    "promo_codes":     self.promo_codes,
                    "pending_payments":{str(k): v for k, v in self.pending_payments.items()},
                    "broadcast_history": self.broadcast_history,
                    "banned_words":    self.banned_words,
                    "security_events": self.security_events[-500:],
                    "activity_log":    self.activity_log[-1000:],
                }
                tmp = DATABASE_FILE + ".tmp"
                with open(tmp, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2, default=str)
                os.replace(tmp, DATABASE_FILE)
                self._dirty = False
                self._last_save = now
            except Exception as e:
                logger.error("فشل حفظ قاعدة البيانات: %s", e)

    # ─── المستخدمون ───────────────────────────────────────────────────────
    def get_user(self, user_id: int, *, username: str = "",
                 first_name: str = "", last_name: str = "") -> "User":
        with self._lock:
            if user_id not in self.users:
                u = User(
                    user_id=user_id, username=username,
                    first_name=first_name, last_name=last_name,
                    join_date=now_iso(), last_active=now_iso(),
                    is_admin=(user_id in ADMIN_IDS),
                )
                self.users[user_id] = u
                self._dirty = True
            else:
                u = self.users[user_id]
                if username:   u.username   = username
                if first_name: u.first_name = first_name
                if last_name:  u.last_name  = last_name
                u.last_active = now_iso()
                u.is_admin    = (user_id in ADMIN_IDS)
                self._dirty   = True
            return u

    def update_user(self, u: "User", save: bool = True) -> None:
        with self._lock:
            self.users[u.user_id] = u
            self._dirty = True
            if save: self.save()

    def all_users(self) -> List["User"]:
        return list(self.users.values())

    def get_premium_users(self) -> List["User"]:
        now = now_iso()
        out = []
        for u in self.users.values():
            if u.is_premium:
                if u.premium_until and u.premium_until < now:
                    u.is_premium = False; u.premium_until = ""
                    self._dirty = True
                else:
                    out.append(u)
        return out

    def get_new_users(self, days: int = 7) -> List["User"]:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        return [u for u in self.users.values() if u.join_date >= cutoff]

    def record_daily_active(self, user_id: int) -> None:
        today = datetime.now().strftime("%Y-%m-%d")
        da    = self.stats.setdefault("daily_active", {})
        da.setdefault(today, [])
        if user_id not in da[today]:
            da[today].append(user_id)
        self._dirty = True

    # ─── الملفات ──────────────────────────────────────────────────────────
    def get_file(self, file_id: str) -> Optional["HostedFile"]:
        return self.files.get(file_id)

    def add_file(self, hf: "HostedFile") -> None:
        with self._lock:
            self.files[hf.file_id] = hf
            self._dirty = True

    def remove_file(self, file_id: str) -> None:
        with self._lock:
            self.files.pop(file_id, None)
            for u in self.users.values():
                if file_id in u.files:
                    u.files.remove(file_id)
            self._dirty = True
            self.save()

    def user_files(self, user_id: int) -> List["HostedFile"]:
        return [self.files[fid] for fid in self.users.get(user_id, User(0)).files if fid in self.files]

    def all_files_sorted(self) -> List["HostedFile"]:
        return sorted(self.files.values(), key=lambda x: x.upload_date, reverse=True)

    # ─── الملفات المعلقة (نظام الموافقة) ─────────────────────────────────
    def add_pending(self, pu: "PendingUpload") -> None:
        with self._lock:
            self.pending_uploads[pu.pending_id] = pu
            u = self.users.get(pu.owner_id)
            if u and pu.pending_id not in u.pending_uploads:
                u.pending_uploads.append(pu.pending_id)
            self._dirty = True

    def get_pending(self, pending_id: str) -> Optional["PendingUpload"]:
        return self.pending_uploads.get(pending_id)

    def remove_pending(self, pending_id: str) -> None:
        with self._lock:
            pu = self.pending_uploads.pop(pending_id, None)
            if pu:
                u = self.users.get(pu.owner_id)
                if u and pending_id in u.pending_uploads:
                    u.pending_uploads.remove(pending_id)
            self._dirty = True
            self.save()

    def all_pending(self, status: str = "pending") -> List["PendingUpload"]:
        return [pu for pu in self.pending_uploads.values() if pu.status == status]

    def user_pending_count(self, user_id: int) -> int:
        return sum(1 for pu in self.pending_uploads.values()
                   if pu.owner_id == user_id and pu.status == "pending")

    # ─── القنوات ──────────────────────────────────────────────────────────
    def all_channels(self, enabled_only: bool = False) -> List["Channel"]:
        chs = list(self.channels.values())
        return [c for c in chs if c.enabled] if enabled_only else chs

    def add_channel(self, ch: "Channel") -> None:
        with self._lock:
            self.channels[ch.chat_id] = ch
            self._dirty = True
            self.save()

    def remove_channel(self, chat_id: str) -> None:
        with self._lock:
            self.channels.pop(chat_id, None)
            self._dirty = True
            self.save()

    # ─── سجل النشاط ────────────────────────────────────────────────────
    def log_activity(self, action: str, user_id: int = 0, detail: str = "") -> None:
        self.activity_log.append({"action": action, "user_id": user_id,
                                   "detail": detail, "at": now_iso()})
        if len(self.activity_log) > 2000:
            self.activity_log = self.activity_log[-1000:]
        self._dirty = True

    def log_security(self, user_id: int, file_name: str,
                     reasons: List[str], banned: bool) -> None:
        self.security_events.append({
            "user_id": user_id, "file": file_name,
            "reasons": reasons, "banned": banned, "at": now_iso(),
        })
        self._dirty = True


# مثيل قاعدة البيانات العالمي
db = Database()


# ══════════════════════════════════════════════════════════════════════════════
# 🔧  دوال مساعدة عامة
# ══════════════════════════════════════════════════════════════════════════════

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def escape_html(text: str) -> str:
    return html.escape(str(text or ""), quote=False)


def shorten(text: str, max_len: int = 30) -> str:
    text = str(text or "")
    return text if len(text) <= max_len else text[:max_len - 1] + "…"


def format_size(size_bytes: int) -> str:
    if size_bytes < 1024:       return f"{size_bytes} B"
    if size_bytes < 1024**2:    return f"{size_bytes/1024:.1f} KB"
    if size_bytes < 1024**3:    return f"{size_bytes/1024**2:.1f} MB"
    return f"{size_bytes/1024**3:.2f} GB"


def format_dt(iso: str) -> str:
    if not iso: return "—"
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M")
    except: return iso[:16]


def humanize_delta(iso: str) -> str:
    if not iso: return "—"
    try:
        dt   = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        diff = datetime.now(timezone.utc) - dt
        s    = int(diff.total_seconds())
        if s < 60:   return f"منذ {s} ثانية"
        if s < 3600: return f"منذ {s//60} دقيقة"
        if s < 86400:return f"منذ {s//3600} ساعة"
        return f"منذ {s//86400} يوم"
    except: return "—"


def progress_bar(pct: int, width: int = 10) -> str:
    filled = int(width * max(0, min(100, pct)) / 100)
    return "█" * filled + "░" * (width - filled)


def make_zip_of_dir(src_dir: str, out_path: str) -> None:
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(src_dir):
            for fn in files:
                full = os.path.join(root, fn)
                arc  = os.path.relpath(full, src_dir)
                zf.write(full, arc)


def write_requirements(work_dir: str, libs: List[str]) -> None:
    path = os.path.join(work_dir, "requirements.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(libs) + "\n")


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


def is_admin_immortal(user_id: int) -> bool:
    return is_admin(user_id) and bool(db.settings.get("admin_immortal", True))


def grant_points(u: "User", pts: int, source: str = "", note: str = "") -> None:
    u.points             += pts
    u.total_points_earned += max(0, pts)
    db.stats["total_points_given"] = db.stats.get("total_points_given", 0) + max(0, pts)
    db.log_activity("grant_points", u.user_id, f"+{pts} {source} {note}")
    db._dirty = True


def detect_php() -> bool:
    try:
        r = subprocess.run(["php", "--version"], capture_output=True, timeout=5)
        return r.returncode == 0
    except: return False


def detect_python_version() -> str:
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


# ══════════════════════════════════════════════════════════════════════════════
# 📡  مراقب الموارد
# ══════════════════════════════════════════════════════════════════════════════

class ResourceMonitor:
    """يراقب CPU / RAM / Disk في الخلفية"""

    def __init__(self):
        self._cpu  = 0.0
        self._ram  = 0.0
        self._disk = 0.0
        self._lock = threading.Lock()
        self._running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        while self._running:
            try:
                import psutil
                with self._lock:
                    self._cpu  = psutil.cpu_percent(interval=1)
                    mem        = psutil.virtual_memory()
                    self._ram  = mem.percent
                    disk       = psutil.disk_usage(".")
                    self._disk = disk.percent
            except ImportError:
                with self._lock:
                    self._cpu = self._ram = self._disk = -1
                break
            except Exception:
                pass
            time.sleep(5)

    @property
    def cpu(self)  -> float: return self._cpu
    @property
    def ram(self)  -> float: return self._ram
    @property
    def disk(self) -> float: return self._disk

    def summary_text(self) -> str:
        if self._cpu < 0:
            return f"{Icon.CPU} موارد النظام غير متاحة (psutil غير مثبت)"
        bar_c = progress_bar(int(self._cpu),  8)
        bar_r = progress_bar(int(self._ram),  8)
        bar_d = progress_bar(int(self._disk), 8)
        return (
            f"{Icon.CPU}  CPU:  {bar_c} {self._cpu:.1f}%\n"
            f"{Icon.MEMORY} RAM:  {bar_r} {self._ram:.1f}%\n"
            f"{Icon.DISK}  Disk: {bar_d} {self._disk:.1f}%"
        )

    def stop(self): self._running = False


res_monitor = ResourceMonitor()


# ══════════════════════════════════════════════════════════════════════════════
# 🏃  مدير العمليات
# ══════════════════════════════════════════════════════════════════════════════

class ProcessManager:
    """يدير تشغيل ملفات Python و PHP"""

    def __init__(self):
        self._procs: Dict[str, subprocess.Popen] = {}
        self._logs:  Dict[str, deque]             = {}
        self._lock   = threading.Lock()
        self._start_times: Dict[str, float]       = {}

    # ─── تشغيل ────────────────────────────────────────────────────────────
    def run(self, file_id: str, cmd: List[str], cwd: str,
            env: Optional[Dict[str, str]] = None,
            timeout: int = 0) -> Tuple[bool, str]:
        with self._lock:
            if file_id in self._procs:
                p = self._procs[file_id]
                if p.poll() is None:
                    return False, "العملية تعمل بالفعل"
                self._cleanup(file_id)

            max_procs = int(db.settings.get("max_processes_per_user", MAX_PROCESSES_PER_USER))
            hf        = db.get_file(file_id)
            owner_id  = hf.owner_id if hf else 0
            if owner_id:
                u    = db.users.get(owner_id)
                prem = u.is_premium if u else False
                if prem:
                    max_procs = int(db.settings.get("premium_max_processes", 10))
                running_for_owner = sum(
                    1 for fid, p2 in self._procs.items()
                    if p2.poll() is None and db.get_file(fid) and db.get_file(fid).owner_id == owner_id
                )
                if running_for_owner >= max_procs:
                    return False, f"وصلت للحد الأقصى ({max_procs} عملية). أوقف عملية أولاً."

            # منع تشغيل أي ملف يستخدم توكن البوت الرئيسي حتى لا يحصل تضارب getUpdates مهما حصل محلياً
            if BOT_TOKEN and _tree_contains_token(cwd, BOT_TOKEN):
                return False, "🚫 ممنوع تشغيل ملف يحتوي توكن البوت الرئيسي — تم منعه لمنع التضارب."
            _kill_local_token_conflicts("قبل تشغيل ملف مستضاف")

            self._logs[file_id] = deque(maxlen=int(db.settings.get("log_runtime_lines", 300)))
            run_env = os.environ.copy()
            if env: run_env.update(env)
            try:
                proc = subprocess.Popen(
                    cmd, cwd=cwd, env=run_env,
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    text=True, encoding="utf-8", errors="replace",
                    preexec_fn=os.setsid if hasattr(os, "setsid") else None,
                )
                self._procs[file_id]       = proc
                self._start_times[file_id] = time.time()
                self._start_log_reader(file_id, proc)
                if timeout > 0:
                    threading.Thread(target=self._timeout_watcher,
                                     args=(file_id, proc, timeout), daemon=True).start()
                return True, f"PID={proc.pid}"
            except Exception as e:
                return False, str(e)

    def _start_log_reader(self, file_id: str, proc: subprocess.Popen) -> None:
        def _reader():
            try:
                for line in iter(proc.stdout.readline, ""):
                    if not line: break
                    ts = datetime.now().strftime("%H:%M:%S")
                    with self._lock:
                        if file_id in self._logs:
                            self._logs[file_id].append(f"[{ts}] {line.rstrip()}")
                    hf = db.get_file(file_id)
                    if hf:
                        hf.runtime_log = "\n".join(list(self._logs[file_id])[-50:])
                        db._dirty = True
            except: pass
            finally:
                proc.stdout.close()
                with self._lock:
                    if file_id in self._procs and self._procs[file_id] == proc:
                        hf = db.get_file(file_id)
                        if hf:
                            hf.process_id = None
                            if file_id in self._start_times:
                                hf.total_runtime_seconds += int(time.time() - self._start_times[file_id])
                            db.add_file(hf)
                            if hf.auto_restart and proc.returncode != 0:
                                logger.info("إعادة تشغيل تلقائية لـ %s", file_id)
                                self.restart(file_id)
        threading.Thread(target=_reader, daemon=True).start()

    def _timeout_watcher(self, file_id: str, proc: subprocess.Popen, timeout: int) -> None:
        end = time.time() + timeout
        while time.time() < end:
            if proc.poll() is not None: return
            time.sleep(1)
        self.stop(file_id)
        with self._lock:
            if file_id in self._logs:
                self._logs[file_id].append(f"[SYS] انتهت المهلة ({timeout}ث) — أُوقفت العملية")

    def _cleanup(self, file_id: str) -> None:
        self._procs.pop(file_id, None)
        self._start_times.pop(file_id, None)

    # ─── إيقاف ────────────────────────────────────────────────────────────
    def stop(self, file_id: str) -> bool:
        with self._lock:
            proc = self._procs.get(file_id)
            if not proc: return False
            try:
                if hasattr(os, "killpg"):
                    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                else:
                    proc.terminate()
                try: proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    if hasattr(os, "killpg"):
                        try: os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                        except: pass
                    else: proc.kill()
            except: pass
            self._cleanup(file_id)
            hf = db.get_file(file_id)
            if hf:
                hf.process_id = None
                hf.last_stop  = now_iso()
                if file_id in self._start_times:
                    hf.total_runtime_seconds += int(time.time() - self._start_times.get(file_id, time.time()))
                db.add_file(hf)
            return True

    def stop_all(self) -> int:
        fids = list(self._procs.keys())
        cnt  = 0
        for fid in fids:
            if self.stop(fid): cnt += 1
        return cnt

    def restart(self, file_id: str) -> Tuple[bool, str]:
        hf = db.get_file(file_id)
        if not hf: return False, "الملف غير موجود"
        self.stop(file_id)
        time.sleep(0.5)
        return self._run_hosted_file(hf)

    def _run_hosted_file(self, hf: "HostedFile") -> Tuple[bool, str]:
        work_dir   = os.path.dirname(hf.stored_path) if hf.stored_path else os.path.join(FILES_DIR, hf.file_id)
        entry      = hf.entry_file or hf.file_name
        entry_path = os.path.join(work_dir, entry).replace('hosted_files/' + hf.file_id + '/hosted_files/' + hf.file_id, 'hosted_files/' + hf.file_id)
        if not os.path.exists(entry_path):
            return False, f"ملف الدخول غير موجود: {entry}"
        timeout = int(db.settings.get("run_timeout_seconds", 0))
        if hf.file_type == "php":
            php_exe = db.settings.get("php_executable", "php")
            cmd = [php_exe, os.path.abspath(entry_path).replace('hosted_files/' + hf.file_id + '/hosted_files/' + hf.file_id, 'hosted_files/' + hf.file_id)]
        else:
            cmd = [sys.executable, "-u", os.path.abspath(entry_path).replace('hosted_files/' + hf.file_id + '/hosted_files/' + hf.file_id, 'hosted_files/' + hf.file_id)]
        work_dir_fixed = os.path.abspath(work_dir).replace('hosted_files/' + hf.file_id + '/hosted_files/' + hf.file_id, 'hosted_files/' + hf.file_id)
        return self.run(hf.file_id, cmd, work_dir_fixed, timeout=timeout)

    # ─── استعلامات ────────────────────────────────────────────────────────
    def is_running(self, file_id: str) -> bool:
        with self._lock:
            p = self._procs.get(file_id)
            return p is not None and p.poll() is None

    def pid(self, file_id: str) -> Optional[int]:
        with self._lock:
            p = self._procs.get(file_id)
            return p.pid if p and p.poll() is None else None

    def all_running(self) -> List[str]:
        with self._lock:
            return [fid for fid, p in self._procs.items() if p.poll() is None]

    def tail_log(self, file_id: str, n: int = 50) -> str:
        with self._lock:
            dq = self._logs.get(file_id)
            if not dq: return ""
            lines = list(dq)[-n:]
        return "\n".join(lines)

    def export_log(self, file_id: str) -> bytes:
        with self._lock:
            dq = self._logs.get(file_id)
            lines = list(dq) if dq else []
        return "\n".join(lines).encode("utf-8", errors="replace")

    def uptime(self, file_id: str) -> str:
        st = self._start_times.get(file_id)
        if not st: return "—"
        s = int(time.time() - st)
        h, r = divmod(s, 3600); m, s2 = divmod(r, 60)
        return f"{h}س {m}د {s2}ث"

    def install_libs(self, libs: List[str], work_dir: str) -> Tuple[bool, str]:
        if not libs: return True, "لا توجد مكتبات"
        write_requirements(work_dir, libs)
        req_file = os.path.join(work_dir, "requirements.txt")
        try:
            r = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", req_file, "--quiet"],
                capture_output=True, text=True, timeout=INSTALL_TIMEOUT_SECONDS,
                encoding="utf-8", errors="replace",
            )
            return r.returncode == 0, (r.stdout + r.stderr)[-3000:]
        except subprocess.TimeoutExpired:
            return False, "انتهت مهلة التثبيت"
        except Exception as e:
            return False, str(e)

    def install_composer(self, work_dir: str) -> Tuple[bool, str]:
        """تثبيت حزم PHP عبر Composer"""
        composer_json = os.path.join(work_dir, "composer.json")
        if not os.path.exists(composer_json):
            return True, "لا يوجد composer.json"
        composer = db.settings.get("composer_path", "composer")
        try:
            r = subprocess.run(
                [composer, "install", "--no-interaction", "--prefer-dist"],
                capture_output=True, text=True, timeout=INSTALL_TIMEOUT_SECONDS,
                cwd=work_dir, encoding="utf-8", errors="replace",
            )
            return r.returncode == 0, (r.stdout + r.stderr)[-3000:]
        except Exception as e:
            return False, str(e)


pm = ProcessManager()


# ══════════════════════════════════════════════════════════════════════════════
# 🛡  حماية Rate Limiting
# ══════════════════════════════════════════════════════════════════════════════

class RateLimiter:
    def __init__(self):
        self._data: Dict[int, deque] = defaultdict(lambda: deque())
        self._lock = threading.Lock()

    def check(self, user_id: int) -> bool:
        if not db.settings.get("rate_limit_enabled", True): return True
        if is_admin(user_id): return True
        limit  = int(db.settings.get("rate_limit_messages", RATE_LIMIT_MESSAGES))
        window = int(db.settings.get("rate_limit_window",   RATE_LIMIT_WINDOW))
        now    = time.time()
        with self._lock:
            dq = self._data[user_id]
            while dq and dq[0] < now - window:
                dq.popleft()
            if len(dq) >= limit:
                return False
            dq.append(now)
            return True


rate_limiter = RateLimiter()


# ══════════════════════════════════════════════════════════════════════════════
# 🔍  محرك تحليل AI
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class AIAnalysisResult:
    lines_of_code: int   = 0
    functions_count: int = 0
    classes_count: int   = 0
    libraries_count: int = 0
    has_async: bool      = False
    has_error_handling: bool = False
    has_logging: bool    = False
    has_config: bool     = False
    has_main: bool       = False
    is_bot: bool         = False
    code_type: str       = "مجهول"
    bot_framework: str   = ""
    complexity: str      = "بسيط"
    quality_score: int   = 50
    security_risk: str   = "منخفض"
    potential_issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    security_notes: List[str]  = field(default_factory=list)
    api_calls: List[str]       = field(default_factory=list)
    summary: str               = ""
    file_type: str             = "python"   # "python" | "php"


class AICodeAnalyzer:
    """محرك تحليل الذكاء الاصطناعي للكود (Python + PHP)"""

    BOT_FRAMEWORKS = {"telegram", "pyrogram", "aiogram", "telebot", "discord", "slack_bolt"}
    WEB_FRAMEWORKS = {"flask", "django", "fastapi", "starlette", "aiohttp", "tornado", "sanic"}
    DATA_LIBS      = {"pandas", "numpy", "scipy", "matplotlib", "sklearn", "tensorflow", "torch"}
    PHP_FRAMEWORKS = {"laravel", "symfony", "codeigniter", "yii", "slim", "lumen"}

    QUALITY_POSITIVE: List[Tuple[str, int, str]] = [
        (r"try\s*[:({]", 5, "معالجة الأخطاء"),
        (r"logging\.|logger\.", 4, "تسجيل الأحداث"),
        (r"os\.getenv|os\.environ", 3, "متغيرات البيئة"),
        (r"if __name__\s*==\s*[\"']__main__[\"']", 4, "نقطة دخول"),
        (r"async\s+def|await\s+", 3, "برمجة غير متزامنة"),
        (r"unittest|pytest|test_", 5, "اختبارات وحدة"),
        (r"type\s+hints|:\s*(str|int|bool|float|list|dict|Optional|List)", 2, "تلميحات الأنواع"),
        (r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'', 2, "توثيق الكود"),
        (r"class\s+\w+", 3, "برمجة كائنية"),
    ]

    QUALITY_NEGATIVE: List[Tuple[str, int, str]] = [
        (r"print\s*\(", -1, "يستخدم print بدل logging"),
        (r"bare\s+except|except\s*:", -3, "except فارغة"),
        (r"TODO|FIXME|HACK|XXX", -2, "كود غير مكتمل"),
        (r"time\.sleep\s*\(\s*[5-9]\d*\.", -2, "تأخير طويل"),
        (r"global\s+\w+", -2, "متغيرات عامة"),
    ]

    API_PATTERNS: List[Tuple[str, str]] = [
        (r"requests\.|aiohttp\.|httpx\.",     "HTTP Client"),
        (r"flask\.|fastapi\.|django\.",        "Web Framework"),
        (r"pandas\.|numpy\.",                  "Data Science"),
        (r"telegram\.|pyrogram\.|aiogram\.",   "Telegram Bot"),
        (r"discord\.",                         "Discord Bot"),
        (r"sqlite3\.|psycopg2\.|motor\.",      "Database"),
        (r"redis\.",                           "Redis"),
        (r"boto3\.",                           "AWS SDK"),
        (r"openai\.|anthropic\.",              "AI API"),
    ]

    PHP_QUALITY_POSITIVE: List[Tuple[str, int, str]] = [
        (r"try\s*\{", 5, "معالجة الأخطاء"),
        (r"class\s+\w+", 4, "برمجة كائنية"),
        (r"namespace\s+", 3, "استخدام Namespaces"),
        (r"use\s+\w+", 2, "استخدام Imports"),
        (r"function\s+\w+\s*\(", 3, "دوال منظمة"),
        (r"//|/\*|\*", 1, "تعليقات"),
        (r"PDO|mysqli", 4, "قواعد بيانات آمنة"),
        (r"htmlspecialchars|filter_input|prepared\s+statement", 5, "حماية XSS/SQL"),
    ]

    PHP_QUALITY_NEGATIVE: List[Tuple[str, int, str]] = [
        (r"mysql_query|mysql_connect", -8, "دوال MySQL قديمة ومهجورة"),
        (r"eval\s*\(", -10, "استخدام eval خطير"),
        (r'\$_GET|\$_POST|\$_REQUEST', -2, "بيانات مستخدم غير محققة"),
        (r"shell_exec|system\s*\(|exec\s*\(|passthru", -8, "تنفيذ أوامر نظام"),
    ]

    @classmethod
    def analyze_source(cls, source: str, filename: str = "") -> AIAnalysisResult:
        result      = AIAnalysisResult()
        result.lines_of_code = len(source.splitlines())

        ext = os.path.splitext(filename.lower())[1] if filename else ""
        if ext == ".php" or (not ext and "<?php" in source[:100]):
            result.file_type = "php"
            return cls._analyze_php(source, filename, result)
        else:
            result.file_type = "python"
            return cls._analyze_python(source, filename, result)

    @classmethod
    def _analyze_python(cls, source: str, filename: str, result: AIAnalysisResult) -> AIAnalysisResult:
        try:
            tree    = ast.parse(source)
            imports = cls._extract_imports(tree)
            result.libraries_count = len(imports)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    result.functions_count += 1
                    if isinstance(node, ast.AsyncFunctionDef):
                        result.has_async = True
                elif isinstance(node, ast.ClassDef):
                    result.classes_count += 1
            code_type, bot_fw = cls._detect_code_type(source, imports)
            result.code_type     = code_type
            result.bot_framework = bot_fw
            result.is_bot        = any(fw in imports for fw in cls.BOT_FRAMEWORKS)
        except SyntaxError as e:
            result.potential_issues.append(f"خطأ في بناء الجملة: {e}")
        except: pass

        score = 50
        for pattern, pts, label in cls.QUALITY_POSITIVE:
            if re.search(pattern, source, re.M):
                score += pts
                if pts >= 3: result.recommendations.append(f"ممتاز: {label}")
        for pattern, pts, label in cls.QUALITY_NEGATIVE:
            if re.search(pattern, source, re.M):
                score += pts
                result.potential_issues.append(label)

        result.has_main           = bool(re.search(r"if __name__\s*==\s*[\"']__main__[\"']", source))
        result.has_error_handling = bool(re.search(r"try\s*:", source))
        result.has_logging        = bool(re.search(r"logging\.|logger\.", source))
        result.has_config         = bool(re.search(r"os\.getenv|os\.environ|\.env", source))

        for pattern, name in cls.API_PATTERNS:
            if re.search(pattern, source):
                result.api_calls.append(name)

        if result.lines_of_code < 50:    result.complexity = "بسيط"
        elif result.lines_of_code < 200: result.complexity = "متوسط"
        elif result.lines_of_code < 500: result.complexity = "متقدم"
        else:                             result.complexity = "ضخم"

        score += min(result.functions_count * 2, 15)
        score += min(result.classes_count * 3, 12)
        if result.has_async:    score += 5
        if result.has_logging:  score += 5
        if result.has_config:   score += 3
        if result.has_main:     score += 5
        result.quality_score = max(0, min(100, score))

        if not result.has_error_handling:
            result.recommendations.append("أضف try/except لمعالجة الأخطاء")
        if not result.has_logging:
            result.recommendations.append("استخدم logging بدلاً من print")
        if not result.has_config:
            result.recommendations.append("استخدم os.getenv لمتغيرات الإعداد")
        if not result.has_main and result.lines_of_code > 20:
            result.recommendations.append("أضف if __name__ == '__main__'")

        if re.search(r"eval\s*\(|exec\s*\(", source):
            result.security_notes.append("تجنب eval/exec — خطر أمني عالي")
        if re.search(r"BOT_TOKEN\s*=\s*['\"][0-9A-Za-z:_-]{20,}", source):
            result.security_notes.append("لا تضع التوكن مباشرة — استخدم .env")
        if re.search(r"os\.system\s*\(", source):
            result.security_notes.append("os.system خطر — استخدم subprocess بأمان")

        quality_label = ("ممتاز" if result.quality_score >= 80 else
                         "جيد"   if result.quality_score >= 60 else
                         "مقبول" if result.quality_score >= 40 else "يحتاج تحسين")
        result.summary = (
            f"Python {result.code_type} بجودة {quality_label} ({result.quality_score}/100). "
            f"{result.lines_of_code} سطر، {result.functions_count} دالة، "
            f"{result.classes_count} كلاس، {result.libraries_count} مكتبة."
        )
        return result

    @classmethod
    def _analyze_php(cls, source: str, filename: str, result: AIAnalysisResult) -> AIAnalysisResult:
        result.code_type = "PHP Script"
        # كشف Framework
        for fw in cls.PHP_FRAMEWORKS:
            if fw.lower() in source.lower():
                result.code_type = f"PHP {fw.capitalize()} App"
                break

        result.functions_count = len(re.findall(r"function\s+\w+\s*\(", source))
        result.classes_count   = len(re.findall(r"class\s+\w+", source))
        result.has_error_handling = bool(re.search(r"try\s*\{", source))
        result.has_logging        = bool(re.search(r"error_log|Logger|monolog", source))

        score = 50
        for pattern, pts, label in cls.PHP_QUALITY_POSITIVE:
            if re.search(pattern, source):
                score += pts
                if pts >= 4: result.recommendations.append(f"ممتاز: {label}")
        for pattern, pts, label in cls.PHP_QUALITY_NEGATIVE:
            if re.search(pattern, source):
                score += pts
                result.potential_issues.append(label)

        if result.lines_of_code < 50:    result.complexity = "بسيط"
        elif result.lines_of_code < 300: result.complexity = "متوسط"
        elif result.lines_of_code < 800: result.complexity = "متقدم"
        else:                             result.complexity = "ضخم"

        score += min(result.functions_count * 2, 15)
        score += min(result.classes_count * 3, 12)
        result.quality_score = max(0, min(100, score))

        if re.search(r"eval\s*\(", source):
            result.security_notes.append("eval() في PHP خطر أمني عالي جداً")
        if re.search(r"shell_exec|system\s*\(|exec\s*\(|passthru", source):
            result.security_notes.append("تنفيذ أوامر نظام — خطر أمني")
        if re.search(r"\$_GET|\$_POST|\$_REQUEST", source) and not re.search(r"htmlspecialchars|filter_input|strip_tags", source):
            result.security_notes.append("بيانات مدخلات غير محققة — خطر XSS")
        if re.search(r"mysql_query|mysql_connect", source):
            result.security_notes.append("دوال MySQL قديمة ومهجورة — استخدم PDO")

        quality_label = ("ممتاز" if result.quality_score >= 80 else
                         "جيد"   if result.quality_score >= 60 else
                         "مقبول" if result.quality_score >= 40 else "يحتاج تحسين")
        result.summary = (
            f"{result.code_type} بجودة {quality_label} ({result.quality_score}/100). "
            f"{result.lines_of_code} سطر، {result.functions_count} دالة، "
            f"{result.classes_count} كلاس."
        )
        return result

    @classmethod
    def _extract_imports(cls, tree: ast.AST) -> Set[str]:
        imports: Set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split(".")[0])
        return imports

    @classmethod
    def _detect_code_type(cls, source: str, imports: Set[str]) -> Tuple[str, str]:
        for fw in cls.BOT_FRAMEWORKS:
            if fw in imports:
                return f"Bot ({fw})", fw
        for fw in cls.WEB_FRAMEWORKS:
            if fw in imports:
                return f"Web App ({fw})", fw
        for lib in cls.DATA_LIBS:
            if lib in imports:
                return f"Data Science ({lib})", ""
        if "tkinter" in imports or "PyQt5" in imports or "wx" in imports:
            return "Desktop App", ""
        if "asyncio" in imports: return "Async Script", ""
        return "Python Script", ""

    @classmethod
    def analyze_file(cls, path: str) -> AIAnalysisResult:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return cls.analyze_source(f.read(), os.path.basename(path))
        except Exception as e:
            r = AIAnalysisResult()
            r.potential_issues.append(f"تعذر تحليل الملف: {e}")
            return r

    @classmethod
    def analyze_directory(cls, dir_path: str) -> AIAnalysisResult:
        py_files  = []
        php_files = []
        for root, _, files in os.walk(dir_path):
            for fn in files:
                fp = os.path.join(root, fn)
                if fn.endswith(".py"):  py_files.append(fp)
                if fn.endswith(".php"): php_files.append(fp)

        all_files = py_files + php_files
        if not all_files:
            r = AIAnalysisResult()
            r.code_type = "لا توجد ملفات Python/PHP"
            return r
        if len(all_files) == 1:
            return cls.analyze_file(all_files[0])

        results: List[AIAnalysisResult] = [cls.analyze_file(p) for p in all_files[:15]]
        merged = AIAnalysisResult()
        merged.lines_of_code   = sum(r.lines_of_code for r in results)
        merged.functions_count = sum(r.functions_count for r in results)
        merged.classes_count   = sum(r.classes_count for r in results)
        merged.libraries_count = sum(r.libraries_count for r in results)
        merged.has_async       = any(r.has_async for r in results)
        merged.has_error_handling = any(r.has_error_handling for r in results)
        merged.has_logging     = any(r.has_logging for r in results)
        merged.has_config      = any(r.has_config for r in results)
        merged.is_bot          = any(r.is_bot for r in results)
        merged.api_calls       = list(set(a for r in results for a in r.api_calls))
        merged.potential_issues= list(set(i for r in results for i in r.potential_issues))[:6]
        merged.recommendations = list(set(rc for r in results for rc in r.recommendations))[:5]
        merged.security_notes  = list(set(s for r in results for s in r.security_notes))[:4]
        merged.quality_score   = int(sum(r.quality_score for r in results) / len(results))

        has_php  = any(r.file_type == "php"    for r in results)
        has_py   = any(r.file_type == "python" for r in results)
        merged.code_type = ("مشروع Python+PHP" if has_php and has_py else
                            "مشروع PHP"        if has_php else "مشروع Python")

        if merged.lines_of_code < 200:    merged.complexity = "بسيط"
        elif merged.lines_of_code < 800:  merged.complexity = "متوسط"
        elif merged.lines_of_code < 2000: merged.complexity = "متقدم"
        else:                              merged.complexity = "ضخم"

        quality_label = ("ممتاز" if merged.quality_score >= 80 else
                         "جيد"   if merged.quality_score >= 60 else
                         "مقبول" if merged.quality_score >= 40 else "يحتاج تحسين")
        merged.summary = (
            f"مشروع {merged.code_type} ({len(all_files)} ملف) بجودة {quality_label} "
            f"({merged.quality_score}/100). {merged.lines_of_code} سطر إجمالاً."
        )
        return merged

    @classmethod
    def format_report(cls, result: AIAnalysisResult, filename: str = "") -> str:
        stars     = "⭐" * max(1, min(5, result.quality_score // 20))
        lang_icon = Icon.PHP if result.file_type == "php" else Icon.PYTHON

        def score_emoji(s: int) -> str:
            if s >= 80: return "🟢"
            if s >= 60: return "🟡"
            if s >= 40: return "🟠"
            return "🔴"

        lines = [
            f"𓆩{Icon.AI}𓆪 <b>تقرير الذكاء الاصطناعي</b>",
            f"{SEP_MAIN}",
        ]
        if filename:
            lines.append(f"{lang_icon} الملف: <code>{escape_html(filename)}</code>")
        lines += [
            f"{Icon.CODE} النوع: <b>{escape_html(result.code_type)}</b>",
            f"{score_emoji(result.quality_score)} جودة الكود: <b>{result.quality_score}/100</b> {stars}",
            f"{Icon.STATS} التعقيد: <b>{result.complexity}</b>",
            f"",
            f"{Icon.INFO} <b>📊 الإحصائيات:</b>",
            f"  {Icon.TASK} الأسطر:    <b>{result.lines_of_code}</b>",
            f"  {Icon.TASK} الدوال:    <b>{result.functions_count}</b>",
            f"  {Icon.TASK} الكلاسات:  <b>{result.classes_count}</b>",
            f"  {Icon.TASK} المكتبات:  <b>{result.libraries_count}</b>",
        ]
        features = []
        if result.has_async:          features.append("غير متزامن ⚡")
        if result.has_error_handling: features.append("معالجة أخطاء ✅")
        if result.has_logging:        features.append("تسجيل أحداث 📝")
        if result.has_config:         features.append("إعدادات بيئة ⚙️")
        if result.has_main:           features.append("نقطة دخول ▶️")
        if features:
            lines.append(f"  {Icon.SPARK} الميزات: {' · '.join(features)}")

        if result.api_calls:
            lines += [f"", f"{Icon.NETWORK} <b>استدعاءات API:</b>"]
            for api in result.api_calls[:5]:
                lines.append(f"  {Icon.TASK} {escape_html(api)}")

        if result.security_notes:
            lines += [f"", f"{Icon.SHIELD} <b>ملاحظات أمنية:</b>"]
            for note in result.security_notes:
                lines.append(f"  {Icon.WARN} {escape_html(note)}")

        if result.potential_issues:
            lines += [f"", f"{Icon.BUG} <b>نقاط تحسين:</b>"]
            for issue in result.potential_issues[:5]:
                lines.append(f"  {Icon.TASK} {escape_html(issue)}")

        if result.recommendations:
            lines += [f"", f"{Icon.LIGHT} <b>توصيات:</b>"]
            for rec in result.recommendations[:4]:
                lines.append(f"  {Icon.TASK} {escape_html(rec)}")

        lines += [
            f"",
            SEP_MAIN,
            f"{Icon.MAGIC} <b>الخلاصة:</b> {escape_html(result.summary)}",
        ]
        return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════
# 🛡  حماية الأمان — فحص الكود
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class SecurityScan:
    blocked: bool = False
    ban: bool     = False
    score: int    = 0
    reasons: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class HostingSecurity:
    """
    ╔══════════════════════════════════════════════════════════╗
    ║  حماية متقدمة لملفات الاستضافة Python + PHP            ║
    ║  يمنع: سرقة API · اختراق النظام · Zip Slip · Bombs    ║
    ╚══════════════════════════════════════════════════════════╝
    """

    CERTAIN_PATTERNS: List[Tuple[str, str]] = [
        (r"(?i)BOT_TOKEN|ADMIN_IDS|SUPPORT_USERNAME|PAYMENT_PROVIDER_TOKEN",
         "محاولة قراءة إعدادات بوت الاستضافة"),
        (r"(?i)bot_database\.json|hosted_files|bot_logs|backups|temp_work|pending_files",
         "محاولة لمس ملفات الاستضافة الداخلية"),
        (r"(?i)DATABASE_FILE|FILES_DIR|LOGS_DIR|BACKUP_DIR|TEMP_DIR|PENDING_DIR",
         "محاولة الوصول لمتغيرات مسارات الاستضافة"),
        (r"(?i)SUPABASE_SERVICE_ROLE_KEY|SUPABASE_URL|SUPABASE_KEY",
         "محاولة قراءة أسرار Supabase"),
        (r"(?i)AWS_SECRET_ACCESS_KEY|AWS_ACCESS_KEY_ID|AWS_SESSION_TOKEN",
         "محاولة قراءة أسرار AWS"),
        (r"(?i)SECRET_KEY|PRIVATE_KEY|SIGNING_KEY|ENCRYPTION_KEY",
         "محاولة قراءة مفاتيح تشفير سرية"),
        (r"(?i)OPENAI_API_KEY|ANTHROPIC_API_KEY|GOOGLE_API_KEY|STRIPE_SECRET",
         "محاولة سرقة مفاتيح AI/Payment API"),
        (r"(?i)GITHUB_TOKEN|GITLAB_TOKEN|BITBUCKET_TOKEN",
         "محاولة سرقة رمز Git"),
        (r"(?i)MONGODB_URI|POSTGRES_URL|DATABASE_URL|REDIS_URL|MYSQL_PWD",
         "محاولة سرقة بيانات اتصال قاعدة البيانات"),
        (r"rm\s+-rf\s+/(?:\s|$)|shutil\.rmtree\(\s*['\"]\/",
         "محاولة حذف جذر النظام"),
        (r"subprocess\.(?:Popen|run|call).*?(?:curl|wget).*?\|\s*(?:sh|bash)",
         "تحميل وتنفيذ سكربت خارجي"),
        (r"fork\s*bomb|:\s*\(\s*\)\s*\{.*\|\s*:\s*&\s*\};",
         "Fork bomb مكتشف"),
        (r"requests\.(get|post)\s*\(['\"]https?://(?!api\.telegram\.org).*?(?:token|secret|password|key)",
         "إرسال بيانات سرية لخادم خارجي"),
        (r"socket\.connect\s*\(.*?(?:\d{1,3}\.){3}\d{1,3}.*?\d{4,5}",
         "اتصال مباشر بعنوان IP خارجي"),
        (r"open\s*\(\s*['\"](?:/etc/passwd|/etc/shadow|/proc/|/sys/)",
         "محاولة قراءة ملفات نظام حساسة"),
        # PHP خاص
        (r"(?i)system\s*\(|shell_exec\s*\(|exec\s*\(|passthru\s*\(",
         "تنفيذ أوامر نظام في PHP"),
        (r"(?i)file_get_contents\s*\(\s*['\"](?:/etc/passwd|/etc/shadow)",
         "قراءة ملفات نظام في PHP"),
        (r"(?i)\$_SERVER\s*\[\s*['\"]HTTP_HOST|SERVER_ADDR|DOCUMENT_ROOT",
         "محاولة قراءة معلومات السيرفر"),
    ]

    WARN_PATTERNS: List[Tuple[str, str]] = [
        (r"subprocess\.|os\.system\(|os\.popen\(", "يستخدم تنفيذ أوامر نظام Python"),
        (r"socket\.|requests\.|aiohttp\.|httpx\.", "يتصل بالشبكة"),
        (r"open\s*\(.*['\"]w['\"]", "يكتب ملفات"),
        (r"shutil\.rmtree|os\.remove|os\.unlink", "يحذف ملفات"),
        (r"eval\s*\(|exec\s*\(", "يستخدم eval/exec"),
        (r"ctypes\.|cffi\.", "يستخدم مكتبات ذات مستوى منخفض"),
        (r"(?i)curl_exec|file_get_contents\s*\(.*https?://", "PHP: استدعاء URL خارجي"),
        (r"(?i)mysql_query|mysqli_query|PDO", "PHP: استعلامات قاعدة بيانات"),
    ]

    DANGEROUS_EXTENSIONS: Set[str] = {
        ".exe", ".dll", ".so", ".dylib", ".sh", ".bash",
        ".bat", ".cmd", ".ps1", ".vbs", ".jar",
        ".asp", ".aspx", ".cgi",
    }

    FORBIDDEN_FILENAMES: Set[str] = {
        ".env", ".env.local", ".env.production", "id_rsa", "id_ed25519",
        "authorized_keys", "known_hosts", ".htpasswd", "credentials",
        "secret", "secrets.json", "config.secret",
    }

    @classmethod
    def scan_source(cls, source: str, label: str) -> SecurityScan:
        res = SecurityScan()
        for pattern, reason in cls.CERTAIN_PATTERNS:
            if re.search(pattern, source, re.DOTALL | re.IGNORECASE):
                res.score += 120
                res.reasons.append(f"{label}: {reason}")
        for pattern, reason in cls.WARN_PATTERNS:
            if re.search(pattern, source, re.DOTALL):
                res.warnings.append(f"{label}: {reason}")
        if res.score >= 120:
            res.blocked = True
            res.ban     = bool(db.settings.get("ban_on_confirmed_danger", True))
        return res

    @classmethod
    def merge(cls, items: List[SecurityScan]) -> SecurityScan:
        out = SecurityScan()
        for item in items:
            out.score    += item.score
            out.reasons.extend(item.reasons)
            out.warnings.extend(item.warnings)
            out.blocked = out.blocked or item.blocked
            out.ban     = out.ban     or item.ban
        return out

    @classmethod
    def scan_file(cls, path: str, label: Optional[str] = None) -> SecurityScan:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return cls.scan_source(f.read(), label or os.path.basename(path))
        except Exception as e:
            r = SecurityScan()
            r.warnings.append(f"تعذر فحص {label or path}: {e}")
            return r

    @classmethod
    def scan_directory(cls, dir_path: str) -> SecurityScan:
        scans: List[SecurityScan] = []
        for root, _, files in os.walk(dir_path):
            for fn in files:
                full    = os.path.join(root, fn)
                rel     = os.path.relpath(full, dir_path)
                fn_lower= fn.lower()
                if fn_lower in cls.FORBIDDEN_FILENAMES:
                    r = SecurityScan(blocked=True, ban=True, score=120,
                                     reasons=[f"{rel}: ملف أسرار/مفاتيح محظور"])
                    scans.append(r); continue
                ext = os.path.splitext(fn_lower)[1]
                if ext in cls.DANGEROUS_EXTENSIONS:
                    r = SecurityScan(blocked=True, ban=False, score=80,
                                     reasons=[f"{rel}: امتداد ملف خطير ({ext})"])
                    scans.append(r); continue
                if fn.endswith(".py") or fn.endswith(".php"):
                    scans.append(cls.scan_file(full, rel))
        return cls.merge(scans)

    @classmethod
    def validate_zip_members(cls, zf: zipfile.ZipFile) -> SecurityScan:
        res = SecurityScan()
        for info in zf.infolist():
            name = info.filename.replace("\\", "/")
            if name.startswith("/") or "../" in name or name.startswith("../"):
                res.blocked = True; res.ban = True; res.score += 120
                res.reasons.append(f"مسار ZIP خطر (Zip Slip): {name}")
            fn_lower = os.path.basename(name).lower()
            if fn_lower in cls.FORBIDDEN_FILENAMES:
                res.blocked = True; res.score += 80
                res.reasons.append(f"ملف محظور داخل ZIP: {name}")
            ext = os.path.splitext(fn_lower)[1]
            if ext in cls.DANGEROUS_EXTENSIONS:
                res.score += 40
                res.warnings.append(f"امتداد خطير داخل ZIP: {name}")
        return res


def safe_extract_zip(zf: zipfile.ZipFile, target_dir: str) -> None:
    base = os.path.abspath(target_dir)
    for member in zf.infolist():
        dest = os.path.abspath(os.path.join(target_dir, member.filename))
        if not dest.startswith(base + os.sep) and dest != base:
            raise ValueError(f"مسار غير آمن داخل ZIP: {member.filename}")
    zf.extractall(target_dir)


# ══════════════════════════════════════════════════════════════════════════════
# 📚  كاشف المكتبات التلقائي (Python)
# ══════════════════════════════════════════════════════════════════════════════

class LibraryDetector:
    STDLIB: Set[str] = {
        "os","sys","re","io","ast","json","time","math","uuid","html","base64",
        "shutil","signal","random","hashlib","zipfile","asyncio","logging",
        "platform","tempfile","threading","subprocess","traceback","urllib",
        "datetime","typing","dataclasses","enum","functools","collections",
        "itertools","string","struct","pathlib","csv","sqlite3","socket",
        "ssl","ftplib","smtplib","email","http","queue","multiprocessing",
        "concurrent","abc","argparse","array","bisect","calendar","copy",
        "ctypes","decimal","difflib","fnmatch","fractions","gc","getopt",
        "getpass","glob","gzip","heapq","inspect","ipaddress","keyword",
        "linecache","locale","mmap","operator","pickle","pkgutil","pprint",
        "statistics","tarfile","textwrap","timeit","token","tokenize",
        "unittest","wave","weakref","xml","xmlrpc","zipimport","zlib",
        "builtins","codecs","codeop","colorsys","compileall","contextlib",
        "contextvars","curses","dis","doctest","encodings","filecmp",
        "fileinput","formatter","html","http","imaplib","importlib","io",
        "lib2to3","mailbox","marshal","modulefinder","msvcrt","netrc",
        "nis","nntplib","numbers","optparse","parser","pdb","pickletools",
        "pipes","pkgutil","poplib","posix","posixpath","profile","pstats",
        "pty","pwd","py_compile","pyclbr","pydoc","readline","reprlib",
        "rlcompleter","runpy","sched","secrets","select","selectors",
        "shelve","shlex","site","smtpd","sndhdr","spwd","stat","stringprep",
        "sunau","symtable","sysconfig","syslog","tabnanny","telnetlib",
        "termios","test","this","tty","turtle","turtledemo","types",
        "unicodedata","uu","venv","warnings","winreg","winsound","wsgiref",
        "xdrlib","xmlrpc","zipapp","_thread","copy_reg","abc","_collections_abc",
        "typing_extensions","annotated_types",
    }

    @classmethod
    def detect_from_source(cls, source: str) -> List[str]:
        try:
            tree = ast.parse(source)
        except: return []
        imports: Set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for a in node.names: imports.add(a.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module: imports.add(node.module.split(".")[0])
        return [lib for lib in sorted(imports) if lib not in cls.STDLIB and not lib.startswith("_")]

    @classmethod
    def detect_from_file(cls, path: str) -> List[str]:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return cls.detect_from_source(f.read())
        except: return []

    @classmethod
    def detect_from_directory(cls, dir_path: str) -> List[str]:
        libs: Set[str] = set()
        req_file = os.path.join(dir_path, "requirements.txt")
        if os.path.exists(req_file):
            with open(req_file, encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        pkg = re.split(r"[>=<!\[]", line)[0].strip()
                        if pkg: libs.add(pkg)
        for root, _, files in os.walk(dir_path):
            for fn in files:
                if fn.endswith(".py"):
                    libs.update(cls.detect_from_file(os.path.join(root, fn)))
        return sorted(libs)

    @classmethod
    def find_entry_point(cls, dir_path: str) -> str:
        for name in ("main.py", "app.py", "bot.py", "run.py", "start.py",
                     "server.py", "index.py", "__main__.py"):
            if os.path.exists(os.path.join(dir_path, name)):
                return name
        for root, _, files in os.walk(dir_path):
            for fn in files:
                if fn.endswith(".py"):
                    return os.path.relpath(os.path.join(root, fn), dir_path)
        return ""

    @classmethod
    def find_php_entry(cls, dir_path: str) -> str:
        for name in ("index.php", "main.php", "app.php", "bot.php", "run.php", "start.php"):
            if os.path.exists(os.path.join(dir_path, name)):
                return name
        for root, _, files in os.walk(dir_path):
            for fn in files:
                if fn.endswith(".php"):
                    return os.path.relpath(os.path.join(root, fn), dir_path)
        return ""


# ══════════════════════════════════════════════════════════════════════════════
# ✉️  إرسال الإشعارات والملصقات
# ══════════════════════════════════════════════════════════════════════════════

async def send_named_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE,
                              name: str) -> None:
    stickers = db.settings.get("stickers") or {}
    file_id  = stickers.get(name) or STICKERS.get(name)
    if not file_id: return
    try:
        chat = update.effective_chat
        if chat: await context.bot.send_sticker(chat_id=chat.id, sticker=file_id)
    except: pass


async def _edit_or_send(update: Update, text: str,
                         markup: Optional[InlineKeyboardMarkup] = None) -> None:
    kwargs: Dict[str, Any] = {"parse_mode": ParseMode.HTML}
    if markup: kwargs["reply_markup"] = markup
    try:
        if update.callback_query and update.callback_query.message:
            try:
                await update.callback_query.edit_message_text(text[:4096], **kwargs)
                return
            except BadRequest as e:
                if "not modified" in str(e).lower(): return
    except: pass
    try:
        chat = update.effective_chat
        if chat:
            await context.bot.send_message(chat.id, text[:4096], **kwargs) if False else None
    except: pass
    try:
        msg = update.effective_message
        if msg:
            await msg.reply_text(text[:4096], **kwargs)
    except: pass


async def _reply_anywhere(update: Update, text: str,
                           markup: Optional[InlineKeyboardMarkup] = None) -> None:
    kwargs: Dict[str, Any] = {"parse_mode": ParseMode.HTML}
    if markup: kwargs["reply_markup"] = markup
    try:
        msg = update.effective_message
        if msg: await msg.reply_text(text[:4096], **kwargs)
    except: pass


async def run_blocking_with_progress(msg: Message, title: str,
                                      fn: Callable, *args) -> Tuple[Any, str]:
    loop   = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, fn, *args)
    return result


# ══════════════════════════════════════════════════════════════════════════════
# 🔐  Decorators للتحقق من الصلاحيات
# ══════════════════════════════════════════════════════════════════════════════

def maintenance_gate(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if db.settings.get("maintenance_mode") and not is_admin(update.effective_user.id):
            text = (
                f"𓆩🛠𓆪 <b>وضع الصيانة مفعّل</b>\n"
                f"{SEP_MAIN}\n"
                f"البوت متوقف مؤقتاً للصيانة.\n"
                f"يرجى المحاولة لاحقاً. 🙏"
            )
            await _reply_anywhere(update, text)
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

def check_banned(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        # فحص أمان: إذا كان التحديث لا يحتوي على مستخدم (تحديث فارغ أو من قنوات) يتم تخطيه
        if not update.effective_user:
            return

        uid = update.effective_user.id
        u   = db.users.get(uid)
        if u and u.is_banned and not is_admin_immortal(uid):
            reason = u.ban_reason or "مخالفة الشروط"
            text   = (
                f"𓆩🚫𓆪 <b>حسابك محظور</b>\n"
                f"{SEP_MAIN}\n"
                f"السبب: {escape_html(reason)}\n\n"
                f"للتواصل مع الدعم: @{db.settings.get('support_username', SUPPORT_USERNAME)}"
            )
            await _reply_anywhere(update, text)
            return
        return await func(update, context, *args, **kwargs)
    return wrapper
def rate_limit(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        uid = update.effective_user.id
        if not rate_limiter.check(uid):
            u = db.users.get(uid)
            if u:
                u.rate_violations = (u.rate_violations or 0) + 1
                db.update_user(u, save=False)
            text = (
                f"𓆩⚡𓆪 <b>تجاوزت الحد المسموح</b>\n"
                f"{SEP_THIN}\n"
                f"أرسلت رسائل كثيرة جداً. انتظر لحظة ثم أعد المحاولة. ⏳"
            )
            await _reply_anywhere(update, text)
            return
        return await func(update, context, *args, **kwargs)
    return wrapper


def admin_only(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if not is_admin(update.effective_user.id):
            await _reply_anywhere(update,
                                   f"𓆩👑𓆪 هذا الأمر للمشرفين فقط.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper


# ══════════════════════════════════════════════════════════════════════════════
# 📣  فحص الاشتراك الإجباري
# ══════════════════════════════════════════════════════════════════════════════

async def check_subscription(user_id: int, bot) -> Tuple[bool, List[Channel]]:
    # ✅ تم تعطيل الاشتراك الإجباري نهائياً
    return True, []


def subscription_keyboard(missing: List[Channel]) -> InlineKeyboardMarkup:
    rows: List[List[InlineKeyboardButton]] = []
    for ch in missing:
        label = f"📣 {shorten(ch.title or ch.chat_id, 25)}"
        link  = ch.invite_link or (f"https://t.me/{ch.chat_id.lstrip('@')}" if ch.chat_id.startswith("@") else "#")
        rows.append([btn_url_success(label, link)])
    rows.append([btn_success("✅ تحققت من الاشتراك", "check_sub")])
    return InlineKeyboardMarkup(rows)


async def enforce_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    # ✅ تم تعطيل الاشتراك الإجباري نهائياً — لا توجد أي رسائل قنوات
    return True


# ══════════════════════════════════════════════════════════════════════════════
# ⌨️  بناء لوحات الأزرار
# ══════════════════════════════════════════════════════════════════════════════

def kb_main_menu(user_id: int) -> InlineKeyboardMarkup:
    rows = [
        # ── رفع ملف ──
        [btn_success("📤  رفع ملف جديد  ✦",              "menu:upload")],
        # ── ملفاتي ──
        [btn_primary("📁  ملفاتي المرفوعة",               "menu:myfiles"),
         btn_primary("⏳  قيد المراجعة",                   "menu:pending")],
        # ── نقاط + دعوة ──
        [btn_primary("💎  نقاطي",                          "menu:points"),
         btn_success("🎁  دعوة أصدقاء",                   "menu:invite")],
        # ── شراء نقاط ──
        [btn_success("⭐  شراء نقاط  ✦",                  "menu:buy")],
        # ── إحصائيات + متصدرون ──
        [btn_primary("📊  إحصائياتي",                      "menu:stats"),
         btn_success("🏆  المتصدرون",                      "menu:leaderboard")],
        # ── كود + دعم ──
        [btn_success("💻  كود نقاط",                       "menu:redeem"),
         btn_primary("💬  الدعم",                           "menu:support")],
        # ── إعدادات + حماية ──
        [btn_primary("⚙️  الإعدادات",                     "menu:settings"),
         btn_success("🛡  الحماية",                         "menu:security")],
        # ── عن البوت ──
        [btn_success("💎  متجر VIP الذهبي  ✦",            "vip:menu"),
         btn_primary("📞  تواصل مع @og4_z",                "vip:contact")],
        [btn_primary("ℹ️  عن البوت",                      "menu:about")],
    ]
    if user_id in ADMIN_IDS:
        rows.append([btn_danger("👑  لوحة الإدارة  ✦",    "admin:panel")])
    return InlineKeyboardMarkup(rows)


def kb_back(target: str = "menu:main", label: Optional[str] = None) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[btn_primary(label or "⬅️  رجوع", target)]])


def kb_confirm(yes_cb: str, no_cb: str = "menu:main",
               yes_label: Optional[str] = None, no_label: Optional[str] = None) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        btn_success(yes_label or "✅  نعم، تأكيد", yes_cb),
        btn_danger (no_label  or "❌  لا، إلغاء",  no_cb),
    ]])


def kb_upload_type() -> InlineKeyboardMarkup:
    """اختيار نوع الملف عند الرفع"""
    return InlineKeyboardMarkup([
        [btn_success("🐍  Python (.py / .zip)", "upload:type:python")],
        [btn_success("🐘  PHP (.php / .zip)",   "upload:type:php")],
        [btn_danger ("❌  إلغاء",               "menu:main")],
    ])


def kb_pending_admin(pending_id: str) -> InlineKeyboardMarkup:
    """أزرار الموافقة/الرفض للمشرف"""
    return InlineKeyboardMarkup([
        [
            btn_success("✅  قبول الملف",          f"approve:{pending_id}"),
            btn_danger ("❌  رفض الملف",            f"reject:{pending_id}"),
        ],
        [btn_primary("🔎  عرض التقرير الكامل",     f"pending:report:{pending_id}")],
        [btn_primary("⬅️  لوحة الإدارة",           "admin:panel")],
    ])


def kb_pending_user_list(user_id: int) -> InlineKeyboardMarkup:
    """قائمة الملفات المعلقة للمستخدم"""
    pending = [pu for pu in db.pending_uploads.values() if pu.owner_id == user_id]
    rows: List[List[InlineKeyboardButton]] = []
    for pu in pending[-10:]:
        status_icon = {"pending": "⏳", "approved": "✅", "rejected": "❌"}.get(pu.status, "❓")
        rows.append([btn_primary(
            f"{status_icon} {shorten(pu.file_name, 25)} — {pu.status}",
            f"pending:view:{pu.pending_id}"
        )])
    rows.append([btn_primary("⬅️  القائمة الرئيسية", "menu:main")])
    return InlineKeyboardMarkup(rows)


def kb_admin_panel() -> InlineKeyboardMarkup:
    rows = [
        [btn_primary ("📊  إحصائيات البوت",           "admin:stats")],
        [btn_primary ("👥  المستخدمون",                "admin:users"),
         btn_success ("🔍  بحث مستخدم",               "admin:search")],
        [btn_primary ("📁  الملفات",                   "admin:files"),
         btn_primary ("📺  العمليات الجارية",          "admin:procs")],
        [btn_success ("⏳  الملفات المعلقة",            "admin:pending"),
         btn_primary ("🛡  مركز الحماية",              "admin:security")],
        [btn_success ("💎  إضافة نقاط",               "admin:addpts"),
         btn_danger  ("➖  خصم نقاط",                 "admin:subpts")],
        [btn_success ("💻  أكواد النقاط",              "admin:codes")],
        [btn_danger  ("🚫  حظر مستخدم",               "admin:ban"),
         btn_success ("🟢  فك الحظر",                 "admin:unban")],
        
        [btn_primary ("📣  القنوات",                   "admin:channels"),
         btn_success ("📢  إرسال بث جماعي",           "admin:broadcast")],
        [btn_primary ("📋  سجل البث",                  "admin:bhist"),
         btn_primary ("🏆  المتصدرون",                 "admin:leaderboard")],
        [btn_primary ("⚙️  الإعدادات",                "admin:settings"),
         btn_primary ("🖥  معلومات النظام",            "admin:sysinfo")],
        [btn_success ("📅  الجدولة",                   "admin:schedule"),
         btn_success ("🧠  تقارير AI",                 "admin:ai_reports")],
        [btn_success ("📥  نسخة احتياطية",             "admin:backup"),
         btn_primary ("📤  استعادة نسخة",              "admin:restore")],
        [btn_primary ("🚨  سجل النشاط",               "admin:activity"),
         btn_danger  ("🛠  وضع الصيانة",              "admin:maint")],
        [btn_success ("🔓  منح وصول بالـID",          "admin:grant_access_start"),
         btn_danger  ("🔒  سحب وصول بالـID",          "admin:revoke_access_start")],
        [btn_warning ("🧰  صيانة الأزرار",            "admin:btnmaint")],
        [btn_success ("👑  لوحة التحكم المتقدمة",      "vctl:refresh")],
        [btn_danger  ("⏹  إيقاف جميع العمليات",      "admin:stop_all")],
        [btn_primary ("🏠  القائمة الرئيسية",          "menu:main")],
    ]
    return InlineKeyboardMarkup(rows)


def kb_file_actions(file_id: str, is_owner: bool, running: bool,
                    is_admin_view: bool = False) -> InlineKeyboardMarkup:
    rows: List[List[InlineKeyboardButton]] = []
    if is_owner or is_admin_view:
        if running:
            rows.append([
                btn_danger ("⏹  إيقاف",                    f"file:stop:{file_id}"),
                btn_primary("🔄  إعادة تشغيل",              f"file:restart:{file_id}"),
            ])
        else:
            rows.append([
                btn_success("▶️  تشغيل الملف",              f"file:run:{file_id}"),
                btn_primary("📥  تحميل ZIP",                f"file:zip:{file_id}"),
            ])
        rows.append([
            btn_primary ("📺  السجل المباشر",               f"file:log:{file_id}"),
            btn_success ("💡  تثبيت المكتبات",              f"file:install:{file_id}"),
        ])
        rows.append([
            btn_success ("🧠  تحليل AI",                    f"file:ai:{file_id}"),
            btn_primary ("✏️  تعديل الوصف",                f"file:desc:{file_id}"),
        ])
        rows.append([
            btn_success ("🔁  إقلاع تلقائي",               f"file:auto:{file_id}"),
            btn_primary ("📤  تصدير السجل",                 f"file:export_log:{file_id}"),
        ])
        rows.append([
            btn_success ("🔗  رابط مشاركة",                f"file:share:{file_id}"),
            btn_primary ("🌐  تغيير العمومية",              f"file:public:{file_id}"),
        ])
        rows.append([btn_danger("🗑  حذف الملف",            f"file:del:{file_id}")])
        if is_admin_view:
            hf = db.get_file(file_id)
            if hf:
                rows.append([btn_primary("👤  صاحب الملف", f"admin:user:{hf.owner_id}")])
    else:
        rows.append([btn_primary("📥  تحميل ZIP", f"file:zip:{file_id}")])
    rows.append([btn_primary("⬅️  ملفاتي", "menu:myfiles")])
    return InlineKeyboardMarkup(rows)


def kb_buy_points() -> InlineKeyboardMarkup:
    packs  = [(10, 15), (25, 35), (50, 65), (100, 120), (250, 280), (500, 540)]
    styles = [btn_primary, btn_success, btn_primary, btn_success, btn_danger, btn_danger]
    emojis = ["🔹", "⭐", "🔷", "💎", "🔥", "👑"]
    rows: List[List[InlineKeyboardButton]] = []
    row:  List[InlineKeyboardButton]       = []
    for i, (pts, stars) in enumerate(packs):
        fn = styles[i % len(styles)]
        em = emojis[i % len(emojis)]
        row.append(fn(f"{em} {pts} نقطة · {stars} ⭐", f"buy:{pts}:{stars}"))
        if len(row) == 2:
            rows.append(row); row = []
    if row: rows.append(row)
    rows.append([btn_primary("⬅️  رجوع", "menu:main")])
    return InlineKeyboardMarkup(rows)


def kb_paginated(items: List[Tuple[str, str]], page: int, page_size: int,
                 base_cb: str, back_cb: str = "menu:main",
                 item_style: str = "primary") -> InlineKeyboardMarkup:
    total  = len(items)
    pages  = max(1, math.ceil(total / page_size))
    page   = max(0, min(page, pages - 1))
    start  = page * page_size
    end    = min(start + page_size, total)
    rows: List[List[InlineKeyboardButton]] = []
    style_fn = {"primary": btn_primary, "success": btn_success, "danger": btn_danger}.get(item_style, btn_primary)
    for label, cb in items[start:end]:
        rows.append([style_fn(label, cb)])
    nav: List[InlineKeyboardButton] = []
    if page > 0:
        nav.append(btn_secondary(f"◀️  السابق",  f"{base_cb}:{page-1}"))
    nav.append(btn_noop(f"صفحة {page+1}/{pages}"))
    if page < pages - 1:
        nav.append(btn_secondary(f"التالي  ▶️", f"{base_cb}:{page+1}"))
    if nav: rows.append(nav)
    rows.append([btn_secondary(f"⬅️  رجوع", back_cb)])
    return InlineKeyboardMarkup(rows)


def kb_settings_admin() -> InlineKeyboardMarkup:
    s = db.settings
    def btgl(label: str, key: str) -> InlineKeyboardButton:
        return btn_toggle(label, f"adminset:toggle:{key}", bool(s.get(key)))
    rows = [
        [btgl("🛠  وضع الصيانة",              "maintenance_mode")],
        [btgl("🔒  الاشتراك إجباري",          "require_subscription")],
        [btgl("📦  تثبيت المكتبات تلقائياً",  "auto_install_libs")],
        [btgl("▶️  تشغيل تلقائي بعد الرفع",  "auto_run_after_upload")],
        [btgl("🔁  إقلاع تلقائي افتراضياً",  "auto_restart_default")],
        [btgl("🗜  ZIP عند فشل التشغيل",      "send_zip_if_run_fails")],
        [btgl("🛡  حماية الاستضافة",          "strict_hosting_security")],
        [btgl("🔐  حماية API متقدمة",         "api_protection_enabled")],
        [btgl("🚨  حظر عند خطر مؤكد",        "ban_on_confirmed_danger")],
        [btgl("🧠  تحليل AI عند الرفع",       "ai_analysis_enabled")],
        [btgl("⏳  موافقة إدارية مطلوبة",     "require_admin_approval")],
        [btgl("🐘  دعم PHP",                   "php_support_enabled")],
        [btgl("✅  موافقة تلقائية للآمنة",    "auto_approve_safe_files")],
        [btgl("📨  إشعار نتيجة المراجعة",     "approval_notify_user")],
        [btgl("🎁  الرفع المجاني الأول",       "first_upload_free")],
        [btgl("🌐  ملفات عامة مفعّلة",        "public_files_enabled")],
        [btgl("🔔  إشعار دخول جديد",          "notify_admin_on_join")],
        [btgl("📤  إشعار رفع جديد",           "notify_admin_on_upload")],
        [btgl("⚡  Rate Limit مفعّل",          "rate_limit_enabled")],
        [btgl("🏆  Leaderboard مفعّل",         "leaderboard_enabled")],
        [btgl("📅  الجدولة مفعّلة",            "schedule_enabled")],
        [btgl("👑  حماية مطلقة للمشرف",       "admin_immortal")],
        [btn_warning(f"سعر الرفع: {s.get('upload_cost',1)} نقطة",        "adminset:num:upload_cost"),
         btn_warning(f"نقاط الدعوة: {s.get('points_per_invite',2)}",     "adminset:num:points_per_invite")],
        [btn_warning(f"نجوم/10نقاط: {s.get('stars_per_10_points',15)}",  "adminset:num:stars_per_10_points"),
         btn_warning(f"حجم/ميجا: {s.get('max_file_size_mb',50)}",        "adminset:num:max_file_size_mb")],
        [btn_warning(f"عمليات/مستخدم: {s.get('max_processes_per_user',3)}", "adminset:num:max_processes_per_user"),
         btn_warning(f"مهلة التشغيل: {s.get('run_timeout_seconds',0)}",    "adminset:num:run_timeout_seconds")],
        [btn_warning(f"حد Rate: {s.get('rate_limit_messages',10)} رسالة",  "adminset:num:rate_limit_messages"),
         btn_warning(f"نافذة Rate: {s.get('rate_limit_window',10)}ث",      "adminset:num:rate_limit_window")],
        [btn_primary(f"✏️  تعديل رسالة الترحيب",    "adminset:text:welcome_message")],
        [btn_primary(f"💬  تعديل يوزر الدعم",        "adminset:text:support_username")],
        [btn_primary(f"🐘  مسار PHP",               "adminset:text:php_executable")],
        [btn_secondary(f"⬅️  لوحة الإدارة",         "admin:panel")],
    ]
    return InlineKeyboardMarkup(rows)


def kb_channels_admin() -> InlineKeyboardMarkup:
    rows: List[List[InlineKeyboardButton]] = []
    for ch in db.all_channels():
        title = ch.title or ch.chat_id
        rows.append([
            btn_toggle(shorten(title, 22), f"chan:toggle:{ch.chat_id}", ch.enabled),
            btn_danger(f"🗑  حذف", f"chan:del:{ch.chat_id}"),
        ])
    rows.append([
        btn_success("➕  إضافة قناة", "chan:add"),
        btn_primary("🔄  تحديث",      "admin:channels"),
    ])
    rows.append([btn_primary("⬅️  لوحة الإدارة", "admin:panel")])
    return InlineKeyboardMarkup(rows)


def kb_settings_user(u: User) -> InlineKeyboardMarkup:
    rows = [
        [btn_toggle("🔔  الإشعارات", "userset:toggle:notif", u.notifications_enabled)],
        [btn_primary("🔗  رابط دعوتي",          "menu:invite")],
        [btn_success("📥  تصدير بياناتي",        "userset:export")],
        [btn_primary("🏠  الرئيسية",             "menu:main")],
    ]
    return InlineKeyboardMarkup(rows)


# ══════════════════════════════════════════════════════════════════════════════
# 📜  نصوص العرض
# ══════════════════════════════════════════════════════════════════════════════

def text_welcome(u: User, bot_username: str) -> str:
    premium_badge = f" 💫" if u.is_premium else ""
    admin_badge   = f" 👑" if is_admin(u.user_id) else ""
    lang_info     = f"🐍 Python: {u.total_python_files} | 🐘 PHP: {u.total_php_files}"
    pending_count = db.user_pending_count(u.user_id)
    pending_info  = f"\n{Icon.PENDING} قيد المراجعة: <b>{pending_count}</b>" if pending_count > 0 else ""
    return (
        f"𓆩♛𓆪 <b>{escape_html(db.settings.get('welcome_message', BOT_NAME))}</b>\n"
        f"{SEP_STAR}\n"
        f"{Icon.USER} الاسم: <b>{escape_html(u.first_name or '—')}</b>{premium_badge}{admin_badge}\n"
        f"المعرّف: <code>{u.user_id}</code>\n"
        f"{Icon.DIAMOND} نقاطك: <b>{u.points}</b>\n"
        f"{Icon.UPLOAD} ر��ع مجاني متبقي: <b>{u.free_uploads}</b>\n"
        f"{Icon.FOLDER} ملفاتك: <b>{len(u.files)}</b>\n"
        f"{lang_info}"
        f"{pending_info}\n"
        f"{SEP_THIN}\n"
        f"{Icon.LINK} رابط دعوتك:\n"
        f"<code>https://t.me/{bot_username}?start=ref{u.user_id}</code>"
    )


def text_about() -> str:
    py      = sys.version.split()[0]
    running = len(pm.all_running())
    php_ok  = detect_php()
    pending = len(db.all_pending())
    return (
        f"𓆩♛𓆪 <b>{BOT_NAME}</b>\n"
        f"{SEP_DOUBLE}\n"
        f"الإصدار: <b>{BOT_VERSION}</b>\n"
        f"Python:  <code>{py}</code>\n"
        f"PHP:     <b>{'متوفر ✅' if php_ok else 'غير متوفر ❌'}</b>\n"
        f"النظام:  <code>{platform.system()} {platform.release()}</code>\n"
        f"{SEP_THIN}\n"
        f"المستخدمون:      <b>{len(db.users)}</b>\n"
        f"الملفات:         <b>{len(db.files)}</b>\n"
        f"يعمل الآن:       <b>{running}</b>\n"
        f"قيد المراجعة:    <b>{pending}</b>\n"
        f"{SEP_THIN}\n"
        f"𓆩🧠𓆪 AI تحليل الكود    | 𓆩🔐𓆪 حماية API\n"
        f"𓆩🛡𓆪 حماية المشرف    | 𓆩⏳𓆪 نظام الموافقة\n"
        f"𓆩🐘𓆪 دعم PHP+Python  | 𓆩📅𓆪 جدولة + Premium"
    )


def text_admin_stats() -> str:
    s       = db.stats
    running = len(pm.all_running())
    premium = len(db.get_premium_users())
    banned  = sum(1 for u in db.all_users() if u.is_banned)
    new7    = len(db.get_new_users(7))
    today   = datetime.now().strftime("%Y-%m-%d")
    daily   = len(db.stats.get("daily_active", {}).get(today, []))
    pending = len(db.all_pending())
    py_files  = sum(1 for f in db.files.values() if f.file_type == "python")
    php_files = sum(1 for f in db.files.values() if f.file_type == "php")
    return (
        f"𓆩📊𓆪 <b>إحصائيات البوت</b>\n"
        f"{SEP_MAIN}\n"
        f"👥 المستخدمون:       <b>{len(db.users)}</b>\n"
        f"  📅 نشطون اليوم:    <b>{daily}</b>\n"
        f"  🆕 جدد (7 أيام):   <b>{new7}</b>\n"
        f"  💫 بريميوم:        <b>{premium}</b>\n"
        f"  🚫 محظورون:        <b>{banned}</b>\n"
        f"{SEP_THIN}\n"
        f"📁 الملفات:          <b>{len(db.files)}</b>\n"
        f"  🐍 Python:         <b>{py_files}</b>\n"
        f"  🐘 PHP:            <b>{php_files}</b>\n"
        f"  ⏳ قيد المراجعة:   <b>{pending}</b>\n"
        f"📺 العمليات الحيّة:  <b>{running}</b>\n"
        f"{SEP_THIN}\n"
        f"▶️  إجمالي التشغيل:  <b>{s.get('total_runs',0)}</b>\n"
        f"📥 إجمالي التحميل:   <b>{s.get('total_downloads',0)}</b>\n"
        f"💎 النقاط الممنوحة:  <b>{s.get('total_points_given',0)}</b>\n"
        f"⭐ نجوم مستلمة:     <b>{s.get('total_stars_received',0)}</b>\n"
        f"📢 إجمالي البث:      <b>{s.get('total_broadcasts',0)}</b>\n"
        f"{SEP_THIN}\n"
        f"📅 تاريخ البدء: <b>{format_dt(s.get('created_at',''))}</b>"
    )


def text_leaderboard(category: str = "points") -> str:
    titles  = {
        "points":  f"𓆩💎𓆪 ترتيب النقاط",
        "uploads": f"𓆩📤𓆪 ترتيب الرفع",
        "invites": f"𓆩🎁𓆪 ترتيب الدعوات",
    }
    getters = {
        "points":  lambda u: u.points,
        "uploads": lambda u: u.total_uploads,
        "invites": lambda u: len(u.invited_users),
    }
    medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
    title  = titles.get(category, titles["points"])
    getter = getters.get(category, getters["points"])
    top    = sorted(db.all_users(), key=getter, reverse=True)[:10]
    lines  = [f"𓆩🏆𓆪 <b>{title}</b>\n{SEP_STAR}"]
    for i, u in enumerate(top):
        name  = escape_html(u.first_name or str(u.user_id))
        val   = getter(u)
        badge = " 💫" if u.is_premium else ""
        lines.append(f"{medals[i]} <b>{name}</b>{badge}  →  <b>{val}</b>")
    return "\n".join(lines)


def text_pending_review(pu: PendingUpload) -> str:
    owner = db.users.get(pu.owner_id)
    owner_name = escape_html(owner.first_name or str(pu.owner_id)) if owner else str(pu.owner_id)
    owner_uname = f"@{escape_html(owner.username)}" if owner and owner.username else "—"
    lang_icon = Icon.PHP if pu.file_type == "php" else Icon.PYTHON
    risk_icon = "🔴" if pu.security_blocked else ("🟡" if pu.security_warnings else "🟢")
    status_ar = {"pending": "قيد المراجعة ⏳", "approved": "مقبول ✅", "rejected": "مرفوض ❌"}.get(pu.status, pu.status)
    return (
        f"𓆩⏳𓆪 <b>ملف ينتظر المراجعة</b>\n"
        f"{SEP_MAIN}\n"
        f"{lang_icon} الملف: <code>{escape_html(pu.file_name)}</code>\n"
        f"النوع: <b>{'PHP 🐘' if pu.file_type == 'php' else 'Python 🐍'}</b>\n"
        f"الحجم: <b>{format_size(pu.size)}</b>\n"
        f"المرسل: <b>{owner_name}</b> ({owner_uname})\n"
        f"المعرّف: <code>{pu.owner_id}</code>\n"
        f"وقت الرفع: <b>{format_dt(pu.submitted_at)}</b>\n"
        f"{SEP_THIN}\n"
        f"{risk_icon} مستوى الخطر: <b>{'مرتفع 🔴' if pu.security_blocked else ('متوسط 🟡' if pu.security_warnings else 'منخفض 🟢')}</b>\n"
        f"درجة الأمان: <b>{pu.security_score}</b>\n"
        f"الحالة: <b>{status_ar}</b>"
    )


def text_pending_full_report(pu: PendingUpload) -> str:
    base = text_pending_review(pu)
    extra_parts = []
    if pu.ai_report:
        extra_parts.append(f"\n{SEP_THIN}\n{Icon.AI} <b>تقرير AI:</b>\n{pu.ai_report[:1500]}")
    if pu.security_reasons:
        extra_parts.append(f"\n{SEP_THIN}\n{Icon.DANGER} <b>مخاطر أمنية مؤكدة:</b>\n{escape_html(pu.security_reasons[:800])}")
    if pu.security_warnings:
        extra_parts.append(f"\n{SEP_THIN}\n{Icon.WARN} <b>تحذيرات:</b>\n{escape_html(pu.security_warnings[:600])}")
    if pu.libraries:
        extra_parts.append(f"\n{SEP_THIN}\n{Icon.LIGHT} <b>المكتبات ({len(pu.libraries)}):</b>\n{escape_html(', '.join(pu.libraries[:15]))}")
    return base + "".join(extra_parts)


# ══════════════════════════════════════════════════════════════════════════════
# 📁  منطق الرفع والاستضافة
# ══════════════════════════════════════════════════════════════════════════════

# حالات المحادثة
ST_AWAIT_UPLOAD       = "awaiting_upload"
ST_AWAIT_UPLOAD_TYPE  = "awaiting_upload_type"
ST_AWAIT_BROADCAST    = "awaiting_broadcast"
ST_AWAIT_ADDPTS_ID    = "awaiting_addpts_id"
ST_AWAIT_ADDPTS_AMT   = "awaiting_addpts_amt"
ST_AWAIT_SUBPTS_ID    = "awaiting_subpts_id"
ST_AWAIT_SUBPTS_AMT   = "awaiting_subpts_amt"
ST_AWAIT_BAN_ID       = "awaiting_ban_id"
ST_AWAIT_BAN_REASON   = "awaiting_ban_reason"
ST_AWAIT_UNBAN_ID     = "awaiting_unban_id"
ST_AWAIT_SEARCH       = "awaiting_search"
ST_AWAIT_CHAN_ADD      = "awaiting_channel"
ST_AWAIT_BWORD        = "awaiting_bword"
ST_AWAIT_SET_NUM      = "awaiting_set_num"
ST_AWAIT_SET_TEXT     = "awaiting_set_text"
ST_AWAIT_FILE_DESC    = "awaiting_file_desc"
ST_AWAIT_CODE_REDEEM  = "awaiting_code_redeem"
ST_AWAIT_CODE_CREATE  = "awaiting_code_create"
ST_AWAIT_PREMIUM_UID  = "awaiting_premium_uid"
ST_AWAIT_PREMIUM_DAYS = "awaiting_premium_days"
ST_AWAIT_NOTE         = "awaiting_note_uid"
ST_AWAIT_REJECT_REASON= "awaiting_reject_reason"
ST_AWAIT_SCHEDULE_FID = "awaiting_schedule_fid"
ST_AWAIT_SCHEDULE_TIME= "awaiting_schedule_time"


def clear_state(context: ContextTypes.DEFAULT_TYPE) -> None:
    for k in list(context.user_data.keys()):
        if k.startswith("awaiting_") or k.startswith("state_"):
            context.user_data.pop(k, None)


@maintenance_gate
@check_banned
@rate_limit
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user      = update.effective_user
    is_new    = user.id not in db.users
    u         = db.get_user(user.id, username=user.username or "",
                             first_name=user.first_name or "", last_name=user.last_name or "")
    u.login_count += 1
    db.record_daily_active(user.id)

    args = context.args or []
    if args and args[0].startswith("ref"):
        try: inviter_id = int(args[0][3:])
        except: inviter_id = 0
        if inviter_id and inviter_id != u.user_id and not u.invited_by:
            inviter = db.users.get(inviter_id)
            if inviter:
                u.invited_by = inviter_id
                if u.user_id not in inviter.invited_users:
                    inviter.invited_users.append(u.user_id)
                if u.user_id not in inviter.invite_reward_given_for:
                    inviter.invite_reward_given_for.append(u.user_id)
                    pts = int(db.settings.get("points_per_invite", 2))
                    grant_points(inviter, pts, "invite", note=f"invited {u.user_id}")
                    try:
                        await context.bot.send_message(
                            inviter_id,
                            f"𓆩🎁𓆪 مبروك! صديق جديد انضم ← <b>+{pts}</b> نقطة 🎉",
                            parse_mode=ParseMode.HTML,
                        )
                    except: pass
                db.update_user(inviter)

    if args and args[0].startswith("file_"):
        fid = args[0][5:]
        hf  = db.get_file(fid)
        if hf and hf.is_public:
            await _send_project_zip_direct(update, context, hf, "تحميل عبر رابط مشاركة")
            db.update_user(u)
            return

    db.update_user(u)
    if not await enforce_subscription(update, context): return
    await send_named_sticker(update, context, "login_success")

    if is_new:
        await notify_admins_new_user(u, context)

    # ── بوابة الموافقة على الشروط (ToS) ──
    if not getattr(u, 'agreed_to_terms', False) and not is_admin(u.user_id):
        await _send_tos_gate(update, context, u)
        return

    # ── بوابة الوصول المدفوع ──
    if not has_paid_access(u.user_id):
        await _send_access_gate(update, context)
        return

    me   = await context.bot.get_me()
    text = text_welcome(u, me.username)
    await update.message.reply_text(text, reply_markup=kb_main_menu(u.user_id), parse_mode=ParseMode.HTML)


async def notify_admins_new_user(u: User, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not db.settings.get("notify_admin_on_join", True): return
    text = (
        f"𓆩🆕𓆪 <b>مستخدم جديد انضم!</b>\n"
        f"{SEP_THIN}\n"
        f"الاسم: <b>{escape_html(u.first_name or '—')}</b>\n"
        f"يوزر: @{escape_html(u.username or '—')}\n"
        f"ID: <code>{u.user_id}</code>\n"
        f"وقت: {format_dt(u.join_date)}"
    )
    for adm in ADMIN_IDS:
        try: await context.bot.send_message(adm, text, parse_mode=ParseMode.HTML)
        except: pass


# ──────────────────────────────────────────────────────────────────────────────
# 📤  رفع الملف — الخطوة 1: اختيار النوع
# ──────────────────────────────────────────────────────────────────────────────

@maintenance_gate
@check_banned
@rate_limit
async def upload_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """الخطوة 1: اختر Python أو PHP"""
    uid = update.effective_user.id
    u   = db.get_user(uid)

    # فحص الحد الأقصى للملفات المعلقة
    max_pending = int(db.settings.get("max_pending_per_user", 5))
    current_pending = db.user_pending_count(uid)
    if current_pending >= max_pending and not is_admin(uid):
        text = (
            f"𓆩⚠️𓆪 <b>لديك {current_pending} ملف قيد المراجعة</b>\n"
            f"{SEP_THIN}\n"
            f"الحد الأقصى {max_pending} ملف. انتظر موافقة المشرف أولاً."
        )
        await _edit_or_send(update, text, kb_back("menu:myfiles"))
        return

    # فحص النقاط
    cost     = int(db.settings.get("upload_cost", 1))
    is_free = (db.settings.get("first_upload_free", True) and u.free_uploads > 0) or is_admin(uid)

    if not is_free and u.points < cost:
        text = (
            f"𓆩❌𓆪 <b>نقاط غير كافية</b>\n"
            f"{SEP_THIN}\n"
            f"رصيدك: <b>{u.points}</b> نقطة\n"
            f"مطلوب: <b>{cost}</b> نقطة للرفع"
        )
        kb = InlineKeyboardMarkup([
            [btn_success("⭐  شراء نقاط", "menu:buy")],
            [btn_primary("⬅️  رجوع",     "menu:main")],
        ])
        await _edit_or_send(update, text, kb)
        return

    text = (
        f"𓆩📤𓆪 <b>رفع ملف جديد</b>\n"
        f"{SEP_MAIN}\n"
        f"اختر نوع الملف الذي تريد رفعه:\n\n"
        f"🐍 <b>Python</b> — ملفات .py أو .zip\n"
        f"🐘 <b>PHP</b> — ملفات .php أو .zip\n"
        f"{SEP_THIN}\n"
        f"سيتم فحص الملف أمنياً وإرساله للمشرف\n"
        f"قبل رفعه على الاستضافة. ⚠️"
    )
    await _edit_or_send(update, text, kb_upload_type())


async def upload_type_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE,
                              file_type: str) -> None:
    """الخطوة 2: المستخدم اختار النوع — اطلب منه إرسال الملف"""
    if file_type == "php" and not db.settings.get("php_support_enabled", True):
        await _edit_or_send(update,
                             f"𓆩❌𓆪 دعم PHP غير مفعّل حالياً.",
                             kb_back("menu:main"))
        return

    context.user_data[ST_AWAIT_UPLOAD] = file_type
    lang_icon = Icon.PHP if file_type == "php" else Icon.PYTHON
    lang_name = "PHP 🐘" if file_type == "php" else "Python 🐍"
    ext_info  = ".php أو .zip" if file_type == "php" else ".py أو .zip"

    text = (
        f"𓆩{lang_icon}𓆪 <b>إرسال ملف {lang_name}</b>\n"
        f"{SEP_MAIN}\n"
        f"أرسل ملفك الآن ({ext_info})\n\n"
        f"𓆩⚠️𓆪 <b>تنبيه مهم:</b>\n"
        f"• سيتم فحص الملف أمنياً بالذكاء الاصطناعي\n"
        f"• يُرسَل للمشرف للمراجعة والموافقة\n"
        f"• ستُبلَّغ بالنتيجة عند الانتهاء ✅\n"
        f"{SEP_THIN}\n"
        f"📤 أرسل ملفاً عادياً الآن:"
    )
    await _edit_or_send(update, text,
                         InlineKeyboardMarkup([[btn_danger("❌  إلغاء", "menu:main")]]))


async def handle_document_upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالجة رفع الملف من المستخدم"""
    uid      = update.effective_user.id
    ud       = context.user_data
    file_type= ud.pop(ST_AWAIT_UPLOAD, None)
    if not file_type: return

    doc = update.message.document
    if not doc:
        await update.message.reply_text(f"𓆩❌𓆪 أرسل ملفاً وليس رسالة نصية.")
        return

    fname   = doc.file_name or "file"
    ext_low = os.path.splitext(fname.lower())[1]

    # التحقق من الامتداد
    if file_type == "python" and ext_low not in (".py", ".zip"):
        await update.message.reply_text(
            f"𓆩⚠️𓆪 الامتداد غير صحيح. أرسل ملف .py أو .zip\n"
            f"اضغط /start وأعد المحاولة.")
        return
    if file_type == "php" and ext_low not in (".php", ".zip"):
        await update.message.reply_text(
            f"𓆩⚠️𓆪 الامتداد غير صحيح. أرسل ملف .php أو .zip\n"
            f"اضغط /start وأعد المحاولة.")
        return

    # فحص الحجم
    max_mb = int(db.settings.get("max_file_size_mb", MAX_FILE_SIZE_MB))
    if doc.file_size and doc.file_size > max_mb * 1024 * 1024:
        await update.message.reply_text(
            f"𓆩❌𓆪 الملف كبير جداً. الحد الأقصى {max_mb} MB.")
        return

    # رسالة التحميل
    progress_msg = await update.message.reply_text(
        f"𓆩⏳𓆪 <b>جاري التحميل والفحص...</b>\n{progress_bar(20)} 20%",
        parse_mode=ParseMode.HTML)

    try:
        # تحميل الملف
        pending_id = str(uuid.uuid4())[:12]
        work_dir   = os.path.join(PENDING_DIR, pending_id)
        os.makedirs(work_dir, exist_ok=True)

        tg_file    = await context.bot.get_file(doc.file_id)
        dest_path  = os.path.join(work_dir, fname)
        await tg_file.download_to_drive(dest_path)

        await progress_msg.edit_text(
            f"𓆩⏳𓆪 <b>جاري الفحص الأمني...</b>\n{progress_bar(50)} 50%",
            parse_mode=ParseMode.HTML)

        # استخراج ZIP إذا لزم
        is_zip = ext_low == ".zip"
        if is_zip:
            try:
                with zipfile.ZipFile(dest_path, "r") as zf:
                    zip_scan = HostingSecurity.validate_zip_members(zf)
                    if zip_scan.blocked:
                        os.makedirs(work_dir, exist_ok=True)
                        shutil.rmtree(work_dir, ignore_errors=True)
                        if zip_scan.ban:
                            u = db.get_user(uid)
                            u.is_banned  = True
                            u.ban_reason = "محاولة رفع ZIP مشبوه"
                            db.update_user(u)
                        await progress_msg.edit_text(
                            f"𓆩🔴𓆪 <b>تم رفض الملف — اكتُشفت ملفات خطيرة في ZIP</b>\n"
                            f"{SEP_THIN}\n"
                            f"الأسباب: {escape_html('; '.join(zip_scan.reasons[:3]))}",
                            parse_mode=ParseMode.HTML)
                        return
                    safe_extract_zip(zf, work_dir)
            except zipfile.BadZipFile:
                await progress_msg.edit_text(f"𓆩❌𓆪 ملف ZIP تالف.")
                shutil.rmtree(work_dir, ignore_errors=True)
                return

        # استخراج توكن/ID/User بوت Telegram بشكل منظّم عند الرفع (مع إخفاء جزء من التوكن للحماية)
        detected_tokens = _extract_telegram_tokens_from_path(work_dir if is_zip else dest_path)
        token_infos = await _notify_token_audit(update, context, uid, fname, detected_tokens)
        if any(info.get("is_main") for info in token_infos):
            shutil.rmtree(work_dir, ignore_errors=True)
            await progress_msg.edit_text(
                "𓆩🚫𓆪 <b>تم رفض الملف لمنع التضارب</b>\n"
                f"{SEP_MAIN}\n"
                "الملف يحتوي توكن البوت الرئيسي، وتشغيله سيصنع نسخة ثانية من نفس البوت.\n"
                "تم إيقاف العملية وحماية البوت الرئيسي ✅",
                parse_mode=ParseMode.HTML)
            return

        # الفحص الأمني
        if is_zip:
            sec_scan = HostingSecurity.scan_directory(work_dir)
        else:
            sec_scan = HostingSecurity.scan_file(dest_path, fname)

        await progress_msg.edit_text(
            f"𓆩🧠𓆪 <b>جاري تحليل الذكاء الاصطناعي...</b>\n{progress_bar(75)} 75%",
            parse_mode=ParseMode.HTML)

        # تحليل AI
        ai_report_text = ""
        if db.settings.get("ai_analysis_enabled", True):
            if is_zip:
                ai_result = AICodeAnalyzer.analyze_directory(work_dir)
            else:
                ai_result = AICodeAnalyzer.analyze_file(dest_path)
            ai_report_text = AICodeAnalyzer.format_report(ai_result, fname)

        # كشف المكتبات
        if file_type == "python":
            libs = LibraryDetector.detect_from_directory(work_dir) if is_zip else \
                   LibraryDetector.detect_from_file(dest_path)
        else:
            libs = []

        # إنشاء سجل الملف المعلق
        pu = PendingUpload(
            pending_id     = pending_id,
            file_name      = fname,
            owner_id       = uid,
            submitted_at   = now_iso(),
            size           = doc.file_size or os.path.getsize(dest_path),
            stored_path    = dest_path,
            file_type      = file_type,
            is_zip         = is_zip,
            ai_report      = ai_report_text,
            security_blocked = sec_scan.blocked,
            security_reasons = "\n".join(sec_scan.reasons[:10]),
            security_warnings= "\n".join(sec_scan.warnings[:10]),
            security_score = sec_scan.score,
            status         = "pending",
            libraries      = libs,
        )

        # إذا كانت الملف خطيراً جداً — رفض فوري
        if sec_scan.blocked and sec_scan.ban:
            pu.status = "rejected"
            pu.reject_reason = "اكتُشفت أنماط خطيرة مؤكدة"
            u = db.get_user(uid)
            u.is_banned  = True
            u.ban_reason = "محاولة رفع كود خطير"
            db.update_user(u)
            db.log_security(uid, fname, sec_scan.reasons, True)
            db.add_pending(pu)
            shutil.rmtree(work_dir, ignore_errors=True)
            await send_named_sticker(update, context, "security_blocked")
            await progress_msg.edit_text(
                f"𓆩🔴𓆪 <b>تم رفض الملف تلقائياً</b>\n"
                f"{SEP_MAIN}\n"
                f"اكتُشفت أنماط خطيرة مؤكدة في الكود.\n"
                f"تم حظر حسابك. للاعتراض: @{db.settings.get('support_username', SUPPORT_USERNAME)}",
                parse_mode=ParseMode.HTML)
            return

        # الموافقة التلقائية للملفات الآمنة
        require_approval = db.settings.get("require_admin_approval", True)
        auto_approve_safe = db.settings.get("auto_approve_safe_files", False)

        if not require_approval or (auto_approve_safe and not sec_scan.blocked and sec_scan.score == 0):
            # استضف الملف مباشرة
            db.add_pending(pu)
            await _finalize_upload(update, context, pu, auto=True)
            await progress_msg.delete()
            return

        # ─── إرسال للمراجعة الإدارية ────────────────────────────────────
        db.add_pending(pu)
        db.save(force=True)

        risk_color  = "🔴" if sec_scan.blocked else ("🟡" if sec_scan.warnings else "🟢")
        lang_icon2  = Icon.PHP if file_type == "php" else Icon.PYTHON

        # إشعار المستخدم
        await progress_msg.edit_text(
            f"𓆩✅𓆪 <b>تم استلام ملفك بنجاح!</b>\n"
            f"{SEP_STAR}\n"
            f"{lang_icon2} الملف: <code>{escape_html(fname)}</code>\n"
            f"الحجم: <b>{format_size(pu.size)}</b>\n"
            f"{risk_color} الفحص الأمني: <b>{'يحتاج مراجعة' if sec_scan.blocked or sec_scan.warnings else 'نظيف ✅'}</b>\n"
            f"{SEP_THIN}\n"
            f"𓆩⏳𓆪 <b>الملف في انتظار موافقة المشرف</b>\n"
            f"ستصلك رسالة فور الموافقة أو الرفض. 🔔",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                [btn_primary("⏳  ملفاتي المعلقة", "menu:pending")],
                [btn_primary("🏠  الرئيسية",       "menu:main")],
            ]),
        )

        # إشعار المشرفين
        if db.settings.get("notify_admin_on_upload", True):
            await notify_admins_pending(pu, context)

    except Exception as e:
        logger.exception("خطأ في رفع الملف: %s", e)
        try: await progress_msg.edit_text(f"𓆩❌𓆪 حدث خطأ: {escape_html(str(e)[:200])}")
        except: pass
        shutil.rmtree(os.path.join(PENDING_DIR, pending_id), ignore_errors=True)


async def notify_admins_pending(pu: PendingUpload, context: ContextTypes.DEFAULT_TYPE) -> None:
    """إرسال إشعار للمشرفين + الملف الأصلي + أزرار قبول/رفض/حظر"""
    text = text_pending_review(pu)
    kb   = kb_pending_admin_plus(pu.pending_id, pu.owner_id)
    caption = (
        f"📦 <b>ملف جديد ينتظر المراجعة</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 المرسل: <code>{pu.owner_id}</code>\n"
        f"📄 الاسم: <code>{escape_html(pu.file_name)}</code>\n"
        f"📊 الحجم: <b>{format_size(pu.size)}</b>\n"
        f"🧬 النوع: <b>{pu.file_type.upper()}</b>\n"
        f"🛡 درجة الأمان: <b>{pu.security_score}/100</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⬇️ الملف مرفق أدناه — افحصه بنفسك ثم اتخذ القرار."
    )
    for adm in ADMIN_IDS:
        try:
            # 1) أرسل التقرير النصي
            await context.bot.send_message(
                adm, text, parse_mode=ParseMode.HTML)
            # 2) أرسل الملف الأصلي كما هو
            try:
                if pu.stored_path and os.path.exists(pu.stored_path):
                    with open(pu.stored_path, "rb") as fh:
                        await context.bot.send_document(
                            adm, document=fh, filename=pu.file_name,
                            caption=caption, parse_mode=ParseMode.HTML,
                            reply_markup=kb,
                        )
                else:
                    await context.bot.send_message(adm, "⚠️ تعذّر العثور على الملف الأصلي.", reply_markup=kb)
            except Exception as e:
                logger.warning("فشل إرسال الملف للمشرف %s: %s", adm, e)
                await context.bot.send_message(adm, f"⚠️ تعذّر إرسال الملف: {e}", reply_markup=kb)
        except Exception as e:
            logger.warning("فشل إشعار المشرف %s: %s", adm, e)


async def _finalize_upload(update: Update, context: ContextTypes.DEFAULT_TYPE,
                            pu: PendingUpload, auto: bool = False,
                            approver_id: int = 0) -> None:
    """نقل الملف من المعلق إلى المستضاف بعد الموافقة"""
    uid   = pu.owner_id
    u     = db.get_user(uid)
    fname = pu.file_name
    ext   = os.path.splitext(fname.lower())[1]

    # إنشاء مجلد العمل
    file_id  = str(uuid.uuid4())[:12]
    work_dir = os.path.join(FILES_DIR, file_id)
    os.makedirs(work_dir, exist_ok=True)

    # نقل الملفات من pending إلى hosted
    src_dir = os.path.dirname(pu.stored_path)
    try:
        for item in os.listdir(src_dir):
            s = os.path.join(src_dir, item)
            d = os.path.join(work_dir, item)
            if os.path.isdir(s): shutil.copytree(s, d)
            else: shutil.copy2(s, d)
    except Exception as e:
        logger.error("فشل نقل ملفات الرفع: %s", e)
        return

    # تحديد نقطة الدخول
    if pu.file_type == "php":
        entry = LibraryDetector.find_php_entry(work_dir) or fname
    else:
        entry = LibraryDetector.find_entry_point(work_dir) if pu.is_zip else fname

    stored_path = os.path.join(work_dir, entry)

    # كتابة requirements إذا لزم
    if pu.file_type == "python" and pu.libraries:
        write_requirements(work_dir, pu.libraries)

    # إنشاء سجل الملف المستضاف
    hf = HostedFile(
        file_id      = file_id,
        file_name    = fname,
        owner_id     = uid,
        upload_date  = now_iso(),
        size         = pu.size,
        libraries    = pu.libraries,
        stored_path  = stored_path,
        entry_file   = entry,
        is_zip       = pu.is_zip,
        file_type    = pu.file_type,
        description  = pu.description,
        ai_analysis  = pu.ai_report[:500] if pu.ai_report else "",
        approved_by  = approver_id or 0,
        approved_at  = now_iso(),
        security_score = pu.security_score,
        security_notes = pu.security_reasons[:300] if pu.security_reasons else "",
    )
    db.add_file(hf)

    # تحديث بيانات المستخدم
    if file_id not in u.files:
        u.files.append(file_id)
    u.total_uploads += 1
    if pu.file_type == "php":
        u.total_php_files += 1
    else:
        u.total_python_files += 1

    cost    = int(db.settings.get("upload_cost", 1))
    is_free = (db.settings.get("first_upload_free", True) and u.free_uploads > 0) or is_admin(uid)
    if is_free and u.free_uploads > 0 and db.settings.get("first_upload_free", True):
        u.free_uploads = max(0, u.free_uploads - 1)
    elif not is_free:
        u.points = max(0, u.points - cost)
    db.update_user(u)
    db.stats["total_runs"] = db.stats.get("total_runs", 0)
    db.log_activity("upload_file", uid, fname)

    # تنظيف الملف المعلق
    shutil.rmtree(src_dir, ignore_errors=True)
    pu.status = "approved"
    db._dirty = True
    db.save(force=True)

    lang_icon = Icon.PHP if pu.file_type == "php" else Icon.PYTHON

    # تشغيل تلقائي إذا كان مفعّلاً
    run_info = ""
    if db.settings.get("auto_run_after_upload", True) and pu.file_type in ("python", "php"):
        if pu.file_type == "python" and pu.libraries and db.settings.get("auto_install_libs", True):
            ok_inst, _ = await asyncio.get_event_loop().run_in_executor(
                None, pm.install_libs, pu.libraries, work_dir)
        ok_run, run_out = pm._run_hosted_file(hf)
        if ok_run:
            hf.run_count += 1; hf.last_run = now_iso(); hf.start_time = now_iso()
            db.add_file(hf)
            run_info = f"\n▶️ <b>تم التشغيل تلقائياً</b> — PID: {run_out}"
        else:
            run_info = f"\n⚠️ التشغيل التلقائي فشل: {escape_html(run_out[:100])}"

    # إشعار المستخدم بالقبول
    if db.settings.get("approval_notify_user", True):
        success_text = (
            f"𓆩✅𓆪 <b>تمت الموافقة على ملفك!</b>\n"
            f"{SEP_STAR}\n"
            f"{lang_icon} الملف: <code>{escape_html(fname)}</code>\n"
            f"الحجم: <b>{format_size(hf.size)}</b>\n"
            f"نقطة الدخول: <code>{escape_html(entry)}</code>"
            f"{run_info}\n"
            f"{SEP_THIN}\n"
            f"يمكنك الآن إدارة الملف من قائمة «ملفاتي»."
        )
        try:
            await context.bot.send_message(
                uid, success_text,
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([
                    [btn_success("▶️  فتح الملف", f"file:open:{file_id}")],
                    [btn_primary("📁  ملفاتي",    "menu:myfiles")],
                ]),
            )
            await send_named_sticker_to_user(uid, context, "upload_success")
        except: pass


async def send_named_sticker_to_user(user_id: int, context: ContextTypes.DEFAULT_TYPE,
                                      name: str) -> None:
    stickers = db.settings.get("stickers") or {}
    file_id  = stickers.get(name) or STICKERS.get(name)
    if not file_id: return
    try: await context.bot.send_sticker(chat_id=user_id, sticker=file_id)
    except: pass


# ──────────────────────────────────────────────────────────────────────────────
# 👑  معالجة موافقة/رفض المشرف
# ──────────────────────────────────────────────────────────────────────────────

@admin_only
async def admin_approve_pending(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                 pending_id: str) -> None:
    """المشرف وافق على الملف"""
    pu = db.get_pending(pending_id)
    if not pu:
        await _edit_or_send(update, f"𓆩❌𓆪 الملف غير موجود أو تمت معالجته.", kb_back("admin:pending"))
        return
    if pu.status != "pending":
        await _edit_or_send(update,
                             f"𓆩ℹ️𓆪 تمت معالجة هذا الملف بالفعل: {pu.status}",
                             kb_back("admin:pending"))
        return

    approver_id = update.effective_user.id
    # نهائي الرفع
    await _finalize_upload(update, context, pu, approver_id=approver_id)
    db.log_activity("approve_pending", approver_id, pu.file_name)

    await _edit_or_send(
        update,
        f"𓆩✅𓆪 <b>تمت الموافقة على الملف</b>\n"
        f"{SEP_THIN}\n"
        f"الملف: <code>{escape_html(pu.file_name)}</code>\n"
        f"المستخدم: <code>{pu.owner_id}</code>",
        InlineKeyboardMarkup([
            [btn_primary("⏳  الملفات المعلقة", "admin:pending")],
            [btn_primary("👑  لوحة الإدارة",    "admin:panel")],
        ]),
    )


@admin_only
async def admin_reject_pending_start(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                      pending_id: str) -> None:
    """المشرف يبدأ عملية الرفض"""
    pu = db.get_pending(pending_id)
    if not pu or pu.status != "pending":
        await _edit_or_send(update, f"𓆩❌𓆪 الملف غير موجود.", kb_back("admin:pending"))
        return
    context.user_data[ST_AWAIT_REJECT_REASON] = pending_id
    await _edit_or_send(
        update,
        f"𓆩❌𓆪 <b>رفض الملف</b>\n"
        f"{SEP_THIN}\n"
        f"الملف: <code>{escape_html(pu.file_name)}</code>\n\n"
        f"أرسل سبب الرفض الآن:",
        InlineKeyboardMarkup([[btn_danger("❌  إلغاء", "admin:pending")]]),
    )


async def admin_reject_do(update: Update, context: ContextTypes.DEFAULT_TYPE,
                           pending_id: str, reason: str) -> None:
    """تنفيذ الرفض"""
    pu = db.get_pending(pending_id)
    if not pu or pu.status != "pending":
        return
    pu.status        = "rejected"
    pu.reviewed_by   = update.effective_user.id
    pu.reviewed_at   = now_iso()
    pu.reject_reason = reason
    db._dirty        = True
    db.save(force=True)

    # حذف الملفات من القرص
    src_dir = os.path.dirname(pu.stored_path)
    shutil.rmtree(src_dir, ignore_errors=True)
    db.log_activity("reject_pending", update.effective_user.id, pu.file_name)

    # إشعار المستخدم بالرفض
    if db.settings.get("approval_notify_user", True):
        lang_icon = Icon.PHP if pu.file_type == "php" else Icon.PYTHON
        reject_text = (
            f"𓆩❌𓆪 <b>تم رفض ملفك</b>\n"
            f"{SEP_MAIN}\n"
            f"{lang_icon} الملف: <code>{escape_html(pu.file_name)}</code>\n"
            f"السبب: <b>{escape_html(reason)}</b>\n"
            f"{SEP_THIN}\n"
            f"للاستفسار: @{db.settings.get('support_username', SUPPORT_USERNAME)}"
        )
        try:
            await context.bot.send_message(
                pu.owner_id, reject_text,
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([
                    [btn_primary("🏠  الرئيسية", "menu:main")],
                ]),
            )
        except: pass

    await update.message.reply_text(
        f"𓆩✅𓆪 تم رفض الملف <code>{escape_html(pu.file_name)}</code>\nالسبب: {escape_html(reason)}",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([
            [btn_primary("⏳  الملفات المعلقة", "admin:pending")],
            [btn_primary("👑  لوحة الإدارة",    "admin:panel")],
        ]),
    )


@admin_only
async def admin_pending_list(update: Update, context: ContextTypes.DEFAULT_TYPE,
                              page: int = 0) -> None:
    """عرض قائمة الملفات المعلقة للمشرف"""
    pending_all = db.all_pending("pending")
    approved    = db.all_pending("approved")
    rejected    = db.all_pending("rejected")

    text = (
        f"𓆩⏳𓆪 <b>إدارة الملفات المعلقة</b>\n"
        f"{SEP_MAIN}\n"
        f"⏳ قيد المراجعة: <b>{len(pending_all)}</b>\n"
        f"✅ مقبولة:       <b>{len(approved)}</b>\n"
        f"❌ مرفوضة:      <b>{len(rejected)}</b>\n"
        f"{SEP_THIN}\n"
    )

    if not pending_all:
        text += "✅ لا توجد ملفات قيد المراجعة حالياً."
        await _edit_or_send(update, text, kb_back("admin:panel"))
        return

    items: List[Tuple[str, str]] = []
    for pu in sorted(pending_all, key=lambda x: x.submitted_at, reverse=True):
        owner = db.users.get(pu.owner_id)
        oname = escape_html(owner.first_name or str(pu.owner_id)) if owner else str(pu.owner_id)
        risk  = "🔴" if pu.security_blocked else ("🟡" if pu.security_warnings else "🟢")
        lang  = "🐘" if pu.file_type == "php" else "🐍"
        label = f"{risk} {lang} {shorten(pu.file_name, 20)} — {oname}"
        items.append((label, f"pending:review:{pu.pending_id}"))

    kb = kb_paginated(items, page, 6, "admin:pending:page", "admin:panel", "success")
    await _edit_or_send(update, text, kb)


async def pending_review_detail(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                  pending_id: str) -> None:
    """عرض تفاصيل ملف معلق"""
    pu = db.get_pending(pending_id)
    if not pu:
        await _edit_or_send(update, f"𓆩❌𓆪 الملف غير موجود.", kb_back("admin:pending"))
        return
    text = text_pending_review(pu)
    kb   = kb_pending_admin(pending_id) if pu.status == "pending" else kb_back("admin:pending")
    await _edit_or_send(update, text, kb)


async def pending_full_report(update: Update, context: ContextTypes.DEFAULT_TYPE,
                               pending_id: str) -> None:
    """عرض التقرير الكامل للملف المعلق"""
    pu = db.get_pending(pending_id)
    if not pu:
        await _edit_or_send(update, f"𓆩❌𓆪 غير موجود.", kb_back("admin:pending"))
        return
    text = text_pending_full_report(pu)
    await _edit_or_send(
        update, text[:4000],
        InlineKeyboardMarkup([
            [btn_success("✅  قبول",   f"approve:{pending_id}"),
             btn_danger ("❌  رفض",    f"reject:{pending_id}")],
            [btn_primary("⬅️  رجوع",   f"pending:review:{pending_id}")],
        ]),
    )


# ──────────────────────────────────────────────────────────────────────────────
# 📁  عرض ملفات المستخدم
# ──────────────────────────────────────────────────────────────────────────────

async def show_my_files(update: Update, context: ContextTypes.DEFAULT_TYPE,
                         page: int = 0) -> None:
    uid   = update.effective_user.id
    u     = db.get_user(uid)
    files = db.user_files(uid)
    text  = (
        f"𓆩📁𓆪 <b>ملفاتك المستضافة</b>\n"
        f"{SEP_MAIN}\n"
        f"المجموع: <b>{len(files)}</b> | "
        f"🐍 Python: <b>{u.total_python_files}</b> | "
        f"🐘 PHP: <b>{u.total_php_files}</b>"
    )
    if not files:
        kb = InlineKeyboardMarkup([
            [btn_success("📤  رفع ملف", "menu:upload")],
            [btn_primary("🏠  الرئيسية", "menu:main")],
        ])
        await _edit_or_send(update, text + "\n\nلا توجد ملفات بعد.", kb)
        return

    items: List[Tuple[str, str]] = []
    for hf in sorted(files, key=lambda x: x.upload_date, reverse=True):
        run_flag  = "▶️" if pm.is_running(hf.file_id) else "⏹"
        lang_flag = "🐘" if hf.file_type == "php" else "🐍"
        label     = f"{run_flag} {lang_flag} {shorten(hf.file_name, 22)} · {format_size(hf.size)}"
        items.append((label, f"file:open:{hf.file_id}"))

    kb = kb_paginated(items, page, 6, "myfiles:page", "menu:main")
    await _edit_or_send(update, text, kb)


async def open_file(update: Update, context: ContextTypes.DEFAULT_TYPE,
                     file_id: str) -> None:
    uid = update.effective_user.id
    hf  = db.get_file(file_id)
    if not hf:
        await _edit_or_send(update, f"𓆩❌𓆪 الملف غير موجود.", kb_back("menu:myfiles"))
        return
    is_owner    = hf.owner_id == uid
    is_adm      = is_admin(uid)
    if not is_owner and not is_adm and not hf.is_public:
        await _edit_or_send(update, f"𓆩🔒𓆪 ليس لديك صلاحية.", kb_back("menu:myfiles"))
        return

    running     = pm.is_running(file_id)
    lang_icon   = Icon.PHP if hf.file_type == "php" else Icon.PYTHON
    status_icon = "▶️ يعمل" if running else "⏹ متوقف"
    owner       = db.users.get(hf.owner_id)
    owner_name  = escape_html(owner.first_name or str(hf.owner_id)) if owner else str(hf.owner_id)
    auto_icon   = "✅" if hf.auto_restart else "❌"
    public_icon = "🌐 عام" if hf.is_public else "🔏 خاص"

    text = (
        f"𓆩{lang_icon}𓆪 <b>{escape_html(hf.file_name)}</b>\n"
        f"{SEP_MAIN}\n"
        f"النوع: <b>{'PHP 🐘' if hf.file_type == 'php' else 'Python 🐍'}</b>\n"
        f"الحالة: <b>{status_icon}</b>\n"
        f"الحجم: <b>{format_size(hf.size)}</b>\n"
        f"صاحب: <b>{owner_name}</b>\n"
        f"نقطة الدخول: <code>{escape_html(hf.entry_file or hf.file_name)}</code>\n"
        f"التشغيلات: <b>{hf.run_count}</b> | التحميلات: <b>{hf.downloads}</b>\n"
        f"إقلاع تلقائي: {auto_icon} | {public_icon}\n"
        f"تاريخ الرفع: {format_dt(hf.upload_date)}\n"
    )
    if running:
        text += f"مدة التشغيل: <b>{pm.uptime(file_id)}</b>\n"
    if hf.description:
        text += f"{SEP_THIN}\n📝 {escape_html(hf.description)}\n"
    if hf.libraries:
        text += f"{SEP_THIN}\n📦 المكتبات: {escape_html(', '.join(hf.libraries[:8]))}\n"

    kb = kb_file_actions(file_id, is_owner, running, is_adm)
    await _edit_or_send(update, text, kb)


# ──────────────────────────────────────────────────────────────────────────────
# 🎛  إجراءات الملفات
# ──────────────────────────────────────────────────────────────────────────────

async def file_run(update: Update, context: ContextTypes.DEFAULT_TYPE,
                    file_id: str) -> None:
    uid = update.effective_user.id
    hf  = db.get_file(file_id)
    if not hf or (hf.owner_id != uid and not is_admin(uid)):
        await _edit_or_send(update, f"𓆩🚫𓆪 لا يمكنك.", kb_back("menu:myfiles"))
        return
    if pm.is_running(file_id):
        await _edit_or_send(update, f"𓆩▶️𓆪 العملية تعمل بالفعل.", kb_back(f"file:open:{file_id}"))
        return

    u = db.get_user(uid)
    # تثبيت مكتبات Python تلقائياً إذا لزم
    if hf.file_type == "python" and hf.libraries and db.settings.get("auto_install_libs", True):
        work_dir = os.path.dirname(hf.stored_path) or os.path.join(FILES_DIR, file_id)
        await asyncio.get_event_loop().run_in_executor(None, pm.install_libs, hf.libraries, work_dir)

    ok, info = pm._run_hosted_file(hf)
    if ok:
        hf.run_count += 1; hf.last_run = now_iso(); hf.start_time = now_iso()
        hf.process_id = pm.pid(file_id)
        db.add_file(hf)
        u.total_runs += 1
        db.update_user(u, save=False)
        db.stats["total_runs"] = db.stats.get("total_runs", 0) + 1
        await send_named_sticker(update, context, "hosting_started")
        text = (
            f"𓆩▶️𓆪 <b>تم التشغيل بنجاح!</b>\n"
            f"{SEP_THIN}\n"
            f"الملف: <code>{escape_html(hf.file_name)}</code>\n"
            f"{info}"
        )
    else:
        text = f"𓆩❌𓆪 <b>فشل التشغيل</b>\n{SEP_THIN}\n{escape_html(info[:300])}"
    await _edit_or_send(update, text, kb_back(f"file:open:{file_id}"))


async def file_stop(update: Update, context: ContextTypes.DEFAULT_TYPE,
                     file_id: str) -> None:
    uid = update.effective_user.id
    hf  = db.get_file(file_id)
    if not hf or (hf.owner_id != uid and not is_admin(uid)):
        await _edit_or_send(update, f"𓆩🚫𓆪 لا يمكنك.", kb_back("menu:myfiles"))
        return
    stopped = pm.stop(file_id)
    hf.last_stop = now_iso()
    db.add_file(hf)
    text = (f"𓆩⏹𓆪 <b>تم الإيقاف.</b>" if stopped else
            f"𓆩ℹ️𓆪 العملية لم تكن تعمل.")
    await _edit_or_send(update, text, kb_back(f"file:open:{file_id}"))


async def file_restart(update: Update, context: ContextTypes.DEFAULT_TYPE,
                        file_id: str) -> None:
    uid = update.effective_user.id
    hf  = db.get_file(file_id)
    if not hf or (hf.owner_id != uid and not is_admin(uid)):
        await _edit_or_send(update, f"𓆩🚫𓆪 لا يمكنك.", kb_back("menu:myfiles"))
        return
    ok, info = pm.restart(file_id)
    if ok:
        hf.run_count += 1; hf.last_run = now_iso(); hf.start_time = now_iso()
        db.add_file(hf)
    text = (f"𓆩🔄𓆪 <b>إعادة التشغيل ناجحة!</b>\n{escape_html(info)}"
            if ok else f"𓆩❌𓆪 فشلت إعادة التشغيل: {escape_html(info)}")
    await _edit_or_send(update, text, kb_back(f"file:open:{file_id}"))


async def file_log(update: Update, context: ContextTypes.DEFAULT_TYPE,
                    file_id: str) -> None:
    uid = update.effective_user.id
    hf  = db.get_file(file_id)
    if not hf or (hf.owner_id != uid and not is_admin(uid)):
        await _edit_or_send(update, f"𓆩🚫𓆪 لا يمكنك.", kb_back("menu:myfiles"))
        return
    tail    = pm.tail_log(file_id, 50)
    if len(tail) > 3500: tail = "…" + tail[-3500:]
    running = pm.is_running(file_id)
    lang    = "PHP 🐘" if hf.file_type == "php" else "Python 🐍"
    text    = (
        f"𓆩📺𓆪 <b>سجل التشغيل — آخر 50 سطر</b>\n"
        f"{SEP_THIN}\n"
        f"النوع: {lang} | الحالة: {'▶️ يعمل · ' + pm.uptime(file_id) if running else '⏹ متوقف'}\n"
        f"{SEP_THIN}\n"
        f"<pre>{escape_html(tail or 'لا يوجد سجل')}</pre>"
    )
    kb = InlineKeyboardMarkup([
        [btn_primary("🔁  تحديث",   f"file:log:{file_id}"),
         btn_primary("📤  تصدير",   f"file:export_log:{file_id}")],
        [btn_secondary("⬅️  رجوع", f"file:open:{file_id}")],
    ])
    await _edit_or_send(update, text, kb)


async def file_export_log(update: Update, context: ContextTypes.DEFAULT_TYPE,
                           file_id: str) -> None:
    uid = update.effective_user.id
    hf  = db.get_file(file_id)
    if not hf or (hf.owner_id != uid and not is_admin(uid)):
        await _edit_or_send(update, f"𓆩🚫𓆪 لا يمكنك.", kb_back("menu:myfiles"))
        return
    log_bytes = pm.export_log(file_id)
    fname     = f"log_{file_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    try:
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=InputFile(io.BytesIO(log_bytes), filename=fname),
            caption=(
                f"𓆩📤𓆪 <b>سجل التشغيل</b>\n"
                f"الملف: <code>{escape_html(hf.file_name)}</code>"
            ),
            parse_mode=ParseMode.HTML,
        )
    except Exception as e:
        await _reply_anywhere(update, f"𓆩❌𓆪 فشل التصدير: {e}")


async def file_install(update: Update, context: ContextTypes.DEFAULT_TYPE,
                        file_id: str) -> None:
    uid = update.effective_user.id
    hf  = db.get_file(file_id)
    if not hf or (hf.owner_id != uid and not is_admin(uid)):
        await _edit_or_send(update, f"𓆩🚫𓆪 لا يمكنك.", kb_back("menu:myfiles"))
        return
    work_dir = os.path.dirname(hf.stored_path) or os.path.join(FILES_DIR, file_id)

    if hf.file_type == "php":
        msg = await _reply_anywhere(
            update,
            f"𓆩💡𓆪 جاري تثبيت حزم Composer لـ PHP...")
        await send_named_sticker(update, context, "installing_libs")
        ok, out = await asyncio.get_event_loop().run_in_executor(None, pm.install_composer, work_dir)
        hf.install_log = out
        db.add_file(hf)
        text = (f"{'𓆩✅𓆪 تم التثبيت!' if ok else '𓆩❌𓆪 فشل التثبيت'}\n<pre>{escape_html(out[-2000:])}</pre>")
        await _edit_or_send(update, text, kb_back(f"file:open:{file_id}"))
        return

    libs = LibraryDetector.detect_from_directory(work_dir)
    hf.libraries = libs
    if libs: write_requirements(work_dir, libs)
    if not libs:
        await _edit_or_send(update, f"𓆩ℹ️𓆪 لا توجد مكتبات خارجية.", kb_back(f"file:open:{file_id}"))
        return
    msg = await _reply_anywhere(update, f"𓆩💡𓆪 جاري تثبيت {len(libs)} مكتبة Python...")
    await send_named_sticker(update, context, "installing_libs")
    ok, out = await asyncio.get_event_loop().run_in_executor(None, pm.install_libs, libs, work_dir)
    hf.install_log = out
    db.add_file(hf)
    snippet = out[-2000:] if out else ""
    text = (
        f"{'𓆩✅𓆪 تم التثبيت بنجاح!' if ok else '𓆩❌𓆪 فشل التثبيت'}\n"
        f"المكتبات: {escape_html(', '.join(libs[:10]))}\n"
        f"<pre>{escape_html(snippet)}</pre>"
    )
    await _edit_or_send(update, text, kb_back(f"file:open:{file_id}"))


async def file_ai_analyze(update: Update, context: ContextTypes.DEFAULT_TYPE,
                           file_id: str) -> None:
    uid = update.effective_user.id
    hf  = db.get_file(file_id)
    if not hf or (hf.owner_id != uid and not is_admin(uid)):
        await _edit_or_send(update, f"𓆩🚫𓆪 لا يمكنك.", kb_back("menu:myfiles"))
        return
    work_dir = os.path.dirname(hf.stored_path) or os.path.join(FILES_DIR, file_id)
    if hf.is_zip:
        result = await asyncio.get_event_loop().run_in_executor(
            None, AICodeAnalyzer.analyze_directory, work_dir)
    else:
        result = await asyncio.get_event_loop().run_in_executor(
            None, AICodeAnalyzer.analyze_file, hf.stored_path)
    report  = AICodeAnalyzer.format_report(result, hf.file_name)
    hf.ai_analysis = result.summary
    db.add_file(hf)
    await send_named_sticker(update, context, "ai_analysis")
    await _edit_or_send(update, report[:4096], kb_back(f"file:open:{file_id}"))


async def file_delete_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE,
                               file_id: str) -> None:
    uid = update.effective_user.id
    hf  = db.get_file(file_id)
    if not hf or (hf.owner_id != uid and not is_admin(uid)):
        await _edit_or_send(update, f"𓆩🚫𓆪 لا يمكنك.", kb_back("menu:myfiles"))
        return
    text = (
        f"𓆩⚠️𓆪 <b>تأكيد الحذف</b>\n"
        f"{SEP_THIN}\n"
        f"سيُحذف <code>{escape_html(hf.file_name)}</code> نهائياً."
    )
    await _edit_or_send(update, text, kb_confirm(f"file:del_yes:{file_id}", f"file:open:{file_id}"))


async def file_delete_do(update: Update, context: ContextTypes.DEFAULT_TYPE,
                          file_id: str) -> None:
    uid = update.effective_user.id
    hf  = db.get_file(file_id)
    if not hf:
        await _edit_or_send(update, f"𓆩❌𓆪 الملف غير موجود.", kb_back("menu:myfiles"))
        return
    if hf.owner_id != uid and not is_admin(uid):
        await _edit_or_send(update, f"𓆩🚫𓆪 لا يمكنك.", kb_back("menu:myfiles"))
        return
    pm.stop(file_id)
    work_dir = os.path.dirname(hf.stored_path) or os.path.join(FILES_DIR, file_id)
    shutil.rmtree(work_dir, ignore_errors=True)
    db.remove_file(file_id)
    db.log_activity("delete_file", uid, hf.file_name)
    await _edit_or_send(update, f"𓆩✅𓆪 تم الحذف بنجاح.", kb_back("menu:myfiles"))


async def file_zip(update: Update, context: ContextTypes.DEFAULT_TYPE,
                    file_id: str) -> None:
    hf = db.get_file(file_id)
    if not hf:
        await _edit_or_send(update, f"𓆩❌𓆪 الملف غير موجود.", kb_back("menu:myfiles"))
        return
    await _send_project_zip_direct(update, context, hf, "طلب تحميل")


async def _send_project_zip_direct(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                    hf: HostedFile, reason: str = "") -> None:
    work_dir = os.path.dirname(hf.stored_path) or os.path.join(FILES_DIR, hf.file_id)
    if hf.file_type == "python" and hf.libraries:
        write_requirements(work_dir, hf.libraries)
    out_zip = os.path.join(TEMP_DIR, f"{hf.file_id}_{int(time.time())}.zip")
    try:
        make_zip_of_dir(work_dir, out_zip)
    except Exception as e:
        await _reply_anywhere(update, f"𓆩❌𓆪 تعذر إنشاء ZIP: {e}")
        return
    lang_icon = Icon.PHP if hf.file_type == "php" else Icon.PYTHON
    caption   = (
        f"𓆩📥𓆪 <b>ملف المشروع</b>\n"
        f"{lang_icon} الملف: <code>{escape_html(hf.file_name)}</code>\n"
        f"الحجم: {format_size(os.path.getsize(out_zip))}\n"
        f"السبب: {escape_html(reason or 'تحميل')}"
    )
    try:
        chat = update.effective_chat
        await chat.send_action(ChatAction.UPLOAD_DOCUMENT)
        with open(out_zip, "rb") as f:
            await context.bot.send_document(
                chat_id=chat.id,
                document=InputFile(f, filename=f"{os.path.splitext(hf.file_name)[0]}.zip"),
                caption=caption, parse_mode=ParseMode.HTML,
            )
        hf.downloads += 1
        db.stats["total_downloads"] = db.stats.get("total_downloads", 0) + 1
        owner = db.users.get(hf.owner_id)
        if owner: owner.total_downloads += 1; db.update_user(owner, save=False)
        db.add_file(hf)
        await send_named_sticker(update, context, "share_link")
    except Exception as e:
        await _reply_anywhere(update, f"𓆩❌𓆪 فشل إرسال الملف: {e}")
    finally:
        try: os.remove(out_zip)
        except: pass


async def file_toggle_auto(update: Update, context: ContextTypes.DEFAULT_TYPE,
                            file_id: str) -> None:
    uid = update.effective_user.id
    hf  = db.get_file(file_id)
    if not hf or (hf.owner_id != uid and not is_admin(uid)):
        await _edit_or_send(update, f"𓆩🚫𓆪 لا يمكنك.", kb_back("menu:myfiles"))
        return
    hf.auto_restart = not hf.auto_restart
    db.add_file(hf)
    await open_file(update, context, file_id)


async def file_toggle_public(update: Update, context: ContextTypes.DEFAULT_TYPE,
                              file_id: str) -> None:
    uid = update.effective_user.id
    hf  = db.get_file(file_id)
    if not hf or (hf.owner_id != uid and not is_admin(uid)):
        await _edit_or_send(update, f"𓆩🚫𓆪 لا يمكنك.", kb_back("menu:myfiles"))
        return
    if not db.settings.get("public_files_enabled", True) and not is_admin(uid):
        await _edit_or_send(update, f"𓆩⚠️𓆪 الملفات العامة معطّلة.", kb_back(f"file:open:{file_id}"))
        return
    hf.is_public = not hf.is_public
    db.add_file(hf)
    await open_file(update, context, file_id)


async def file_share(update: Update, context: ContextTypes.DEFAULT_TYPE,
                      file_id: str) -> None:
    hf = db.get_file(file_id)
    if not hf:
        await _edit_or_send(update, f"𓆩❌𓆪 الملف غير موجود.", kb_back("menu:myfiles"))
        return
    me   = await context.bot.get_me()
    link = f"https://t.me/{me.username}?start=file_{file_id}"
    text = (
        f"𓆩🔗𓆪 <b>رابط مشاركة الملف</b>\n"
        f"{SEP_MAIN}\n"
        f"<code>{link}</code>\n\n"
        f"{'🌐 الملف عام — يمكن لأي شخص تحميله.' if hf.is_public else '🔏 الملف خاص — فقط أنت تستطيع تحميله.'}"
    )
    share_text = urllib.parse.quote(f"استخدم هذا الرابط لتحميل ملفي: {link}")
    kb = InlineKeyboardMarkup([
        [btn_url_primary("🔗  مشاركة عبر تيليجرام",
                         f"https://t.me/share/url?url={urllib.parse.quote(link)}&text={share_text}")],
        [btn_secondary("⬅️  رجوع", f"file:open:{file_id}")],
    ])
    await _edit_or_send(update, text, kb)


async def file_desc_start(update: Update, context: ContextTypes.DEFAULT_TYPE,
                           file_id: str) -> None:
    context.user_data[ST_AWAIT_FILE_DESC] = file_id
    await _edit_or_send(
        update, f"𓆩✏️𓆪 أرسل وصفاً جديداً للملف:",
        InlineKeyboardMarkup([[btn_danger("❌  إلغاء", f"file:open:{file_id}")]]),
    )


# ══════════════════════════════════════════════════════════════════════════════
# 💳  شراء النقاط
# ══════════════════════════════════════════════════════════════════════════════

async def show_buy_points(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    u    = db.get_user(update.effective_user.id)
    text = (
        f"𓆩⭐𓆪 <b>شراء نقاط بنجوم تيليجرام</b>\n"
        f"{SEP_MAIN}\n"
        f"رصيدك الحالي: <b>{u.points}</b> نقطة\n\n"
        f"اختر الباقة المناسبة:"
    )
    await _edit_or_send(update, text, kb_buy_points())


async def initiate_purchase(update: Update, context: ContextTypes.DEFAULT_TYPE,
                              points: int, stars: int) -> None:
    user = update.effective_user
    chat = update.effective_chat
    try:
        prices  = [LabeledPrice(label=f"{points} نقطة", amount=stars)]
        payload = f"pts_{user.id}_{points}_{int(time.time())}"
        db.pending_payments[user.id] = {
            "payload": payload, "points": points, "stars": stars, "created": now_iso(),
        }
        await context.bot.send_invoice(
            chat_id=chat.id, title=f"{points} نقطة",
            description=f"شراء {points} نقطة لاستخدامها في استضافة الملفات.",
            payload=payload, provider_token=PAYMENT_PROVIDER_TOKEN,
            currency="XTR", prices=prices, start_parameter=f"buy{points}",
        )
    except Exception as e:
        await _reply_anywhere(update, f"𓆩❌𓆪 تعذر إنشاء الفاتورة: {e}")


async def precheckout_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    q       = update.pre_checkout_query
    pending = db.pending_payments.get(q.from_user.id)
    if not pending or pending.get("payload") != q.invoice_payload:
        await q.answer(ok=False, error_message="انتهت صلاحية الفاتورة. أعد المحاولة.")
        return
    await q.answer(ok=True)


async def successful_payment_handler(update: Update,
                                      context: ContextTypes.DEFAULT_TYPE) -> None:
    msg     = update.message
    payment = msg.successful_payment
    user    = update.effective_user
    pending = db.pending_payments.pop(user.id, None) or {}
    points  = int(pending.get("points") or 0)
    stars   = int(payment.total_amount or pending.get("stars") or 0)
    u       = db.get_user(user.id)
    if points <= 0:
        m = re.match(r"pts_(\d+)_(\d+)_", payment.invoice_payload or "")
        if m: points = int(m.group(2))
    if points > 0:
        grant_points(u, points, "purchase", note=f"stars={stars}")
        u.purchases_total_stars += stars
        db.stats["total_stars_received"] = db.stats.get("total_stars_received", 0) + stars
        db.update_user(u)
    await send_named_sticker(update, context, "points_added")
    await msg.reply_text(
        f"𓆩✅𓆪 <b>تم الدفع بنجاح!</b>\n"
        f"{SEP_THIN}\n"
        f"أُضيفت <b>{points}</b> نقطة ⭐\n"
        f"رصيدك الآن: <b>{u.points}</b>",
        reply_markup=InlineKeyboardMarkup([[btn_primary("💎  نقاطي", "menu:points")]]),
        parse_mode=ParseMode.HTML,
    )
    for adm in ADMIN_IDS:
        try:
            await context.bot.send_message(
                adm,
                f"𓆩⭐𓆪 <b>دفعة جديدة</b>\n"
                f"ID: <code>{user.id}</code> ({escape_html(user.first_name or '')})\n"
                f"النقاط: <b>{points}</b> | النجوم: <b>{stars}</b>",
                parse_mode=ParseMode.HTML,
            )
        except: pass


# ══════════════════════════════════════════════════════════════════════════════
# 🌟  ميزات المستخدم (النقاط، الدعوة، الإحصائيات...)
# ══════════════════════════════════════════════════════════════════════════════

async def show_points(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    u   = db.get_user(update.effective_user.id)
    prem= " (بريميوم — رفع مجاني)" if u.is_premium else ""
    text = (
        f"𓆩💎𓆪 <b>نقاطك</b>\n"
        f"{SEP_MAIN}\n"
        f"رصيد النقاط:     <b>{u.points}</b>\n"
        f"رفع مجاني متبقي: <b>{u.free_uploads}</b>{prem}\n"
        f"إجمالي ما ربحته: <b>{u.total_points_earned}</b>\n"
        f"النجوم المدفوعة: <b>{u.purchases_total_stars}</b>"
    )
    kb = InlineKeyboardMarkup([
        [btn_warning("⭐  شراء نقاط",   "menu:buy"),
         btn_success("🎁  دعوة أصدقاء", "menu:invite")],
        [btn_primary("💻  استرداد كود",  "menu:redeem")],
        [btn_secondary("⬅️  الرئيسية",  "menu:main")],
    ])
    await _edit_or_send(update, text, kb)


async def show_invite(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    u    = db.get_user(update.effective_user.id)
    me   = await context.bot.get_me()
    link = f"https://t.me/{me.username}?start=ref{u.user_id}"
    share_text = urllib.parse.quote(f"جرّب بوت استضافة Python و PHP الأقوى! {link}")
    text = (
        f"𓆩🎁𓆪 <b>ادعُ أصدقاءك واربح نقاطاً</b>\n"
        f"{SEP_MAIN}\n"
        f"بكل صديق جديد ينضم عبر رابطك تحصل على\n"
        f"<b>{db.settings.get('points_per_invite', 2)}</b> نقطة 🎉\n\n"
        f"𓆩🔗𓆪 رابطك الخاص:\n<code>{link}</code>\n\n"
        f"دعوات ناجحة: <b>{len(u.invited_users)}</b>"
    )
    kb = InlineKeyboardMarkup([
        [btn_url_success("🔗  مشاركة الرابط",
                         f"https://t.me/share/url?url={urllib.parse.quote(link)}&text={share_text}")],
        [btn_secondary("⬅️  الرئيسية", "menu:main")],
    ])
    await send_named_sticker(update, context, "share_link")
    await _edit_or_send(update, text, kb)


async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    u          = db.get_user(update.effective_user.id)
    files_run  = sum(1 for fid in u.files if pm.is_running(fid))
    pending_ct = db.user_pending_count(u.user_id)
    text = (
        f"𓆩📊𓆪 <b>إحصائياتك</b>\n"
        f"{SEP_MAIN}\n"
        f"المعرّف: <code>{u.user_id}</code>\n"
        f"الانضمام: {format_dt(u.join_date)}\n"
        f"آخر نشاط: {humanize_delta(u.last_active)}\n"
        f"مرات الدخول: <b>{u.login_count}</b>\n"
        f"{SEP_THIN}\n"
        f"📤 الرفع: <b>{u.total_uploads}</b>\n"
        f"  🐍 Python: <b>{u.total_python_files}</b>\n"
        f"  🐘 PHP: <b>{u.total_php_files}</b>\n"
        f"  ⏳ قيد المراجعة: <b>{pending_ct}</b>\n"
        f"▶️ التشغيل: <b>{u.total_runs}</b> (يعمل: {files_run})\n"
        f"📥 التحميلات: <b>{u.total_downloads}</b>\n"
        f"{SEP_THIN}\n"
        f"💎 النقاط: <b>{u.points}</b>\n"
        f"🎁 الدعوات: <b>{len(u.invited_users)}</b>\n"
        f"📁 الملفات: <b>{len(u.files)}</b>\n"
        f"⚡ انتهاكات Rate: <b>{u.rate_violations}</b>"
    )
    await _edit_or_send(update, text,
                        InlineKeyboardMarkup([[btn_secondary("⬅️  الرئيسية", "menu:main")]]))


async def show_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE,
                            category: str = "points") -> None:
    if not db.settings.get("leaderboard_enabled", True):
        await _edit_or_send(update, f"𓆩ℹ️𓆪 المتصدرون معطّلون.", kb_back("menu:main"))
        return
    text = text_leaderboard(category)
    kb   = InlineKeyboardMarkup([
        [btn_primary("💎  النقاط",   "leaderboard:points"),
         btn_primary("📤  الرفع",    "leaderboard:uploads"),
         btn_primary("🎁  الدعوات",  "leaderboard:invites")],
        [btn_secondary("⬅️  الرئيسية", "menu:main")],
    ])
    await send_named_sticker(update, context, "leaderboard")
    await _edit_or_send(update, text, kb)


async def show_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    u    = db.get_user(update.effective_user.id)
    prem = f" · بريميوم حتى {format_dt(u.premium_until)}" if u.is_premium else ""
    text = (
        f"𓆩⚙️𓆪 <b>إعداداتك</b>\n"
        f"{SEP_MAIN}\n"
        f"الإشعارات: <b>{'مفعّلة ✅' if u.notifications_enabled else 'معطّلة ❌'}</b>{prem}"
    )
    await _edit_or_send(update, text, kb_settings_user(u))


async def show_support(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    sup  = db.settings.get("support_username") or SUPPORT_USERNAME
    text = (
        f"𓆩💬𓆪 <b>الدعم الفني</b>\n"
        f"{SEP_MAIN}\n"
        f"للتواصل مع الإدارة والمساعدة:"
    )
    rows: List[List[InlineKeyboardButton]] = []
    if sup:
        rows.append([btn_url_primary(f"💬  تواصل @{sup}", f"https://t.me/{sup}")])
    rows.append([btn_secondary("⬅️  الرئيسية", "menu:main")])
    await _edit_or_send(update, text, InlineKeyboardMarkup(rows))


async def show_about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _edit_or_send(update, text_about(),
                        InlineKeyboardMarkup([[btn_secondary("⬅️  الرئيسية", "menu:main")]]))


async def show_security_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    approval_status = "✅ مفعّل" if db.settings.get("require_admin_approval", True) else "❌ معطّل"
    php_status      = "✅ مدعوم" if db.settings.get("php_support_enabled", True) else "❌ معطّل"
    text = (
        f"𓆩🛡𓆪 <b>مركز الحماية</b>\n"
        f"{SEP_MAIN}\n"
        f"𓆩🔐𓆪 يمنع سرقة توكن البوت ومفاتيح API\n"
        f"𓆩🛡𓆪 يكشف محاولات استخراج بيانات الاعتماد\n"
        f"𓆩🔎𓆪 يفحص الكود قبل الاستضافة\n"
        f"𓆩🧠𓆪 الذكاء الاصطناعي يحلل تلقائياً\n"
        f"𓆩👑𓆪 المشرفون محميون دائماً\n"
        f"{SEP_THIN}\n"
        f"⏳ نظام الموافقة الإدارية: <b>{approval_status}</b>\n"
        f"🐘 دعم PHP: <b>{php_status}</b>"
    )
    await _edit_or_send(update, text,
                        InlineKeyboardMarkup([[btn_secondary("⬅️  الرئيسية", "menu:main")]]))


async def show_pending_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """عرض ملفات المستخدم قيد المراجعة"""
    uid     = update.effective_user.id
    pending = [pu for pu in db.pending_uploads.values() if pu.owner_id == uid]
    if not pending:
        text = (
            f"𓆩⏳𓆪 <b>الملفات قيد المراجعة</b>\n"
            f"{SEP_THIN}\n"
            f"لا توجد ملفات قيد المراجعة حالياً. ✅"
        )
        await _edit_or_send(update, text, kb_back("menu:main"))
        return

    text = (
        f"𓆩⏳𓆪 <b>ملفاتك قيد المراجعة</b>\n"
        f"{SEP_MAIN}\n"
        f"المجموع: <b>{len(pending)}</b>\n"
        f"⏳ قيد المراجعة: <b>{sum(1 for p in pending if p.status == 'pending')}</b>\n"
        f"✅ مقبولة: <b>{sum(1 for p in pending if p.status == 'approved')}</b>\n"
        f"❌ مرفوضة: <b>{sum(1 for p in pending if p.status == 'rejected')}</b>"
    )
    await _edit_or_send(update, text, kb_pending_user_list(uid))


async def redeem_code_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data[ST_AWAIT_CODE_REDEEM] = True
    await _edit_or_send(
        update, f"𓆩💻𓆪 أرسل كود النقاط:",
        InlineKeyboardMarkup([[btn_danger("❌  إلغاء", "menu:points")]]),
    )


async def redeem_code_do(update: Update, context: ContextTypes.DEFAULT_TYPE,
                          raw: str) -> None:
    context.user_data.pop(ST_AWAIT_CODE_REDEEM, None)
    code  = raw.strip().upper()
    promo = db.promo_codes.get(code)
    u     = db.get_user(update.effective_user.id)
    if not promo or not promo.get("active", True):
        await update.message.reply_text(f"𓆩❌𓆪 الكود غير صحيح أو متوقف.")
        return
    used_by = promo.setdefault("used_by", [])
    limit   = int(promo.get("limit", 1))
    if u.user_id in used_by:
        await update.message.reply_text(f"𓆩ℹ️𓆪 استخدمت هذا الكود من قبل.")
        return
    if len(used_by) >= limit:
        await update.message.reply_text(f"𓆩⚠️𓆪 انتهى حد استخدام هذا الكود.")
        return
    points = int(promo.get("points", 0))
    if points <= 0:
        await update.message.reply_text(f"𓆩❌𓆪 الكود لا يحتوي نقاطاً.")
        return
    used_by.append(u.user_id)
    grant_points(u, points, "admin", note=f"promo:{code}")
    if not u.access_unlocked:
        u.access_unlocked   = True
        u.access_source     = "promo_key"
        u.access_granted_at = now_iso()
    db.update_user(u, save=False)
    db.save(force=True)
    await send_named_sticker(update, context, "points_added")
    await update.message.reply_text(
        f"𓆩✅𓆪 <b>تم تفعيل الكود</b>\n"
        f"الكود: <code>{escape_html(code)}</code>\n"
        f"النقاط: <b>+{points}</b> ⭐\n"
        f"رصيدك الآن: <b>{u.points}</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([[btn_primary("💎  نقاطي", "menu:points")]]),
    )


# ══════════════════════════════════════════════════════════════════════════════
# 👑  لوحة الإدارة
# ══════════════════════════════════════════════════════════════════════════════

@admin_only
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pending_count = len(db.all_pending("pending"))
    pending_badge = f" 🔴 ({pending_count})" if pending_count > 0 else " ✅"
    text = (
        f"𓆩👑𓆪 <b>لوحة الإدارة</b>{pending_badge}\n"
        f"{SEP_DOUBLE}\n"
        f"مرحباً يا مشرف! اختر من القائمة:"
    )
    await _edit_or_send(update, text, kb_admin_panel())


@admin_only
async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _edit_or_send(
        update, text_admin_stats(),
        InlineKeyboardMarkup([
            [btn_primary("🔁  تحديث",          "admin:stats")],
            [btn_secondary("⬅️  لوحة الإدارة", "admin:panel")],
        ]),
    )


@admin_only
async def admin_users(update: Update, context: ContextTypes.DEFAULT_TYPE,
                       page: int = 0) -> None:
    users = sorted(db.all_users(), key=lambda x: x.last_active, reverse=True)
    items: List[Tuple[str, str]] = []
    for u in users:
        flag  = ("👑" if is_admin(u.user_id) else
                 "💫" if u.is_premium else
                 "🚫" if u.is_banned else "👤")
        label = f"{flag} [{u.user_id}] {shorten(u.first_name or str(u.user_id), 16)} · {u.points}pts"
        items.append((label, f"admin:user:{u.user_id}"))
    kb   = kb_paginated(items, page, 8, "admin:users:page", "admin:panel")
    text = f"𓆩👥𓆪 <b>المستخدمون ({len(users)})</b>"
    await _edit_or_send(update, text, kb)


@admin_only
async def admin_user_details(update: Update, context: ContextTypes.DEFAULT_TYPE,
                              uid: int) -> None:
    u = db.users.get(uid)
    if not u:
        await _edit_or_send(update, f"𓆩❌𓆪 مستخدم غير موجود.", kb_back("admin:panel"))
        return
    files_list = db.user_files(uid)
    running    = sum(1 for f in files_list if pm.is_running(f.file_id))
    pending    = db.user_pending_count(uid)
    badges     = []
    if is_admin(uid):  badges.append("👑 مشرف")
    if u.is_premium:   badges.append("💫 بريميوم")
    if u.is_banned:    badges.append("🚫 محظور")
    badge_str  = " | ".join(badges) if badges else "👤 عادي"
    text = (
        f"𓆩👤𓆪 <b>تفاصيل المستخدم</b>\n"
        f"{SEP_MAIN}\n"
        f"ID:            <code>{u.user_id}</code>\n"
        f"الاسم:         <b>{escape_html(u.first_name or '—')}</b>\n"
        f"يوزرنيم:       @{escape_html(u.username or '—')}\n"
        f"الحالة:        {badge_str}\n"
        f"نقاط:          <b>{u.points}</b>\n"
        f"دعوات:         <b>{len(u.invited_users)}</b>\n"
        f"رفع كلي:       <b>{u.total_uploads}</b> (🐍{u.total_python_files} | 🐘{u.total_php_files})\n"
        f"ملفات:         <b>{len(files_list)}</b> (يعمل: {running})\n"
        f"قيد المراجعة:  <b>{pending}</b>\n"
        f"انضمام:        {format_dt(u.join_date)}\n"
        f"آخر نشاط:      {humanize_delta(u.last_active)}\n"
        f"ملاحظة:        {escape_html(u.notes or '—')}"
    )
    rows = [
        [btn_success("➕  +نقاط",             f"admin:addpts_user:{uid}"),
         btn_danger ("➖  -نقاط",             f"admin:subpts_user:{uid}")],
        [btn_danger ("🚫  حظر",               f"admin:ban_user:{uid}"),
         btn_success("🟢  فك الحظر",          f"admin:unban_user:{uid}")],
        
        [btn_primary(f"📁  ملفاته ({len(files_list)})", f"admin:user_files:{uid}"),
         btn_primary("📝  ملاحظة",            f"admin:note_user:{uid}")],
        [btn_success("🔓  منح وصول",         f"admin:grant_access:{uid}"),
         btn_danger ("🔒  سحب وصول",         f"admin:revoke_access:{uid}")],
        [btn_secondary("⬅️  رجوع", "admin:panel")],
    ]
    await _edit_or_send(update, text, InlineKeyboardMarkup(rows))


@admin_only
async def admin_files(update: Update, context: ContextTypes.DEFAULT_TYPE,
                       page: int = 0) -> None:
    files = db.all_files_sorted()
    items: List[Tuple[str, str]] = []
    for f in files:
        flag  = "▶️" if pm.is_running(f.file_id) else "⏹"
        lang  = "🐘" if f.file_type == "php" else "🐍"
        owner = db.users.get(f.owner_id)
        ownr  = f"@{owner.username}" if owner and owner.username else str(f.owner_id)
        items.append((f"{flag} {lang} {shorten(f.file_name, 20)} · {format_size(f.size)} · {ownr}",
                      f"file:open:{f.file_id}"))
    kb   = kb_paginated(items, page, 8, "admin:files:page", "admin:panel")
    py_c = sum(1 for f in files if f.file_type == "python")
    ph_c = sum(1 for f in files if f.file_type == "php")
    await _edit_or_send(update,
                         f"𓆩📁𓆪 <b>كل الملفات ({len(files)})</b>\n"
                         f"🐍 Python: {py_c} | 🐘 PHP: {ph_c}", kb)


@admin_only
async def admin_user_files_list(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                 uid: int, page: int = 0) -> None:
    files = db.user_files(uid)
    u     = db.users.get(uid)
    uname = escape_html(u.first_name or str(uid)) if u else str(uid)
    if not files:
        await _edit_or_send(
            update, f"𓆩📁𓆪 <b>ملفات {uname}</b>\nلا توجد ملفات.",
            InlineKeyboardMarkup([[btn_secondary("⬅️  رجوع", f"admin:user:{uid}")]]),
        )
        return
    items: List[Tuple[str, str]] = []
    for f in sorted(files, key=lambda x: x.upload_date, reverse=True):
        flag = "▶️" if pm.is_running(f.file_id) else "⏹"
        lang = "🐘" if f.file_type == "php" else "🐍"
        items.append((f"{flag} {lang} {shorten(f.file_name, 26)} · {format_size(f.size)}", f"file:open:{f.file_id}"))
    kb   = kb_paginated(items, page, 8, f"admin:user_files_page:{uid}", f"admin:user:{uid}")
    total_size = sum(f.size for f in files)
    text = (
        f"𓆩📁𓆪 <b>ملفات {uname}</b>\n{SEP_THIN}\n"
        f"ID: <code>{uid}</code>\n"
        f"العدد: <b>{len(files)}</b> | الحجم: <b>{format_size(total_size)}</b>"
    )
    await _edit_or_send(update, text, kb)


@admin_only
async def admin_procs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    running = pm.all_running()
    text    = (
        f"𓆩📺𓆪 <b>العمليات الحيّة ({len(running)})</b>\n"
        f"{SEP_MAIN}\n"
        f"{res_monitor.summary_text()}\n{SEP_THIN}\n"
    )
    rows: List[List[InlineKeyboardButton]] = []
    if not running:
        text += "✅ لا توجد عمليات قيد التشغيل."
    else:
        for fid in running:
            hf = db.get_file(fid)
            if not hf: continue
            lang = "🐘" if hf.file_type == "php" else "🐍"
            text += f"{lang} <code>{fid}</code> {shorten(hf.file_name, 18)} PID={pm.pid(fid)} {pm.uptime(fid)}\n"
            rows.append([
                btn_danger (f"⏹ {shorten(hf.file_name, 12)}", f"file:stop:{fid}"),
                btn_primary("📺", f"file:log:{fid}"),
                btn_warning("🔄", f"file:restart:{fid}"),
            ])
    rows.append([
        btn_success("🔴  إيقاف الكل", "admin:stop_all"),
        btn_primary("🔁  تحديث",      "admin:procs"),
    ])
    rows.append([btn_secondary("⬅️  رجوع", "admin:panel")])
    await _edit_or_send(update, text, InlineKeyboardMarkup(rows))


@admin_only
async def admin_stop_all(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    count = pm.stop_all()
    await _edit_or_send(
        update,
        f"𓆩⏹𓆪 تم إيقاف <b>{count}</b> عملية.",
        InlineKeyboardMarkup([[btn_secondary("⬅️  رجوع", "admin:panel")]]),
    )


@admin_only
async def admin_backup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    db.save(force=True)
    bk_path = os.path.join(BACKUP_DIR, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip")
    try:
        with zipfile.ZipFile(bk_path, "w", zipfile.ZIP_DEFLATED) as zf:
            if os.path.exists(DATABASE_FILE):
                zf.write(DATABASE_FILE, os.path.basename(DATABASE_FILE))
            for root, _, files in os.walk(FILES_DIR):
                for fn in files:
                    full = os.path.join(root, fn)
                    zf.write(full, os.path.relpath(full, "."))
        size = os.path.getsize(bk_path)
        with open(bk_path, "rb") as f:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=InputFile(f, filename=os.path.basename(bk_path)),
                caption=(
                    f"𓆩📥𓆪 <b>نسخة احتياطية</b>\n"
                    f"التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                    f"الحجم: {format_size(size)}"
                ),
                parse_mode=ParseMode.HTML,
            )
    except Exception as e:
        await _reply_anywhere(update, f"𓆩❌𓆪 فشل النسخ: {e}")


@admin_only
async def admin_restore_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["awaiting_restore"] = True
    await _edit_or_send(
        update,
        f"𓆩📤𓆪 <b>استعادة نسخة احتياطية</b>\nأرسل ملف backup_*.zip",
        InlineKeyboardMarkup([[btn_danger("❌  إلغاء", "admin:panel")]]),
    )


async def _do_restore(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.pop("awaiting_restore", None)
    doc = update.message.document
    if not doc or not (doc.file_name or "").startswith("backup_"):
        await update.message.reply_text(f"𓆩⚠️𓆪 يجب أن يكون الملف backup_*.zip")
        return
    tmp_path = os.path.join(TEMP_DIR, f"restore_{int(time.time())}.zip")
    try:
        tg_file = await context.bot.get_file(doc.file_id)
        await tg_file.download_to_drive(tmp_path)
        with zipfile.ZipFile(tmp_path, "r") as zf:
            zf.extractall(".")
        db.load()
        await update.message.reply_text(
            f"𓆩✅𓆪 تمت الاستعادة بنجاح!",
            reply_markup=InlineKeyboardMarkup([[btn_primary("👑  لوحة الإدارة", "admin:panel")]]),
        )
    except Exception as e:
        await update.message.reply_text(f"𓆩❌𓆪 فشلت الاستعادة: {e}")
    finally:
        try: os.remove(tmp_path)
        except: pass


@admin_only
async def admin_maint_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    db.settings["maintenance_mode"] = not db.settings.get("maintenance_mode", False)
    db.save(force=True)
    state = "مفعّل 🟡" if db.settings["maintenance_mode"] else "معطّل ✅"
    await _edit_or_send(
        update, f"𓆩🛠𓆪 وضع الصيانة: <b>{state}</b>",
        InlineKeyboardMarkup([[btn_secondary("⬅️  رجوع", "admin:panel")]]),
    )


@admin_only
async def admin_sysinfo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    py       = sys.version.split()[0]
    uptime_s = int(time.time() - _bot_start_time)
    h, r     = divmod(uptime_s, 3600); m, s = divmod(r, 60)
    php_ok   = detect_php()
    text = (
        f"𓆩🖥𓆪 <b>معلومات النظام</b>\n"
        f"{SEP_MAIN}\n"
        f"Python:            <code>{py}</code>\n"
        f"PHP:               <b>{'✅ متوفر' if php_ok else '❌ غير متوفر'}</b>\n"
        f"النظام:            <code>{platform.system()} {platform.release()}</code>\n"
        f"المعالج:           <code>{platform.machine()}</code>\n"
        f"مدة تشغيل البوت:   <b>{h}س {m}د {s}ث</b>\n"
        f"المسار:            <code>{escape_html(os.getcwd())}</code>\n"
        f"{SEP_THIN}\n"
        f"المستخدمون: <b>{len(db.users)}</b>\n"
        f"الملفات:    <b>{len(db.files)}</b>\n"
        f"العمليات:   <b>{len(pm.all_running())}</b>\n"
        f"قيد المراجعة: <b>{len(db.all_pending())}</b>\n"
        f"الإصدار:    <b>{BOT_VERSION}</b>\n"
        f"{SEP_THIN}\n"
        f"{res_monitor.summary_text()}"
    )
    await _edit_or_send(
        update, text,
        InlineKeyboardMarkup([
            [btn_primary("🔁  تحديث",         "admin:sysinfo")],
            [btn_secondary("⬅️  رجوع",        "admin:panel")],
        ]),
    )


@admin_only
async def admin_settings_view(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _edit_or_send(
        update,
        f"𓆩⚙️𓆪 <b>إعدادات البوت</b>\n{SEP_MAIN}\nاضغط أي زر لتعديله.",
        kb_settings_admin(),
    )


@admin_only
async def admin_settings_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                 key: str) -> None:
    if key in db.settings and isinstance(db.settings[key], bool):
        db.settings[key] = not db.settings[key]
        db.save(force=True)
    await admin_settings_view(update, context)


@admin_only
async def admin_settings_num_start(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                    key: str) -> None:
    context.user_data[ST_AWAIT_SET_NUM] = key
    await _edit_or_send(
        update, f"𓆩✏️𓆪 أرسل القيمة الرقمية الجديدة لـ <b>{escape_html(key)}</b>:",
        InlineKeyboardMarkup([[btn_danger("❌  إلغاء", "admin:settings")]]),
    )


@admin_only
async def admin_settings_text_start(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                     key: str) -> None:
    context.user_data[ST_AWAIT_SET_TEXT] = key
    await _edit_or_send(
        update, f"𓆩✏️𓆪 أرسل النص الجديد لـ <b>{escape_html(key)}</b>:",
        InlineKeyboardMarkup([[btn_danger("❌  إلغاء", "admin:settings")]]),
    )


@admin_only
async def admin_broadcast_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = f"𓆩📢𓆪 <b>إرسال بث جماعي</b>\n{SEP_MAIN}\nاختر الجمهور:"
    kb   = InlineKeyboardMarkup([
        [btn_success("👥  كل المستخدمين",    "broadcast:target:all"),
         btn_primary("🎯  للجميع",   "broadcast:target:all")],
        [btn_primary("🆕  الجدد (7 أيام)", "broadcast:target:new")],
        [btn_danger ("❌  إلغاء",            "admin:panel")],
    ])
    await _edit_or_send(update, text, kb)


async def admin_broadcast_do(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    target = context.user_data.pop(ST_AWAIT_BROADCAST, "all")
    msg    = update.message
    if target == "premium":   recipients = db.get_premium_users()
    elif target == "new":     recipients = db.get_new_users(7)
    else:                     recipients = db.all_users()
    sent = 0; failed = 0
    throttle = max(1, int(db.settings.get("broadcast_throttle_ms", 50))) / 1000.0
    progress = await msg.reply_text(f"𓆩📢𓆪 جاري البث لـ {len(recipients)} مستخدم…")
    for u in recipients:
        try: await msg.copy(chat_id=u.user_id); sent += 1
        except: failed += 1
        if (sent + failed) % 25 == 0:
            try:
                await progress.edit_text(
                    f"𓆩📢𓆪 {progress_bar(int((sent+failed)/len(recipients)*100))} "
                    f"✅{sent} / ❌{failed}")
            except: pass
        await asyncio.sleep(throttle)
    db.broadcast_history.append({"by": update.effective_user.id, "at": now_iso(),
                                  "sent": sent, "failed": failed, "target": target})
    db.stats["total_broadcasts"] = db.stats.get("total_broadcasts", 0) + 1
    db.save(force=True)
    await progress.edit_text(
        f"𓆩✅𓆪 <b>انتهى البث</b>\n✅ نجح: <b>{sent}</b> | ❌ فشل: <b>{failed}</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([[btn_primary("👑  لوحة الإدارة", "admin:panel")]]),
    )


@admin_only
async def admin_addpts_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data[ST_AWAIT_ADDPTS_ID] = True
    await _edit_or_send(update, f"𓆩➕𓆪 أرسل آيدي المستخدم:",
                        InlineKeyboardMarkup([[btn_danger("❌  إلغاء", "admin:panel")]]))


@admin_only
async def admin_subpts_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data[ST_AWAIT_SUBPTS_ID] = True
    await _edit_or_send(update, f"𓆩➖𓆪 أرسل آيدي المستخدم:",
                        InlineKeyboardMarkup([[btn_danger("❌  إلغاء", "admin:panel")]]))


@admin_only
async def admin_ban_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data[ST_AWAIT_BAN_ID] = True
    await _edit_or_send(update, f"𓆩🚫𓆪 أرسل آيدي المستخدم للحظر:",
                        InlineKeyboardMarkup([[btn_danger("❌  إلغاء", "admin:panel")]]))


@admin_only
async def admin_unban_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data[ST_AWAIT_UNBAN_ID] = True
    await _edit_or_send(update, f"𓆩🟢𓆪 أرسل آيدي المستخدم لفك الحظر:",
                        InlineKeyboardMarkup([[btn_danger("❌  إلغاء", "admin:panel")]]))


@admin_only
async def admin_search_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data[ST_AWAIT_SEARCH] = True
    await _edit_or_send(update, f"𓆩🔍𓆪 أرسل اسم/يوزر/آيدي للبحث:",
                        InlineKeyboardMarkup([[btn_danger("❌  إلغاء", "admin:panel")]]))


@admin_only
async def admin_security(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    events = db.security_events[-20:]
    text   = (
        f"𓆩🛡𓆪 <b>مركز الحماية</b>\n"
        f"{SEP_MAIN}\n"
        f"حماية الاستضافة:  <b>{'✅' if db.settings.get('strict_hosting_security') else '❌'}</b>\n"
        f"حماية API:        <b>{'✅' if db.settings.get('api_protection_enabled') else '❌'}</b>\n"
        f"حظر عند الخطر:   <b>{'✅' if db.settings.get('ban_on_confirmed_danger') else '❌'}</b>\n"
        f"نظام الموافقة:    <b>{'✅' if db.settings.get('require_admin_approval') else '❌'}</b>\n"
        f"أحداث أمنية:     <b>{len(db.security_events)}</b>\n"
    )
    if events:
        text += f"\n{SEP_THIN}\n<b>آخر الأحداث:</b>\n"
        for e in events[-10:]:
            banned_str = " [حُظر]" if e.get("banned") else ""
            text += f"• {format_dt(e.get('at',''))} ID={e.get('user_id')} {shorten(e.get('file',''),15)}{banned_str}\n"
    rows = [
        [btn_toggle("حماية الاستضافة", "adminset:toggle:strict_hosting_security",
                    bool(db.settings.get("strict_hosting_security"))),
         btn_toggle("حماية API",       "adminset:toggle:api_protection_enabled",
                    bool(db.settings.get("api_protection_enabled")))],
        [btn_toggle("حظر عند خطر",    "adminset:toggle:ban_on_confirmed_danger",
                    bool(db.settings.get("ban_on_confirmed_danger"))),
         btn_toggle("نظام الموافقة",   "adminset:toggle:require_admin_approval",
                    bool(db.settings.get("require_admin_approval")))],
        [btn_secondary("⬅️  رجوع", "admin:panel")],
    ]
    await _edit_or_send(update, text, InlineKeyboardMarkup(rows))


@admin_only
async def admin_ai_reports(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    files_with_ai = [(fid, hf) for fid, hf in db.files.items() if hf.ai_analysis]
    text = (
        f"𓆩🧠𓆪 <b>تقارير الذكاء الاصطناعي</b>\n"
        f"{SEP_MAIN}\n"
        f"ملفات تم تحليلها: <b>{len(files_with_ai)}</b> / {len(db.files)}\n\n"
    )
    for fid, hf in files_with_ai[-10:]:
        owner = db.users.get(hf.owner_id)
        ownr  = f"@{owner.username}" if owner and owner.username else str(hf.owner_id)
        lang  = "🐘" if hf.file_type == "php" else "🐍"
        text += f"• {lang} <code>{shorten(hf.file_name, 18)}</code> ({ownr}): {escape_html(hf.ai_analysis[:60])}\n"
    await _edit_or_send(
        update, text,
        InlineKeyboardMarkup([[btn_secondary("⬅️  لوحة الإدارة", "admin:panel")]]),
    )


@admin_only
async def admin_channels(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        f"𓆩📣𓆪 <b>إدارة قنوات الاشتراك الإجباري</b>\n"
        f"{SEP_MAIN}\n"
        f"الكلي: <b>{len(db.channels)}</b> | المفعّل: <b>{len(db.all_channels(True))}</b>"
    )
    await _edit_or_send(update, text, kb_channels_admin())


@admin_only
async def admin_channel_add_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data[ST_AWAIT_CHAN_ADD] = True
    text = (
        f"𓆩📣𓆪 أرسل القناة:\n"
        f"• <code>@channel_username</code>\n"
        f"• معرّف رقمي مثل <code>-1001234567890</code>"
    )
    await _edit_or_send(
        update, text,
        InlineKeyboardMarkup([[btn_danger("❌  إلغاء", "admin:channels")]]),
    )


async def admin_channel_add_save(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                  raw: str) -> None:
    raw = raw.strip()
    if not (raw.startswith("@") or raw.lstrip("-").isdigit()):
        await update.message.reply_text(f"𓆩❌𓆪 صيغة غير صحيحة.")
        return
    chat_id = raw; title = raw; invite = ""
    try:
        chat    = await context.bot.get_chat(chat_id)
        title   = chat.title or chat.username or raw
        try: invite = await context.bot.export_chat_invite_link(chat.id)
        except: invite = f"https://t.me/{chat.username}" if chat.username else ""
        chat_id = f"@{chat.username}" if chat.username else str(chat.id)
    except Exception as e:
        await update.message.reply_text(f"𓆩⚠️𓆪 لم أستطع جلب القناة: {e}")
    ch = Channel(chat_id=chat_id, title=title, invite_link=invite,
                 added_by=update.effective_user.id, added_at=now_iso(), enabled=True)
    db.add_channel(ch)
    context.user_data.pop(ST_AWAIT_CHAN_ADD, None)
    await update.message.reply_text(
        f"𓆩✅𓆪 أضيفت القناة: <b>{escape_html(title)}</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([[btn_primary("📣  القنوات", "admin:channels")]]),
    )


@admin_only
async def admin_channel_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                chat_id: str) -> None:
    ch = db.channels.get(chat_id)
    if ch: ch.enabled = not ch.enabled; db.save(force=True)
    await admin_channels(update, context)


@admin_only
async def admin_channel_delete(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                chat_id: str) -> None:
    db.remove_channel(chat_id)
    await admin_channels(update, context)


@admin_only
async def admin_broadcast_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    h    = db.broadcast_history[-20:]
    text = f"𓆩📋𓆪 <b>سجل البث</b>\n{SEP_MAIN}\n"
    if not h: text += "لا يوجد سجل."
    else:
        for b in reversed(h):
            tgt_l = {"all": "الكل", "premium": "البريميوم", "new": "الجدد"}.get(b.get("target",""), "—")
            text += f"• {format_dt(b.get('at',''))} — ✅{b.get('sent',0)}/❌{b.get('failed',0)} — [{tgt_l}]\n"
    await _edit_or_send(update, text,
                        InlineKeyboardMarkup([[btn_secondary("⬅️  رجوع", "admin:panel")]]))


@admin_only
async def admin_bwords(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = f"𓆩🛡𓆪 <b>الكلمات المحظورة</b>\n{SEP_MAIN}\n"
    text += ("\n".join(f"• <code>{escape_html(w)}</code>" for w in db.banned_words[:50])
             if db.banned_words else "لا توجد.")
    rows = [
        [btn_success("➕  إضافة",      "admin:bword_add"),
         btn_danger ("🗑  مسح الكل",   "admin:bword_clear")],
        [btn_secondary("⬅️  رجوع", "admin:panel")],
    ]
    await _edit_or_send(update, text, InlineKeyboardMarkup(rows))


@admin_only
async def admin_bword_add_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data[ST_AWAIT_BWORD] = True
    await _edit_or_send(update, f"𓆩🛡𓆪 أرسل الكلمة المراد حظرها:",
                        InlineKeyboardMarkup([[btn_danger("❌  إلغاء", "admin:bwords")]]))


@admin_only
async def admin_bword_clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    db.banned_words = []
    db.save(force=True)
    await admin_bwords(update, context)


@admin_only
async def admin_codes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = f"𓆩💻𓆪 <b>أكواد النقاط</b>\n{SEP_MAIN}\n"
    if not db.promo_codes: text += "لا توجد أكواد."
    else:
        for code, data in list(db.promo_codes.items())[:25]:
            used  = len(data.get("used_by", []))
            limit = data.get("limit", 1)
            bar   = progress_bar(int(used / max(limit, 1) * 100), 6)
            text += f"• <code>{escape_html(code)}</code> — <b>{data.get('points',0)}</b>pts [{bar} {used}/{limit}]\n"
    rows = [
        [btn_success("➕  إضافة كود",   "code:add"),
         btn_danger ("🗑  مسح الكل",    "code:clear")],
        [btn_secondary("⬅️  رجوع", "admin:panel")],
    ]
    await _edit_or_send(update, text, InlineKeyboardMarkup(rows))


@admin_only
async def admin_code_add_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data[ST_AWAIT_CODE_CREATE] = True
    await _edit_or_send(
        update,
        f"𓆩💻𓆪 أرسل الكود بهذا الشكل:\n<code>CODE 10 100</code>\nالاسم ← النقاط ← عدد الاستخدام",
        InlineKeyboardMarkup([[btn_danger("❌  إلغاء", "admin:codes")]]),
    )


async def admin_code_add_save(update: Update, context: ContextTypes.DEFAULT_TYPE,
                               raw: str) -> None:
    context.user_data.pop(ST_AWAIT_CODE_CREATE, None)
    parts = raw.strip().split()
    if len(parts) < 2:
        await update.message.reply_text(f"𓆩❌𓆪 الصيغة: CODE POINTS LIMIT")
        return
    code   = re.sub(r"[^A-Za-z0-9_-]", "", parts[0]).upper()[:32]
    points = int(parts[1])
    limit  = int(parts[2]) if len(parts) > 2 else 1
    db.promo_codes[code] = {
        "points": points, "limit": max(1, limit), "used_by": [],
        "active": True, "created_by": update.effective_user.id, "created_at": now_iso(),
    }
    db.save(force=True)
    await send_named_sticker(update, context, "admin_action")
    await update.message.reply_text(
        f"𓆩✅𓆪 تم إنشاء الكود\n<code>{escape_html(code)}</code> — <b>{points}</b>pts / <b>{limit}</b>x",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([[btn_primary("💻  الأكواد", "admin:codes")]]),
    )


@admin_only
async def admin_codes_clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    db.promo_codes = {}
    db.save(force=True)
    await admin_codes(update, context)


@admin_only
async def admin_activity_log(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log  = db.activity_log[-30:]
    text = f"𓆩🚨𓆪 <b>سجل النشاط (آخر 30)</b>\n{SEP_MAIN}\n"
    if not log: text += "لا يوجد نشاط."
    else:
        for entry in reversed(log):
            uid_s    = f"<code>{entry.get('user_id', '—')}</code>" if entry.get("user_id") else "—"
            detail_s = escape_html(shorten(entry.get("detail", ""), 30))
            text    += f"• {format_dt(entry.get('at',''))} [{escape_html(entry.get('action',''))}] {uid_s} {detail_s}\n"
    await _edit_or_send(update, text,
                        InlineKeyboardMarkup([[btn_secondary("⬅️  رجوع", "admin:panel")]]))


@admin_only
async def admin_premium(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    prem_users = db.get_premium_users()
    text = (
        f"𓆩💫𓆪 <b>إدارة البريميوم</b>\n{SEP_MAIN}\n"
        f"المستخدمون البريميوم: <b>{len(prem_users)}</b>\n\n"
        + ("\n".join(
            f"• <code>{u.user_id}</code> @{escape_html(u.username or '—')} حتى {format_dt(u.premium_until)}"
            for u in prem_users[:15])
           if prem_users else "لا يوجد مستخدمون بريميوم.")
    )
    rows = [
        
        [btn_secondary("⬅️  رجوع", "admin:panel")],
    ]
    await _edit_or_send(update, text, InlineKeyboardMarkup(rows))


@admin_only
async def admin_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = text_leaderboard("points")
    kb   = InlineKeyboardMarkup([
        [btn_primary("💎  النقاط",  "leaderboard:points"),
         btn_primary("📤  الرفع",   "leaderboard:uploads"),
         btn_primary("🎁  الدعوات", "leaderboard:invites")],
        [btn_secondary("⬅️  رجوع", "admin:panel")],
    ])
    await _edit_or_send(update, text, kb)


@admin_only
async def admin_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tasks = list(db.scheduled_tasks.values())
    text  = f"𓆩📅𓆪 <b>المهام المجدولة ({len(tasks)})</b>\n{SEP_MAIN}\n"
    if not tasks: text += "لا توجد مهام مجدولة."
    else:
        for t in tasks[:20]:
            hf    = db.get_file(t.file_id)
            fname = hf.file_name if hf else t.file_id
            text += (f"• <code>{t.task_id}</code> {shorten(fname, 18)} "
                     f"{'✅' if t.enabled else '❌'} وقت: {format_dt(t.run_at)}\n")
    await _edit_or_send(update, text,
                        InlineKeyboardMarkup([[btn_secondary("⬅️  رجوع", "admin:panel")]]))


# ══════════════════════════════════════════════════════════════════════════════
# 🎯  موجّه ضغطات الأزرار
# ══════════════════════════════════════════════════════════════════════════════

_bot_start_time = time.time()


@maintenance_gate
@check_banned
@rate_limit
async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    q = update.callback_query
    if not q: return
    try: await q.answer()
    except: pass
    data = q.data or ""
    uid  = q.from_user.id

    if data not in ("check_sub", "noop") and not is_admin(uid):
        if not await enforce_subscription(update, context): return

    # ── بوابة الوصول المدفوع ──
    if data.startswith("access:"):
        if await _handle_access_callback(update, context, data): return
    if not is_admin(uid) and not has_paid_access(uid) and \
       not data.startswith(("access:", "vip:", "menu:buy", "buy:",
                            "tos:", "check_sub", "noop")):
        await _send_access_gate(update, context); return

    # ── صيانة الأزرار ──
    if not is_admin(uid):
        disabled, lbl = is_button_disabled(data)
        if disabled:
            await _edit_or_send(update,
                f"🛠 <b>{lbl}</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"هذه الميزة <b>تحت الصيانة</b> حالياً.\n"
                f"يرجى المحاولة لاحقاً 🙏",
                InlineKeyboardMarkup([[btn_primary("⬅️ الرئيسية", "menu:main")]]))
            return
    if data.startswith(("admin:btnmaint", "btnmaint:")):
        if await _handle_btnmaint_callback(update, context, data): return
    if data == "admin:grant_access_start" and is_admin(uid):
        await _admin_access_grant_start(update, context); return
    if data == "admin:revoke_access_start" and is_admin(uid):
        await _admin_access_revoke_start(update, context); return
    if data.startswith("admin:grant_access:") and is_admin(uid):
        try: tid = int(data.split(":")[-1])
        except: tid = 0
        if tid and unlock_user_access(tid, "admin", uid):
            await _edit_or_send(update,
                f"✅ تم منح الوصول للمستخدم <code>{tid}</code>.",
                InlineKeyboardMarkup([[btn_primary("⬅️ رجوع", f"admin:user:{tid}")]]))
            try: await context.bot.send_message(tid,
                "🎉 تم تفعيل وصولك للبوت! أرسل /start للبدء.")
            except: pass
        return
    if data.startswith("admin:revoke_access:") and is_admin(uid):
        try: tid = int(data.split(":")[-1])
        except: tid = 0
        if tid and lock_user_access(tid):
            await _edit_or_send(update,
                f"🔒 تم سحب الوصول من <code>{tid}</code>.",
                InlineKeyboardMarkup([[btn_primary("⬅️ رجوع", f"admin:user:{tid}")]]))
        return

    try:
        if data == "noop": return

        if data == "check_sub":
            ok, missing = await check_subscription(uid, context.bot)
            if ok:
                me = await context.bot.get_me()
                u  = db.get_user(uid)
                await send_named_sticker(update, context, "subscription_ok")
                await _edit_or_send(update, text_welcome(u, me.username), kb_main_menu(uid))
            else:
                kb = subscription_keyboard(missing)
                await update.callback_query.edit_message_reply_markup(reply_markup=kb)
            return

        # ─── القائمة الرئيسية ───────────────────────────────────────────
        if data == "menu:main":
            me = await context.bot.get_me(); u = db.get_user(uid)
            await _edit_or_send(update, text_welcome(u, me.username), kb_main_menu(uid)); return
        if data == "menu:upload":
            await upload_start(update, context); return
        if data == "menu:myfiles":
            await show_my_files(update, context, 0); return
        if data == "menu:pending":
            await show_pending_user(update, context); return
        if data == "menu:points":
            await show_points(update, context); return
        if data == "menu:invite":
            await show_invite(update, context); return
        if data == "menu:buy":
            await show_buy_points(update, context); return
        if data == "menu:stats":
            await show_stats(update, context); return
        if data == "menu:settings":
            await show_settings(update, context); return
        if data == "menu:support":
            await show_support(update, context); return
        if data == "menu:about":
            await show_about(update, context); return
        if data == "menu:security":
            await show_security_info(update, context); return
        if data == "menu:leaderboard":
            await show_leaderboard(update, context); return
        if data == "menu:redeem":
            await redeem_code_start(update, context); return

        # ─── اختيار نوع الرفع ────────────────────────────────────────────
        if data.startswith("upload:type:"):
            file_type = data.split(":")[-1]
            await upload_type_chosen(update, context, file_type); return

        # ─── الملفات المعلقة ──────────────────────────────────────────────
        if data.startswith("pending:view:"):
            await pending_review_detail(update, context, data[13:]); return
        if data.startswith("pending:report:"):
            await pending_full_report(update, context, data[15:]); return
        if data.startswith("approve:"):
            await admin_approve_pending(update, context, data[8:]); return
        if data.startswith("reject:"):
            await admin_reject_pending_start(update, context, data[7:]); return

        # ─── صفحات الملفات ───────────────────────────────────────────────
        if data.startswith("myfiles:page:"):
            page = int(data.split(":")[-1])
            await show_my_files(update, context, page); return

        # ─── إجراءات الملفات ─────────────────────────────────────────────
        if data.startswith("file:open:"):
            await open_file(update, context, data[10:]); return
        if data.startswith("file:run:"):
            await file_run(update, context, data[9:]); return
        if data.startswith("file:stop:"):
            await file_stop(update, context, data[10:]); return
        if data.startswith("file:restart:"):
            await file_restart(update, context, data[13:]); return
        if data.startswith("file:log:"):
            await file_log(update, context, data[9:]); return
        if data.startswith("file:export_log:"):
            await file_export_log(update, context, data[16:]); return
        if data.startswith("file:install:"):
            await file_install(update, context, data[13:]); return
        if data.startswith("file:del:"):
            await file_delete_confirm(update, context, data[9:]); return
        if data.startswith("file:del_yes:"):
            await file_delete_do(update, context, data[13:]); return
        if data.startswith("file:zip:"):
            await file_zip(update, context, data[9:]); return
        if data.startswith("file:auto:"):
            await file_toggle_auto(update, context, data[10:]); return
        if data.startswith("file:public:"):
            await file_toggle_public(update, context, data[12:]); return
        if data.startswith("file:share:"):
            await file_share(update, context, data[11:]); return
        if data.startswith("file:desc:"):
            await file_desc_start(update, context, data[10:]); return
        if data.startswith("file:ai:"):
            await file_ai_analyze(update, context, data[8:]); return

        # ─── شراء ───────────────────────────────────────────────────────
        if data.startswith("buy:"):
            parts = data.split(":")
            await initiate_purchase(update, context, int(parts[1]), int(parts[2])); return

        # ─── Leaderboard ─────────────────────────────────────────────────
        if data.startswith("leaderboard:"):
            await show_leaderboard(update, context, data.split(":")[-1]); return

        # ─── إعدادات المستخدم ────────────────────────────────────────────
        if data == "userset:toggle:notif":
            u = db.get_user(uid)
            u.notifications_enabled = not u.notifications_enabled
            db.update_user(u)
            await show_settings(update, context); return
        if data == "userset:export":
            u = db.get_user(uid)
            data_export = json.dumps(asdict(u), ensure_ascii=False, indent=2)
            await context.bot.send_document(
                chat_id=uid,
                document=InputFile(io.BytesIO(data_export.encode("utf-8")),
                                    filename=f"user_{uid}_data.json"),
                caption=f"𓆩📥𓆪 بياناتك الكاملة",
            )
            return

        # ─── البث ────────────────────────────────────────────────────────
        if data.startswith("broadcast:target:"):
            target = data.split(":")[-1]
            context.user_data[ST_AWAIT_BROADCAST] = target
            await _edit_or_send(update,
                                 f"𓆩📢𓆪 أرسل رسالة البث الآن ({target}):",
                                 InlineKeyboardMarkup([[btn_danger("❌  إلغاء", "admin:panel")]]))
            return

        # ─── لوحة الإدارة ────────────────────────────────────────────────
        if data == "admin:panel":
            await admin_panel(update, context); return
        if data == "admin:stats":
            await admin_stats(update, context); return
        if data.startswith("admin:users"):
            page = int(data.split(":")[-1]) if "page" in data else 0
            await admin_users(update, context, page); return
        if data.startswith("admin:files"):
            page = int(data.split(":")[-1]) if "page" in data else 0
            await admin_files(update, context, page); return
        if data.startswith("admin:user_files_page:"):
            parts = data.split(":"); uid_t = int(parts[-2]); page = int(parts[-1])
            await admin_user_files_list(update, context, uid_t, page); return
        if data.startswith("admin:user_files:"):
            await admin_user_files_list(update, context, int(data.split(":")[-1]), 0); return
        if data.startswith("admin:user:"):
            await admin_user_details(update, context, int(data.split(":")[-1])); return
        if data.startswith("admin:pending"):
            page = int(data.split(":")[-1]) if "page" in data else 0
            await admin_pending_list(update, context, page); return
        if data == "admin:channels":
            await admin_channels(update, context); return
        if data == "admin:settings":
            await admin_settings_view(update, context); return
        if data == "admin:broadcast":
            await admin_broadcast_start(update, context); return
        if data == "admin:addpts":
            await admin_addpts_start(update, context); return
        if data == "admin:subpts":
            await admin_subpts_start(update, context); return
        if data.startswith("admin:addpts_user:"):
            uid_t = int(data.split(":")[-1])
            context.user_data["addpts_target"] = uid_t
            context.user_data[ST_AWAIT_ADDPTS_AMT] = True
            await _edit_or_send(update, f"𓆩➕𓆪 أرسل عدد النقاط للإضافة للمستخدم <code>{uid_t}</code>:",
                                InlineKeyboardMarkup([[btn_danger("❌  إلغاء", f"admin:user:{uid_t}")]]))
            return
        if data.startswith("admin:subpts_user:"):
            uid_t = int(data.split(":")[-1])
            context.user_data["subpts_target"] = uid_t
            context.user_data[ST_AWAIT_SUBPTS_AMT] = True
            await _edit_or_send(update, f"𓆩➖𓆪 أرسل عدد النقاط للخصم من <code>{uid_t}</code>:",
                                InlineKeyboardMarkup([[btn_danger("❌  إلغاء", f"admin:user:{uid_t}")]]))
            return
        if data == "admin:ban":
            await admin_ban_start(update, context); return
        if data == "admin:unban":
            await admin_unban_start(update, context); return
        if data.startswith("admin:ban_user:"):
            uid_t = int(data.split(":")[-1])
            if is_admin_immortal(uid_t):
                await _edit_or_send(update, f"𓆩👑𓆪 المشرف محمي ولا يمكن حظره!", kb_back(f"admin:user:{uid_t}"))
                return
            context.user_data[ST_AWAIT_BAN_REASON] = uid_t
            await _edit_or_send(update, f"𓆩🚫𓆪 أرسل سبب الحظر:",
                                InlineKeyboardMarkup([[btn_danger("❌  إلغاء", f"admin:user:{uid_t}")]]))
            return
        if data.startswith("admin:unban_user:"):
            uid_t = int(data.split(":")[-1])
            u     = db.get_user(uid_t)
            u.is_banned = False; u.ban_reason = ""; u.ban_until = ""
            db.update_user(u)
            db.log_activity("unban", uid, str(uid_t))
            await _edit_or_send(update, f"𓆩🟢𓆪 فُكّ حظر <code>{uid_t}</code>.", kb_back(f"admin:user:{uid_t}"))
            return
        if data == "admin:search":
            await admin_search_start(update, context); return
        if data == "admin:procs":
            await admin_procs(update, context); return
        if data == "admin:stop_all":
            await admin_stop_all(update, context); return
        if data == "admin:backup":
            await admin_backup(update, context); return
        if data == "admin:restore":
            await admin_restore_info(update, context); return
        if data == "admin:maint":
            await admin_maint_toggle(update, context); return
        if data == "admin:bwords":
            await admin_bwords(update, context); return
        if data == "admin:bword_add":
            await admin_bword_add_start(update, context); return
        if data == "admin:bword_clear":
            await admin_bword_clear(update, context); return
        if data == "admin:codes":
            await admin_codes(update, context); return
        if data == "admin:security":
            await admin_security(update, context); return
        if data == "admin:sysinfo":
            await admin_sysinfo(update, context); return
        if data == "admin:bhist":
            await admin_broadcast_history(update, context); return
        if data == "admin:activity":
            await admin_activity_log(update, context); return
        if data == "admin:premium":
            await admin_premium(update, context); return
        if data == "admin:leaderboard":
            await admin_leaderboard(update, context); return
        if data == "admin:schedule":
            await admin_schedule(update, context); return
        if data == "admin:ai_reports":
            await admin_ai_reports(update, context); return

        # ─── إعدادات المشرف ──────────────────────────────────────────────
        if data.startswith("adminset:toggle:"):
            await admin_settings_toggle(update, context, data[16:]); return
        if data.startswith("adminset:num:"):
            await admin_settings_num_start(update, context, data[13:]); return
        if data.startswith("adminset:text:"):
            await admin_settings_text_start(update, context, data[14:]); return

        # ─── القنوات ─────────────────────────────────────────────────────
        if data == "chan:add":
            await admin_channel_add_start(update, context); return
        if data.startswith("chan:toggle:"):
            await admin_channel_toggle(update, context, data[12:]); return
        if data.startswith("chan:del:"):
            await admin_channel_delete(update, context, data[9:]); return

        # ─── الأكواد ─────────────────────────────────────────────────────
        if data == "code:add":
            await admin_code_add_start(update, context); return
        if data == "code:clear":
            await admin_codes_clear(update, context); return

        # ─── البريميوم ───────────────────────────────────────────────────
        if data == "premium:grant":
            context.user_data[ST_AWAIT_PREMIUM_UID] = "grant"
            await _edit_or_send(update, f"𓆩💫𓆪 أرسل آيدي المستخدم:",
                                InlineKeyboardMarkup([[btn_danger("❌  إلغاء", "admin:premium")]]))
            return
        if data == "premium:revoke":
            context.user_data[ST_AWAIT_PREMIUM_UID] = "revoke"
            await _edit_or_send(update, f"𓆩❌𓆪 أرسل آيدي المستخدم:",
                                InlineKeyboardMarkup([[btn_danger("❌  إلغاء", "admin:premium")]]))
            return
        if data.startswith("admin:grant_premium:"):
            uid_t = int(data.split(":")[-1])
            context.user_data[ST_AWAIT_PREMIUM_UID]  = f"grant:{uid_t}"
            context.user_data[ST_AWAIT_PREMIUM_DAYS] = True
            await _edit_or_send(update, f"𓆩💫𓆪 كم يوم؟ (0 = أبداً):",
                                InlineKeyboardMarkup([[btn_danger("❌  إلغاء", f"admin:user:{uid_t}")]]))
            return
        if data.startswith("admin:revoke_premium:"):
            uid_t = int(data.split(":")[-1])
            u     = db.get_user(uid_t)
            u.is_premium = False; u.premium_until = ""
            db.update_user(u)
            await _edit_or_send(update, f"𓆩✅𓆪 سُحب البريميوم من <code>{uid_t}</code>.",
                                kb_back(f"admin:user:{uid_t}"))
            return
        if data.startswith("admin:note_user:"):
            uid_t = int(data.split(":")[-1])
            context.user_data[ST_AWAIT_NOTE] = uid_t
            await _edit_or_send(update, f"𓆩📝𓆪 أرسل الملاحظة:",
                                InlineKeyboardMarkup([[btn_danger("❌  إلغاء", f"admin:user:{uid_t}")]]))
            return

        # ─── ADDONS v9: ToS + VIP + Support ─────────────────────────
        if data.startswith("tos:"):
            await _handle_tos_callback(update, context, data); return
        if data.startswith("vip:"):
            await _handle_vip_callback(update, context, data); return
        if data.startswith("admin_vip:"):
            await _handle_admin_vip_callback(update, context, data); return
        if data.startswith("admin_sec:"):
            await _handle_admin_section(update, context, data); return
        if data.startswith("pban:"):
            await _handle_pending_ban(update, context, data); return
        # ────────────────────────────────────────────────────────────

        logger.debug("callback غير معالج: %s", data)

    except Exception as e:
        logger.exception("callback_router error for %s: %s", data, e)
        try: await _edit_or_send(update, f"𓆩❌𓆪 خطأ: {escape_html(str(e)[:200])}", kb_back())
        except: pass


# ══════════════════════════════════════════════════════════════════════════════
# 💬  موجّه الرسائل النصية
# ══════════════════════════════════════════════════════════════════════════════

@maintenance_gate
@check_banned
@rate_limit
async def text_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    text = update.message.text or ""
    ud   = context.user_data
    # ── ADDONS v9: حالات VIP النصية ──
    if ud.get('await_vip_key'):
        await _vip_redeem_key(update, context, text); return
    if ud.get('await_vip_genkey'):
        await _admin_vip_genkey_do(update, context, text); return
    if ud.get('await_vip_grant'):
        await _admin_vip_grant_do(update, context, text); return
    if ud.get('await_vip_revoke'):
        await _admin_vip_revoke_do(update, context, text); return
    if ud.get('await_vip_price'):
        await _admin_vip_price_do(update, context, text); return

    # ─── وصف الملف ───────────────────────────────────────────────────────
    if ud.get(ST_AWAIT_FILE_DESC):
        file_id = ud.pop(ST_AWAIT_FILE_DESC)
        hf = db.get_file(file_id)
        if hf:
            hf.description = text[:200]
            db.add_file(hf)
            await update.message.reply_text(
                f"𓆩✅𓆪 تم تحديث الوصف.",
                reply_markup=InlineKeyboardMarkup([[btn_primary("📄  الملف", f"file:open:{file_id}")]]),
            )
        return

    # ─── منح/سحب الوصول (مشرف) ───────────────────────────────────────────
    if ud.get(ST_AWAIT_ACCESS_GRANT_ID) and is_admin(user.id):
        await _admin_access_grant_do(update, context, text); return
    if ud.get(ST_AWAIT_ACCESS_REVOKE_ID) and is_admin(user.id):
        await _admin_access_revoke_do(update, context, text); return

    # ─── كود الاسترداد ───────────────────────────────────────────────────
    if ud.get(ST_AWAIT_CODE_REDEEM):
        await redeem_code_do(update, context, text); return

    # ─── سبب الرفض ───────────────────────────────────────────────────────
    if ud.get(ST_AWAIT_REJECT_REASON) and is_admin(user.id):
        pending_id = ud.pop(ST_AWAIT_REJECT_REASON)
        await admin_reject_do(update, context, pending_id, text.strip()); return

    # ─── إنشاء كود ───────────────────────────────────────────────────────
    if ud.get(ST_AWAIT_CODE_CREATE) and is_admin(user.id):
        await admin_code_add_save(update, context, text); return

    # ─── إضافة قناة ──────────────────────────────────────────────────────
    if ud.get(ST_AWAIT_CHAN_ADD) and is_admin(user.id):
        await admin_channel_add_save(update, context, text); return

    # ─── رسالة البث ──────────────────────────────────────────────────────
    if ud.get(ST_AWAIT_BROADCAST) and is_admin(user.id):
        await admin_broadcast_do(update, context); return

    # ─── كلمة محظورة ─────────────────────────────────────────────────────
    if ud.get(ST_AWAIT_BWORD) and is_admin(user.id):
        ud.pop(ST_AWAIT_BWORD)
        word = text.strip().lower()
        if word and word not in db.banned_words:
            db.banned_words.append(word)
            db.save(force=True)
        await update.message.reply_text(
            f"𓆩✅𓆪 تم إضافة الكلمة المحظورة.",
            reply_markup=InlineKeyboardMarkup([[btn_primary("🛡  الكلمات المحظورة", "admin:bwords")]]),
        )
        return

    # ─── إعداد رقمي ──────────────────────────────────────────────────────
    if ud.get(ST_AWAIT_SET_NUM) and is_admin(user.id):
        key = ud.pop(ST_AWAIT_SET_NUM)
        try:
            db.settings[key] = int(text.strip())
            db.save(force=True)
            await update.message.reply_text(f"𓆩✅𓆪 تم تحديث <b>{escape_html(key)}</b>.",
                                             parse_mode=ParseMode.HTML)
        except ValueError:
            await update.message.reply_text(f"𓆩❌𓆪 يجب إرسال رقم صحيح.")
        return

    # ─── إعداد نصي ───────────────────────────────────────────────────────
    if ud.get(ST_AWAIT_SET_TEXT) and is_admin(user.id):
        key = ud.pop(ST_AWAIT_SET_TEXT)
        db.settings[key] = text.strip()
        db.save(force=True)
        await update.message.reply_text(f"𓆩✅𓆪 تم تحديث <b>{escape_html(key)}</b>.",
                                         parse_mode=ParseMode.HTML)
        return

    # ─── إضافة نقاط (ID) ─────────────────────────────────────────────────
    if ud.get(ST_AWAIT_ADDPTS_ID) and is_admin(user.id):
        ud.pop(ST_AWAIT_ADDPTS_ID)
        try:
            target_id = int(text.strip())
            ud["addpts_target"] = target_id
            ud[ST_AWAIT_ADDPTS_AMT] = True
            await update.message.reply_text(
                f"𓆩➕𓆪 كم نقطة لـ <code>{target_id}</code>?",
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([[btn_danger("❌  إلغاء", "admin:panel")]]),
            )
        except ValueError:
            await update.message.reply_text(f"𓆩❌𓆪 معرّف غير صحيح.")
        return

    # ─── إضافة نقاط (الكمية) ─────────────────────────────────────────────
    if ud.get(ST_AWAIT_ADDPTS_AMT) and is_admin(user.id):
        ud.pop(ST_AWAIT_ADDPTS_AMT)
        target_id = ud.pop("addpts_target", None)
        try:
            pts = int(text.strip())
            if target_id:
                u_t = db.get_user(target_id)
                grant_points(u_t, pts, "admin", note=f"by={user.id}")
                db.update_user(u_t)
                await update.message.reply_text(
                    f"𓆩✅𓆪 أُضيف <b>{pts}</b> نقطة لـ <code>{target_id}</code>. رصيده: <b>{u_t.points}</b>",
                    parse_mode=ParseMode.HTML,
                    reply_markup=InlineKeyboardMarkup([[btn_primary("👑  الإدارة", "admin:panel")]]),
                )
        except ValueError:
            await update.message.reply_text(f"𓆩❌𓆪 أرسل رقماً.")
        return

    # ─── خصم نقاط (ID) ───────────────────────────────────────────────────
    if ud.get(ST_AWAIT_SUBPTS_ID) and is_admin(user.id):
        ud.pop(ST_AWAIT_SUBPTS_ID)
        try:
            target_id = int(text.strip())
            ud["subpts_target"] = target_id
            ud[ST_AWAIT_SUBPTS_AMT] = True
            await update.message.reply_text(
                f"𓆩➖𓆪 كم نقطة تُخصَم من <code>{target_id}</code>?",
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([[btn_danger("❌  إلغاء", "admin:panel")]]),
            )
        except ValueError:
            await update.message.reply_text(f"𓆩❌𓆪 معرّف غير صحيح.")
        return

    # ─── خصم نقاط (الكمية) ───────────────────────────────────────────────
    if ud.get(ST_AWAIT_SUBPTS_AMT) and is_admin(user.id):
        ud.pop(ST_AWAIT_SUBPTS_AMT)
        target_id = ud.pop("subpts_target", None)
        try:
            pts = int(text.strip())
            if target_id:
                u_t = db.get_user(target_id)
                u_t.points = max(0, u_t.points - pts)
                db.update_user(u_t)
                await update.message.reply_text(
                    f"𓆩✅𓆪 خُصم <b>{pts}</b> نقطة من <code>{target_id}</code>. رصيده: <b>{u_t.points}</b>",
                    parse_mode=ParseMode.HTML,
                )
        except ValueError:
            await update.message.reply_text(f"𓆩❌𓆪 أرسل رقماً.")
        return

    # ─── حظر مستخدم (ID) ─────────────────────────────────────────────────
    if ud.get(ST_AWAIT_BAN_ID) and is_admin(user.id):
        ud.pop(ST_AWAIT_BAN_ID)
        try:
            target_id = int(text.strip())
            if is_admin_immortal(target_id):
                await update.message.reply_text(f"𓆩👑𓆪 المشرف محمي.")
                return
            ud[ST_AWAIT_BAN_REASON] = target_id
            await update.message.reply_text(
                f"𓆩🚫𓆪 أرسل سبب حظر <code>{target_id}</code>:",
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([[btn_danger("❌  إلغاء", "admin:panel")]]),
            )
        except ValueError:
            await update.message.reply_text(f"𓆩❌𓆪 معرّف غير صحيح.")
        return

    # ─── حظر مستخدم (السبب) ──────────────────────────────────────────────
    if isinstance(ud.get(ST_AWAIT_BAN_REASON), int) and is_admin(user.id):
        target_id = ud.pop(ST_AWAIT_BAN_REASON)
        reason    = text.strip() or "مخالفة الشروط"
        u_t = db.get_user(target_id)
        u_t.is_banned = True; u_t.ban_reason = reason
        db.update_user(u_t)
        db.log_activity("ban", user.id, f"{target_id}: {reason}")
        try:
            await context.bot.send_message(
                target_id,
                f"𓆩🚫𓆪 تم حظر حسابك.\nالسبب: {escape_html(reason)}\n"
                f"للاعتراض: @{db.settings.get('support_username', SUPPORT_USERNAME)}",
                parse_mode=ParseMode.HTML,
            )
        except: pass
        await update.message.reply_text(
            f"𓆩✅𓆪 تم حظر <code>{target_id}</code>.",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([[btn_primary("👑  الإدارة", "admin:panel")]]),
        )
        return

    # ─── فك الحظر ────────────────────────────────────────────────────────
    if ud.get(ST_AWAIT_UNBAN_ID) and is_admin(user.id):
        ud.pop(ST_AWAIT_UNBAN_ID)
        try:
            target_id = int(text.strip())
            u_t = db.get_user(target_id)
            u_t.is_banned = False; u_t.ban_reason = ""; u_t.ban_until = ""
            db.update_user(u_t)
            db.log_activity("unban", user.id, str(target_id))
            await update.message.reply_text(
                f"𓆩🟢𓆪 فُكّ حظر <code>{target_id}</code> بنجاح.",
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup([[btn_primary("👑  الإدارة", "admin:panel")]]),
            )
        except ValueError:
            await update.message.reply_text(f"𓆩❌𓆪 معرّف غير صحيح.")
        return

    # ─── البحث ───────────────────────────────────────────────────────────
    if ud.get(ST_AWAIT_SEARCH) and is_admin(user.id):
        ud.pop(ST_AWAIT_SEARCH)
        query   = text.strip().lower()
        results = []
        for u_s in db.all_users():
            if (query in str(u_s.user_id) or
                query in (u_s.username or "").lower() or
                query in (u_s.first_name or "").lower()):
                results.append(u_s)
        if not results:
            await update.message.reply_text(f"𓆩🔍𓆪 لا توجد نتائج.")
            return
        items  = [(f"👤 [{u_s.user_id}] {shorten(u_s.first_name or str(u_s.user_id), 18)} · {u_s.points}pts",
                   f"admin:user:{u_s.user_id}") for u_s in results[:20]]
        kb     = kb_paginated(items, 0, 10, "noop_page", "admin:panel")
        await update.message.reply_text(
            f"𓆩🔍𓆪 نتائج البحث: <b>{len(results)}</b>",
            parse_mode=ParseMode.HTML, reply_markup=kb,
        )
        return

    # ─── البريميوم (ID) ───────────────────────────────────────────────────
    if ud.get(ST_AWAIT_PREMIUM_UID) and is_admin(user.id):
        action = ud.pop(ST_AWAIT_PREMIUM_UID, "")
        try:
            target_id = int(text.strip())
            if action == "revoke":
                u_t = db.get_user(target_id)
                u_t.is_premium = False; u_t.premium_until = ""
                db.update_user(u_t)
                await update.message.reply_text(f"𓆩✅𓆪 سُحب البريميوم من <code>{target_id}</code>.",
                                                 parse_mode=ParseMode.HTML)
            else:
                ud[ST_AWAIT_PREMIUM_UID]  = f"grant:{target_id}"
                ud[ST_AWAIT_PREMIUM_DAYS] = True
                await update.message.reply_text(
                    f"𓆩💫𓆪 كم يوم بريميوم لـ <code>{target_id}</code>؟ (0 = أبداً):",
                    parse_mode=ParseMode.HTML,
                    reply_markup=InlineKeyboardMarkup([[btn_danger("❌  إلغاء", "admin:panel")]]),
                )
        except ValueError:
            await update.message.reply_text(f"𓆩❌𓆪 معرّف غير صحيح.")
        return

    # ─── البريميوم (الأيام) ───────────────────────────────────────────────
    if ud.get(ST_AWAIT_PREMIUM_DAYS) and is_admin(user.id):
        ud.pop(ST_AWAIT_PREMIUM_DAYS)
        action    = ud.pop(ST_AWAIT_PREMIUM_UID, "")
        target_id = int(action.split(":")[-1]) if ":" in str(action) else 0
        try:
            days = int(text.strip())
            if target_id:
                u_t = db.get_user(target_id)
                u_t.is_premium        = True
                u_t.premium_granted_by= user.id
                if days > 0:
                    until = (datetime.now(timezone.utc) + timedelta(days=days)).isoformat()
                    u_t.premium_until = until
                else:
                    u_t.premium_until = ""
                db.update_user(u_t)
                await send_named_sticker(update, context, "premium_granted")
                await update.message.reply_text(
                    f"𓆩💫𓆪 مُنح البريميوم لـ <code>{target_id}</code>"
                    f"{'  (أبداً)' if days == 0 else f' لـ {days} يوم'}",
                    parse_mode=ParseMode.HTML,
                    reply_markup=InlineKeyboardMarkup([[btn_primary("👑  الإدارة", "admin:panel")]]),
                )
                try:
                    await context.bot.send_message(
                        target_id,
                        f"𓆩💫𓆪 تهانينا! حصلت على عضوية <b>البريميوم</b> 🎉",
                        parse_mode=ParseMode.HTML,
                    )
                except: pass
        except ValueError:
            await update.message.reply_text(f"𓆩❌𓆪 أرسل رقم.")
        return

    # ─── ملاحظة المستخدم ─────────────────────────────────────────────────
    if isinstance(ud.get(ST_AWAIT_NOTE), int) and is_admin(user.id):
        target_id = ud.pop(ST_AWAIT_NOTE)
        u_t = db.get_user(target_id)
        u_t.notes = text.strip()[:200]
        db.update_user(u_t)
        await update.message.reply_text(f"𓆩✅𓆪 تم حفظ الملاحظة.")
        return

    # ─── الكلمات المحظورة ────────────────────────────────────────────────
    if db.banned_words:
        text_lower = text.lower()
        for word in db.banned_words:
            if word in text_lower:
                await update.message.delete()
                return


@maintenance_gate
@check_banned
@rate_limit
async def document_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """موجّه الملفات المرسلة"""
    ud = context.user_data
    if ud.get("awaiting_restore") and is_admin(update.effective_user.id):
        await _do_restore(update, context)
        return
    if ud.get(ST_AWAIT_UPLOAD):
        await handle_document_upload(update, context)
        return


# ══════════════════════════════════════════════════════════════════════════════
# ⏰  المهام الدورية
# ══════════════════════════════════════════════════════════════════════════════

async def job_save_db(context: ContextTypes.DEFAULT_TYPE) -> None:
    db.save()


async def job_check_premium(context: ContextTypes.DEFAULT_TYPE) -> None:
    """التحقق من انتهاء صلاحية البريميوم"""
    now = now_iso()
    for u in db.all_users():
        if u.is_premium and u.premium_until and u.premium_until < now:
            u.is_premium = False; u.premium_until = ""
            db.update_user(u, save=False)
            if u.notifications_enabled:
                try:
                    await context.bot.send_message(
                        u.user_id,
                        f"𓆩💫𓆪 انتهت عضوية البريميوم الخاصة بك.\n"
                        f"اشتر نقاطاً للترقية مجدداً.",
                        parse_mode=ParseMode.HTML,
                    )
                except: pass
    db.save()


async def job_check_scheduled(context: ContextTypes.DEFAULT_TYPE) -> None:
    """تشغيل المهام المجدولة"""
    if not db.settings.get("schedule_enabled", True): return
    now = now_iso()
    for tid, task in list(db.scheduled_tasks.items()):
        if not task.enabled: continue
        if task.run_at <= now:
            hf = db.get_file(task.file_id)
            if hf and not pm.is_running(task.file_id):
                ok, info = pm._run_hosted_file(hf)
                if ok:
                    hf.run_count += 1; hf.last_run = now_iso()
                    db.add_file(hf)
            task.last_triggered = now
            if task.repeat == "once":
                task.enabled = False
            db.scheduled_tasks[tid] = task
    db.save()


async def job_cleanup_pending(context: ContextTypes.DEFAULT_TYPE) -> None:
    """تنظيف الملفات المعلقة القديمة (أكثر من 7 أيام)"""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
    to_remove = [
        pid for pid, pu in db.pending_uploads.items()
        if pu.status != "pending" and pu.submitted_at < cutoff
    ]
    for pid in to_remove:
        db.pending_uploads.pop(pid, None)
    if to_remove:
        db.save(force=True)
        logger.info("تم تنظيف %d ملف معلق قديم", len(to_remove))


# ══════════════════════════════════════════════════════════════════════════════
# 🚀  تهيئة وتشغيل البوت
# ══════════════════════════════════════════════════════════════════════════════

async def setup_commands(app: Application) -> None:
    commands = [
        BotCommand("start",  "القائمة الرئيسية"),
        BotCommand("help",   "المساعدة والإرشادات"),
        BotCommand("myfiles","ملفاتي المستضافة"),
        BotCommand("upload", "رفع ملف جديد"),
        BotCommand("pending","الملفات قيد المراجعة"),
        BotCommand("points", "رصيد نقاطي"),
        BotCommand("stats",  "إحصائياتي"),
        BotCommand("invite", "دعوة أصدقاء"),
        BotCommand("top",    "المتصدرون"),
        BotCommand("redeem", "استرداد كود نقاط"),
        BotCommand("support","الدعم الفني"),
        BotCommand("about",  "عن البوت"),
    ]
    try:
        await app.bot.set_my_commands(commands, scope=BotCommandScopeDefault())
    except Exception as e:
        logger.warning("فشل تعيين الأوامر: %s", e)


@maintenance_gate
@check_banned
@rate_limit
async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        f"𓆩❓𓆪 <b>دليل الاستخدام</b>\n"
        f"{SEP_DOUBLE}\n"
        f"𓆩📤𓆪 <b>رفع الملف:</b>\n"
        f"  اضغط «رفع ملف جديد» واختر Python أو PHP\n"
        f"  ثم أرسل الملف — سيُراجَع قبل الاستضافة\n\n"
        f"𓆩🐍𓆪 <b>Python:</b> .py أو .zip\n"
        f"𓆩🐘𓆪 <b>PHP:</b> .php أو .zip\n\n"
        f"𓆩💎𓆪 <b>النقاط:</b>\n"
        f"  • الرفع الأول مجاني\n"
        f"  • كل دعوة ناجحة = {db.settings.get('points_per_invite', 2)} نقاط\n"
        f"  • الرفع اللاحق = {db.settings.get('upload_cost', 1)} نقطة\n\n"
        f"𓆩🛡𓆪 <b>الحماية:</b>\n"
        f"  كل ملف يُفحص بالذكاء الاصطناعي\n"
        f"  ويُرسَل للمشرف للموافقة عليه"
    )
    await _reply_anywhere(update, text,
                           InlineKeyboardMarkup([[btn_primary("🏠  القائمة الرئيسية", "menu:main")]]))


@maintenance_gate
@check_banned
@rate_limit
async def cmd_myfiles(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await show_my_files(update, context, 0)


@maintenance_gate
@check_banned
@rate_limit
async def cmd_pending(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await show_pending_user(update, context)


@maintenance_gate
@check_banned
@rate_limit
async def cmd_upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await upload_start(update, context)


@maintenance_gate
@check_banned
@rate_limit
async def cmd_points(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await show_points(update, context)


@maintenance_gate
@check_banned
@rate_limit
async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await show_stats(update, context)


@maintenance_gate
@check_banned
@rate_limit
async def cmd_invite(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await show_invite(update, context)


@maintenance_gate
@check_banned
@rate_limit
async def cmd_top(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await show_leaderboard(update, context)


@maintenance_gate
@check_banned
@rate_limit
async def cmd_support(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await show_support(update, context)


@maintenance_gate
@check_banned
@rate_limit
async def cmd_about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await show_about(update, context)


@maintenance_gate
@check_banned
@rate_limit
async def cmd_redeem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await redeem_code_start(update, context)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    global _LAST_CONFLICT_LOG_TS
    # تضارب getUpdates: لا نطبع Traceback متكرر، نحاول قتل أي نسخة محلية تستخدم نفس التوكن ثم نترك polling يكمل
    if isinstance(context.error, Conflict):
        now_ts = time.time()
        killed = _kill_local_token_conflicts("Conflict/getUpdates")
        if now_ts - _LAST_CONFLICT_LOG_TS > 60:
            logger.warning(
                "⚠️ تم رصد تضارب getUpdates. أُوقفت %s عملية محلية متضاربة. "
                "إذا بقي الخطأ فهناك نسخة خارج هذا الجهاز تستخدم نفس التوكن ويجب إيقافها من مصدر تشغيلها.",
                killed,
            )
            _LAST_CONFLICT_LOG_TS = now_ts
        return
    # تجاهل أخطاء الشبكة المؤقتة (Timeout / NetworkError) — لا توقف البوت
    if isinstance(context.error, (TimedOut, NetworkError)):
        logger.warning("شبكة بطيئة/مؤقتة: %s — سيتم المتابعة تلقائياً", context.error)
        return
    logger.error("خطأ غير متوقع: %s", context.error, exc_info=context.error)
    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(
                f"𓆩❌𓆪 حدث خطأ غير متوقع. حاول مجدداً."
            )
        except: pass


def main() -> None:
    logger.info("=" * 60)
    logger.info(f"  {BOT_NAME} v{BOT_VERSION}")
    logger.info("  Starting...")
    logger.info("=" * 60)

    if BOT_TOKEN in ("ضع_توكن_البوت_هنا", ""):
        logger.critical("BOT_TOKEN غير محدد! ضعه في متغير البيئة BOT_TOKEN")
        sys.exit(1)

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .connect_timeout(30.0)
        .read_timeout(30.0)
        .write_timeout(30.0)
        .pool_timeout(30.0)
        .get_updates_connect_timeout(30.0)
        .get_updates_read_timeout(60.0)
        .get_updates_write_timeout(30.0)
        .get_updates_pool_timeout(30.0)
        .build()
    )

    # أوامر
    app.add_handler(CommandHandler("start",   cmd_start))
    app.add_handler(CommandHandler("help",    cmd_help))
    app.add_handler(CommandHandler("myfiles", cmd_myfiles))
    app.add_handler(CommandHandler("upload",  cmd_upload))
    app.add_handler(CommandHandler("pending", cmd_pending))
    app.add_handler(CommandHandler("points",  cmd_points))
    app.add_handler(CommandHandler("stats",   cmd_stats))
    app.add_handler(CommandHandler("invite",  cmd_invite))
    app.add_handler(CommandHandler("top",     cmd_top))
    app.add_handler(CommandHandler("support", cmd_support))
    app.add_handler(CommandHandler("about",   cmd_about))
    app.add_handler(CommandHandler("redeem",  cmd_redeem))

    # أزرار
    app.add_handler(CallbackQueryHandler(callback_router))

    # الرسائل
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_router))
    app.add_handler(MessageHandler(filters.Document.ALL, document_router))

    # الدفع
    app.add_handler(PreCheckoutQueryHandler(precheckout_handler))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_handler))

    # خطأ
    app.add_error_handler(error_handler)

    # المهام الدورية
    jq = app.job_queue
    if jq:
        jq.run_repeating(job_save_db,          interval=30,   first=10)
        jq.run_repeating(job_check_premium,    interval=3600, first=60)
        jq.run_repeating(job_check_scheduled,  interval=60,   first=30)
        jq.run_repeating(job_cleanup_pending,  interval=86400,first=3600)

    # إعداد الأوامر
    async def post_init(app2):
        await setup_commands(app2)
        logger.info("✅ البوت يعمل الآن!")
        logger.info("   المشرفون: %s", ADMIN_IDS)
        logger.info("   PHP مدعوم: %s", detect_php())
        logger.info("   نظام الموافقة: %s", db.settings.get("require_admin_approval", True))

    app.post_init = post_init
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)



# ════════════════════════════════════════════════════════════════════════════════
# ⫷⫸  ADDONS v9.0 — ToS · VIP · Support · Admin Sections  ⫷⫸
# ════════════════════════════════════════════════════════════════════════════════

# ─── النصوص الثابتة ────────────────────────────────────────────────────────────

TOS_TEXT = (
    "𓆩📜𓆪 <b>اتفاقية وشروط الاستخدام — PyHost Pro Ultra PLUS</b>\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "قبل استخدام البوت، يجب الموافقة على البنود التالية:\n\n"
    "<b>1.</b> أتعهد بعدم استضافة أي ملفات ضارة أو مخالفة:\n"
    "    • فيروسات، تروجان، RAT، Stealer، Miner.\n"
    "    • بوتات إغراق/هجوم/فلود/DDoS.\n"
    "    • أدوات سرقة حسابات/توكنات/كروت بنكية.\n"
    "    • محتوى إباحي، سب وقذف، تحريض أو إرهاب.\n"
    "    • انتهاك حقوق الملكية الفكرية لطرف ثالث.\n\n"
    "<b>2.</b> أتحمّل المسؤولية الكاملة عن أي ملف أرفعه.\n"
    "<b>3.</b> أوافق على أن يفحص المشرف الكود قبل النشر.\n"
    "<b>4.</b> الإدارة لها الحق في حذف/إيقاف/حظر دون إنذار.\n"
    "<b>5.</b> أي محاولة لاختراق البوت = حظر فوري دائم + إبلاغ.\n"
    "<b>6.</b> الخدمة 'كما هي' دون ضمانات؛ النسخ الاحتياطية مسؤوليتي.\n"
    "<b>7.</b> الميزات المدفوعة (VIP) غير قابلة للاسترداد.\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "👇 اضغط <b>أوافق</b> للمتابعة، أو <b>رفض</b> للخروج."
)

def kb_tos() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [btn_success("✅  أوافق على الشروط", "tos:accept")],
        [btn_danger ("❌  أرفض",              "tos:decline")],
        [btn_url_primary("📜  للاستفسار @og4_z", "https://t.me/og4_z")],
    ])

async def _send_tos_gate(update: Update, context: ContextTypes.DEFAULT_TYPE, u: "User") -> None:
    if update.callback_query:
        await _edit_or_send(update, TOS_TEXT, kb_tos())
    else:
        await update.message.reply_text(TOS_TEXT, reply_markup=kb_tos(), parse_mode=ParseMode.HTML)

async def _handle_tos_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, data: str) -> None:
    uid = update.effective_user.id
    u   = db.get_user(uid)
    if data == "tos:accept":
        u.agreed_to_terms = True
        db.update_user(u, save=True)
        me = await context.bot.get_me()
        await _edit_or_send(update,
            "𓆩✅𓆪 <b>تم قبول الشروط</b>\n━━━━━━━━━━━━━━━━━━━━\nأهلاً بك في البوت 🎉",
            kb_main_menu(uid))
        try:
            await asyncio.sleep(1)
            await context.bot.send_message(uid, text_welcome(u, me.username),
                reply_markup=kb_main_menu(uid), parse_mode=ParseMode.HTML)
        except Exception: pass
    elif data == "tos:decline":
        await _edit_or_send(update,
            "𓆩🚫𓆪 <b>تم رفض الشروط</b>\nلا يمكن استخدام البوت بدون قبولها.\n"
            "أعد الأمر /start في أي وقت للموافقة.",
            InlineKeyboardMarkup([[btn_url_primary("📞 تواصل @og4_z", "https://t.me/og4_z")]]))



# ═════════════════════════════════════════════════════════════════════════════
# 🔐  بوابة الوصول المدفوع (Paid Access Gate) + صيانة الأزرار
# ═════════════════════════════════════════════════════════════════════════════

PAID_BOT_ENABLED = True   # ← إذا False يصبح البوت مجاناً للجميع

LICENSE_GATE_TEXT = (
    "╔══════════════════════════════════════╗\n"
    "║  𓆩👑𓆪  <b>PyHost Pro Ultra — وصول مدفوع</b>  𓆩👑𓆪  ║\n"
    "╚══════════════════════════════════════╝\n"
    "✨ <b>أهلاً بك في أرقى بوت استضافة Python &amp; PHP</b> ✨\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "🔒  هذا البوت يعمل بنظام <b>الوصول المدفوع</b>.\n"
    "    لاستخدام الميزات تحتاج إلى <b>مفتاح تفعيل</b>\n"
    "    أو الاشتراك بأحد باقات <b>VIP</b> 💎\n\n"
    "📜  <b>اتفاقية الترخيص:</b>\n"
    "    • الاستخدام شخصي فقط، يحظر إعادة البيع.\n"
    "    • يمنع رفع ملفات ضارة أو مخالفة.\n"
    "    • للمشرف صلاحية إيقاف الوصول دون إنذار.\n"
    "    • بقبول الترخيص أنت توافق على كل ما سبق.\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "👇  اختر طريقة التفعيل:"
)

def kb_access_gate() -> InlineKeyboardMarkup:
    rows = [
        [btn_success("🔑  لدي مفتاح تفعيل",        "access:enter_key")],
        [btn_success("💎  شراء وصول VIP",          "vip:menu")],
        [btn_primary("⭐  شراء نقاط مباشرة",        "menu:buy")],
        [btn_primary("📞  تواصل مع الإدارة",       "vip:contact")],
        [btn_url_primary("🌐  دعم مباشر @og4_z",    "https://t.me/og4_z")],
    ]
    return InlineKeyboardMarkup(rows)

def has_paid_access(user_id: int) -> bool:
    """يحدد إن كان المستخدم يملك صلاحية دخول البوت."""
    if not PAID_BOT_ENABLED:
        return True
    if is_admin(user_id):
        return True
    u = db.users.get(user_id)
    if not u:
        return False
    if getattr(u, "access_unlocked", False):
        return True
    if getattr(u, "is_premium", False):
        return True
    try:
        if _is_vip(user_id):
            return True
    except Exception:
        pass
    return False

def unlock_user_access(user_id: int, source: str = "manual", by: int = 0) -> bool:
    u = db.users.get(user_id)
    if not u:
        return False
    u.access_unlocked   = True
    u.access_granted_by = by
    u.access_granted_at = now_iso()
    u.access_source     = source
    db.update_user(u, save=True)
    return True

def lock_user_access(user_id: int) -> bool:
    u = db.users.get(user_id)
    if not u:
        return False
    u.access_unlocked = False
    db.update_user(u, save=True)
    return True

async def _send_access_gate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query:
        await _edit_or_send(update, LICENSE_GATE_TEXT, kb_access_gate())
    else:
        await update.message.reply_text(LICENSE_GATE_TEXT,
            reply_markup=kb_access_gate(), parse_mode=ParseMode.HTML)

async def _handle_access_callback(update: Update,
                                  context: ContextTypes.DEFAULT_TYPE,
                                  data: str) -> bool:
    """يرجع True إذا تعامل مع الحدث."""
    if data == "access:gate":
        await _send_access_gate(update, context); return True
    if data == "access:enter_key":
        context.user_data[ST_AWAIT_CODE_REDEEM] = True
        await _edit_or_send(update,
            "🔑 <b>أرسل مفتاح التفعيل الآن:</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "أرسل المفتاح كرسالة نصية وسيتم التحقق منه فوراً.",
            InlineKeyboardMarkup([[btn_danger("❌  إلغاء", "access:gate")]]))
        return True
    return False


# ─────────────────────────────────────────────────────────────
# 🧰  نظام صيانة الأزرار (Button Maintenance Registry)
# ─────────────────────────────────────────────────────────────

BUTTON_MAINTENANCE: List[Tuple[str, str]] = [
    # (callback_prefix, label)
    ("menu:upload",       "📤 رفع ملف جديد"),
    ("menu:myfiles",      "📁 ملفاتي"),
    ("menu:pending",      "⏳ قيد المراجعة"),
    ("menu:points",       "💎 نقاطي"),
    ("menu:buy",          "⭐ شراء نقاط"),
    ("menu:invite",       "🎁 دعوة الأصدقاء"),
    ("menu:stats",        "📊 الإحصائيات"),
    ("menu:leaderboard",  "🏆 المتصدرون"),
    ("menu:redeem",       "💻 كود النقاط"),
    ("menu:support",      "💬 الدعم"),
    ("menu:settings",     "⚙️ الإعدادات"),
    ("menu:security",     "🛡 الحماية"),
    ("menu:about",        "ℹ️ عن البوت"),
    ("vip:menu",          "💎 متجر VIP"),
    ("file:run",          "▶️ تشغيل الملف"),
    ("file:stop",         "⏹ إيقاف الملف"),
    ("file:restart",      "🔄 إعادة التشغيل"),
    ("file:install",      "💡 تثبيت المكتبات"),
    ("file:ai",           "🧠 تحليل AI"),
    ("file:zip",          "📥 تحميل ZIP"),
    ("file:share",        "🔗 رابط المشاركة"),
    ("file:del",          "🗑 حذف الملف"),
]

def _maint_store() -> Dict[str, bool]:
    return db.settings.setdefault("disabled_buttons", {})

def is_button_disabled(callback_data: str) -> Tuple[bool, str]:
    """ترجع (متعطل؟, اسم الزر)."""
    store = _maint_store()
    for prefix, label in BUTTON_MAINTENANCE:
        if callback_data == prefix or callback_data.startswith(prefix + ":"):
            if store.get(prefix, False):
                return True, label
    return False, ""

def kb_button_maintenance() -> InlineKeyboardMarkup:
    store = _maint_store()
    rows: List[List[InlineKeyboardButton]] = []
    row: List[InlineKeyboardButton] = []
    for prefix, label in BUTTON_MAINTENANCE:
        active = not store.get(prefix, False)   # active = شغّال
        row.append(btn_toggle(label, f"btnmaint:toggle:{prefix}", active))
        if len(row) == 1:
            rows.append(row); row = []
    if row: rows.append(row)
    rows.append([
        btn_danger ("🛑  تعطيل الكل", "btnmaint:all_off"),
        btn_success("✅  تفعيل الكل", "btnmaint:all_on"),
    ])
    rows.append([btn_secondary("⬅️  لوحة الإدارة", "admin:panel")])
    return InlineKeyboardMarkup(rows)

async def _show_button_maint(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    store = _maint_store()
    disabled_n = sum(1 for p, _ in BUTTON_MAINTENANCE if store.get(p, False))
    text = (
        f"🧰 <b>صيانة الأزرار</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"الأزرار المعطّلة حالياً: <b>{disabled_n}</b> / {len(BUTTON_MAINTENANCE)}\n"
        f"اضغط على أي زر للتبديل بين <b>شغّال / تحت الصيانة</b>.\n"
        f"المشرف لا يتأثر بهذه الإعدادات."
    )
    await _edit_or_send(update, text, kb_button_maintenance())

async def _handle_btnmaint_callback(update: Update,
                                    context: ContextTypes.DEFAULT_TYPE,
                                    data: str) -> bool:
    if not is_admin(update.effective_user.id):
        return False
    if data == "admin:btnmaint":
        await _show_button_maint(update, context); return True
    if data.startswith("btnmaint:toggle:"):
        prefix = data[len("btnmaint:toggle:"):]
        store  = _maint_store()
        store[prefix] = not store.get(prefix, False)
        db.save(force=True)
        await _show_button_maint(update, context); return True
    if data == "btnmaint:all_off":
        store = _maint_store()
        for p, _ in BUTTON_MAINTENANCE: store[p] = True
        db.save(force=True)
        await _show_button_maint(update, context); return True
    if data == "btnmaint:all_on":
        store = _maint_store()
        for p, _ in BUTTON_MAINTENANCE: store[p] = False
        db.save(force=True)
        await _show_button_maint(update, context); return True
    return False


# ─────────────────────────────────────────────────────────────
# 🔓  منح/سحب وصول بالـID (للمشرف)
# ─────────────────────────────────────────────────────────────
ST_AWAIT_ACCESS_GRANT_ID = "awaiting_access_grant_id"
ST_AWAIT_ACCESS_REVOKE_ID = "awaiting_access_revoke_id"

async def _admin_access_grant_start(update, context):
    context.user_data[ST_AWAIT_ACCESS_GRANT_ID] = True
    await _edit_or_send(update,
        "🔓 <b>منح وصول للبوت</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "أرسل ID المستخدم لمنحه صلاحية دخول البوت.",
        InlineKeyboardMarkup([[btn_danger("❌ إلغاء", "admin:panel")]]))

async def _admin_access_revoke_start(update, context):
    context.user_data[ST_AWAIT_ACCESS_REVOKE_ID] = True
    await _edit_or_send(update,
        "🔒 <b>سحب وصول</b>\n"
        "━━━━━━━━━━━━━━━━━\n"
        "أرسل ID المستخدم لسحب صلاحية الدخول منه.",
        InlineKeyboardMarkup([[btn_danger("❌ إلغاء", "admin:panel")]]))

async def _admin_access_grant_do(update, context, raw: str):
    context.user_data.pop(ST_AWAIT_ACCESS_GRANT_ID, None)
    try: uid = int(raw.strip())
    except: 
        await update.message.reply_text("❌ ID غير صالح."); return
    u = db.users.get(uid)
    if not u:
        await update.message.reply_text("❌ المستخدم غير موجود في قاعدة البيانات."); return
    unlock_user_access(uid, source="admin", by=update.effective_user.id)
    await update.message.reply_text(
        f"✅ تم منح الوصول للمستخدم <code>{uid}</code>.\n"
        f"يمكنه الآن استخدام البوت بنظام النقاط العادي.",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([[btn_primary("⬅️ لوحة الإدارة", "admin:panel")]]))
    try:
        await context.bot.send_message(uid,
            "🎉 <b>تم تفعيل وصولك للبوت!</b>\n"
            "أرسل /start للبدء.", parse_mode=ParseMode.HTML)
    except: pass

async def _admin_access_revoke_do(update, context, raw: str):
    context.user_data.pop(ST_AWAIT_ACCESS_REVOKE_ID, None)
    try: uid = int(raw.strip())
    except: 
        await update.message.reply_text("❌ ID غير صالح."); return
    lock_user_access(uid)
    await update.message.reply_text(
        f"🔒 تم سحب الوصول من <code>{uid}</code>.",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([[btn_primary("⬅️ لوحة الإدارة", "admin:panel")]]))


# ═════════════════════════════════════════════════════════════════════════════
# 💎 نظام VIP المتكامل
# ═════════════════════════════════════════════════════════════════════════════

def _vip_store() -> Dict[str, Any]:
    """مخزن VIP داخل db.settings"""
    s = db.settings.setdefault("vip", {
        "enabled": True,
        "plans": {
            "7":   {"days": 7,   "stars": 50,  "label": "أسبوع"},
            "30":  {"days": 30,  "stars": 150, "label": "شهر"},
            "90":  {"days": 90,  "stars": 400, "label": "3 أشهر"},
            "365": {"days": 365, "stars": 1200,"label": "سنة كاملة"},
        },
        "keys": {},      # key_code -> {days, used_by, created_at, note}
        "members": {},   # str(user_id) -> {until_iso, source, granted_by}
    })
    return s

def _is_vip(user_id: int) -> bool:
    st = _vip_store()
    rec = st["members"].get(str(user_id))
    if not rec: return False
    try:
        until = datetime.fromisoformat(rec["until"])
        return until > datetime.now(timezone.utc).replace(tzinfo=None)
    except Exception:
        return False

def _vip_grant(user_id: int, days: int, source: str = "manual", granted_by: int = 0) -> str:
    st  = _vip_store()
    now = datetime.utcnow()
    cur = st["members"].get(str(user_id))
    if cur:
        try: base = max(datetime.fromisoformat(cur["until"]), now)
        except: base = now
    else:
        base = now
    until = base + timedelta(days=days)
    st["members"][str(user_id)] = {
        "until":      until.isoformat(timespec="seconds"),
        "source":     source,
        "granted_by": granted_by,
        "days_added": days,
    }
    # تزامن مع نظام Premium الموجود
    try:
        u = db.get_user(user_id)
        u.is_premium = True
        u.premium_until = until.isoformat(timespec="seconds")
        u.premium_granted_by = granted_by
        db.update_user(u, save=True)
    except Exception: pass
    db.save(force=True)
    return until.strftime("%Y-%m-%d %H:%M UTC")

def _vip_revoke(user_id: int) -> bool:
    st = _vip_store()
    if str(user_id) in st["members"]:
        st["members"].pop(str(user_id), None)
        try:
            u = db.get_user(user_id)
            u.is_premium = False
            u.premium_until = ""
            db.update_user(u, save=True)
        except Exception: pass
        db.save(force=True)
        return True
    return False

def _vip_gen_key(days: int, note: str = "", uses: int = 1) -> str:
    import secrets
    key = "VIP-" + "-".join(
        "".join(secrets.choice("ABCDEFGHJKMNPQRSTUVWXYZ23456789") for _ in range(4))
        for _ in range(3)
    )
    st = _vip_store()
    st["keys"][key] = {
        "days": int(days),
        "uses_left": int(uses),
        "used_by": [],
        "created_at": now_iso(),
        "note": note,
    }
    db.save(force=True)
    return key

def _vip_redeem(user_id: int, raw_key: str) -> Tuple[bool, str]:
    key = raw_key.strip().upper()
    st  = _vip_store()
    rec = st["keys"].get(key)
    if not rec: return False, "❌ مفتاح غير موجود."
    if rec["uses_left"] <= 0: return False, "⚠️ انتهت استخدامات هذا المفتاح."
    if user_id in rec.get("used_by", []): return False, "ℹ️ استخدمت هذا المفتاح من قبل."
    until = _vip_grant(user_id, rec["days"], source="key", granted_by=0)
    rec["uses_left"] -= 1
    rec.setdefault("used_by", []).append(user_id)
    db.save(force=True)
    return True, f"✅ تم تفعيل VIP لمدة <b>{rec['days']}</b> يوم.\nينتهي: <code>{until}</code>"


# ─── واجهات VIP ────────────────────────────────────────────────────────────

def kb_vip_menu(user_id: int) -> InlineKeyboardMarkup:
    st = _vip_store()
    plans = st["plans"]
    rows  = []
    # خطط الشراء بالنجوم
    for pid, p in sorted(plans.items(), key=lambda x: int(x[1]["days"])):
        rows.append([btn_success(
            f"⭐ {p['label']} — {p['stars']} نجمة ({p['days']} يوم)",
            f"vip:buy:{pid}")])
    rows.append([btn_primary("🔑  تفعيل بمفتاح", "vip:redeem"),
                 btn_primary("👤  حالتي VIP",     "vip:status")])
    rows.append([btn_url_primary("📞  تواصل @og4_z (شراء يدوي)", "https://t.me/og4_z")])
    if is_admin(user_id):
        rows.append([btn_danger("👑  إدارة VIP", "admin_vip:panel")])
    rows.append([btn_secondary("⬅️  الرئيسية", "menu:main")])
    return InlineKeyboardMarkup(rows)

async def _handle_vip_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, data: str) -> None:
    uid = update.effective_user.id
    parts = data.split(":")
    sub = parts[1] if len(parts) > 1 else ""

    if sub == "menu":
        is_v = _is_vip(uid)
        until = _vip_store()["members"].get(str(uid), {}).get("until", "—")
        txt = (
            "𓆩💎𓆪 <b>متجر VIP الذهبي</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "مميزات VIP:\n"
            "• ⚡ أولوية مراجعة الملفات\n"
            "• 📦 مساحة وحجم رفع أكبر\n"
            "• 🚀 تشغيل عدد عمليات أعلى\n"
            "• 🛡 لا حدود Rate Limit صارمة\n"
            "• 🎁 نقاط مضاعفة على الدعوة\n"
            "• 💬 دعم مباشر مع @og4_z\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"حالتك: <b>{'✅ VIP فعّال حتى ' + until if is_v else '⚪ عادي'}</b>"
        )
        await _edit_or_send(update, txt, kb_vip_menu(uid)); return

    if sub == "contact":
        txt = (
            "𓆩📞𓆪 <b>قسم الدعم المباشر</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "للشراء اليدوي، الاستفسارات، التفعيل،\n"
            "الإزالة، أو أي خدمة خاصة:\n\n"
            "👤  <b>@og4_z</b>\n"
            "🕐  الرد خلال 24 ساعة عادةً\n"
            "💳  ندعم الدفع اليدوي بأسعار مرنة"
        )
        kb = InlineKeyboardMarkup([
            [btn_url_success("💬  افتح المحادثة الآن", "https://t.me/og4_z")],
            [btn_secondary("⬅️  رجوع", "vip:menu")],
        ])
        await _edit_or_send(update, txt, kb); return

    if sub == "buy" and len(parts) >= 3:
        pid = parts[2]
        plan = _vip_store()["plans"].get(pid)
        if not plan:
            await _edit_or_send(update, "❌ خطة غير موجودة.", kb_back("vip:menu")); return
        try:
            await context.bot.send_invoice(
                chat_id=uid,
                title=f"VIP — {plan['label']}",
                description=f"اشتراك VIP لمدة {plan['days']} يوم",
                payload=f"vip_plan:{pid}:{plan['days']}",
                provider_token="",   # Telegram Stars
                currency="XTR",
                prices=[LabeledPrice(label=plan['label'], amount=int(plan['stars']))],
            )
        except Exception as e:
            await _edit_or_send(update, f"❌ تعذّر فتح الفاتورة: {escape_html(str(e)[:200])}",
                                kb_back("vip:menu"))
        return

    if sub == "redeem":
        context.user_data["await_vip_key"] = True
        await _edit_or_send(update,
            "🔑 أرسل مفتاح VIP الآن (يبدأ بـ <code>VIP-</code>):",
            InlineKeyboardMarkup([[btn_danger("❌ إلغاء", "vip:menu")]]))
        return

    if sub == "status":
        rec = _vip_store()["members"].get(str(uid))
        if not rec:
            txt = "⚪ أنت لست VIP حالياً.\nيمكنك الشراء أو إدخال مفتاح."
        else:
            txt = (
                "✅ <b>عضو VIP فعّال</b>\n"
                f"ينتهي: <code>{rec.get('until','—')}</code>\n"
                f"المصدر: <code>{rec.get('source','—')}</code>"
            )
        await _edit_or_send(update, txt, kb_back("vip:menu")); return

async def _vip_redeem_key(update: Update, context: ContextTypes.DEFAULT_TYPE, raw: str) -> None:
    context.user_data.pop("await_vip_key", None)
    ok, msg = _vip_redeem(update.effective_user.id, raw)
    await update.message.reply_text(msg, parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([[btn_primary("💎 متجر VIP", "vip:menu")]]))


# ─── معالج دفع VIP عبر النجوم (يلتقطه successful_payment_handler الأصلي عبر payload) ─
# نلصق Wrapper على successful_payment_handler الأصلي عبر تعديل دالة الدفع لاحقاً
# الحل: نسجّل MessageHandler إضافي لـ SUCCESSFUL_PAYMENT يتعامل مع payload vip_plan
async def vip_successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    sp = update.message.successful_payment if update.message else None
    if not sp: return
    payload = sp.invoice_payload or ""
    if not payload.startswith("vip_plan:"): return
    try:
        _, pid, days = payload.split(":")
        days = int(days)
    except Exception:
        return
    uid = update.effective_user.id
    until = _vip_grant(uid, days, source=f"stars:{pid}", granted_by=0)
    await update.message.reply_text(
        f"𓆩💎𓆪 <b>تم تفعيل VIP بنجاح!</b>\n"
        f"المدة: <b>{days}</b> يوم\n"
        f"ينتهي: <code>{until}</code>\n"
        f"شكراً لدعمك 💛",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([[btn_primary("💎 حالة VIP", "vip:status")]]))
    # إشعار الإدارة
    for adm in ADMIN_IDS:
        try:
            await context.bot.send_message(adm,
                f"💎 شراء VIP جديد\nUser: <code>{uid}</code>\nمدة: {days} يوم\nNJم: {sp.total_amount}",
                parse_mode=ParseMode.HTML)
        except: pass


# ═════════════════════════════════════════════════════════════════════════════
# 👑 إدارة VIP (للمشرف)
# ═════════════════════════════════════════════════════════════════════════════

def kb_admin_vip() -> InlineKeyboardMarkup:
    st = _vip_store()
    return InlineKeyboardMarkup([
        [btn_success("🎁 منح VIP لمستخدم", "admin_vip:grant"),
         btn_danger ("🚫 سحب VIP",          "admin_vip:revoke")],
        [btn_primary("🔑 توليد مفتاح VIP",  "admin_vip:genkey"),
         btn_primary("📋 قائمة الأعضاء",    "admin_vip:list")],
        [btn_primary("💰 تعديل الأسعار",    "admin_vip:prices"),
         btn_primary("🗝 قائمة المفاتيح",   "admin_vip:keys")],
        [btn_secondary("⬅️ لوحة الإدارة",  "admin:panel")],
    ])

async def _handle_admin_vip_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, data: str) -> None:
    if not is_admin(update.effective_user.id):
        await _edit_or_send(update, "❌ مخصص للإدارة.", kb_back()); return
    st = _vip_store()
    parts = data.split(":")
    sub = parts[1] if len(parts) > 1 else ""

    if sub == "panel":
        txt = (
            "👑 <b>إدارة VIP</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"👥 الأعضاء النشطون: <b>{len(st['members'])}</b>\n"
            f"🔑 المفاتيح: <b>{len(st['keys'])}</b>\n"
            f"💰 الخطط: <b>{len(st['plans'])}</b>"
        )
        await _edit_or_send(update, txt, kb_admin_vip()); return

    if sub == "grant":
        context.user_data["await_vip_grant"] = True
        await _edit_or_send(update,
            "🎁 أرسل: <code>user_id days</code>\nمثال: <code>123456789 30</code>",
            InlineKeyboardMarkup([[btn_danger("❌ إلغاء","admin_vip:panel")]])); return

    if sub == "revoke":
        context.user_data["await_vip_revoke"] = True
        await _edit_or_send(update, "🚫 أرسل user_id للسحب:",
            InlineKeyboardMarkup([[btn_danger("❌ إلغاء","admin_vip:panel")]])); return

    if sub == "genkey":
        context.user_data["await_vip_genkey"] = True
        await _edit_or_send(update,
            "🔑 أرسل: <code>days [uses] [note]</code>\nمثال: <code>30 1 هدية</code>",
            InlineKeyboardMarkup([[btn_danger("❌ إلغاء","admin_vip:panel")]])); return

    if sub == "list":
        members = st["members"]
        if not members:
            await _edit_or_send(update, "لا يوجد أعضاء VIP.", kb_back("admin_vip:panel")); return
        lines = ["👥 <b>أعضاء VIP</b>", "━━━━━━━━━━━━━━━━"]
        for uid_s, rec in list(members.items())[:50]:
            lines.append(f"• <code>{uid_s}</code> — حتى {rec.get('until','—')[:16]} ({rec.get('source','—')})")
        await _edit_or_send(update, "\n".join(lines), kb_back("admin_vip:panel")); return

    if sub == "keys":
        keys = st["keys"]
        if not keys:
            await _edit_or_send(update, "لا توجد مفاتيح.", kb_back("admin_vip:panel")); return
        lines = ["🗝 <b>مفاتيح VIP</b>", "━━━━━━━━━━━━━━━━"]
        for k, rec in list(keys.items())[:30]:
            lines.append(f"<code>{k}</code> — {rec['days']}ي · متبقّي {rec['uses_left']}")
        await _edit_or_send(update, "\n".join(lines), kb_back("admin_vip:panel")); return

    if sub == "prices":
        rows = []
        for pid, p in st["plans"].items():
            rows.append([btn_primary(f"{p['label']} — {p['stars']}⭐", f"admin_vip:price:{pid}")])
        rows.append([btn_secondary("⬅️ رجوع","admin_vip:panel")])
        await _edit_or_send(update, "💰 اختر خطة لتعديل سعرها بالنجوم:", InlineKeyboardMarkup(rows)); return

    if sub == "price" and len(parts) >= 3:
        pid = parts[2]
        context.user_data["await_vip_price"] = pid
        await _edit_or_send(update,
            f"💰 أرسل السعر الجديد بالنجوم لخطة <b>{pid}</b>:",
            InlineKeyboardMarkup([[btn_danger("❌ إلغاء","admin_vip:prices")]])); return

async def _admin_vip_grant_do(update: Update, context: ContextTypes.DEFAULT_TYPE, raw: str) -> None:
    context.user_data.pop("await_vip_grant", None)
    try:
        parts = raw.split()
        uid = int(parts[0]); days = int(parts[1])
        until = _vip_grant(uid, days, source="admin_manual", granted_by=update.effective_user.id)
        await update.message.reply_text(
            f"✅ تم منح VIP لـ <code>{uid}</code> مدة <b>{days}</b> يوم.\nحتى: <code>{until}</code>",
            parse_mode=ParseMode.HTML)
        try:
            await context.bot.send_message(uid,
                f"💎 <b>تم تفعيل VIP لحسابك!</b>\nالمدة: {days} يوم\nحتى: <code>{until}</code>\nبواسطة الإدارة 👑",
                parse_mode=ParseMode.HTML)
        except: pass
    except Exception as e:
        await update.message.reply_text(f"❌ صيغة خاطئة: {e}")

async def _admin_vip_revoke_do(update: Update, context: ContextTypes.DEFAULT_TYPE, raw: str) -> None:
    context.user_data.pop("await_vip_revoke", None)
    try:
        uid = int(raw.strip())
        ok = _vip_revoke(uid)
        await update.message.reply_text("✅ تم السحب." if ok else "ℹ️ المستخدم ليس VIP.")
        if ok:
            try:
                await context.bot.send_message(uid,
                    "⚠️ تم سحب اشتراك VIP من حسابك.\nأصبح حسابك عادياً (يعمل بالنقاط).")
            except: pass
    except Exception as e:
        await update.message.reply_text(f"❌ خطأ: {e}")

async def _admin_vip_genkey_do(update: Update, context: ContextTypes.DEFAULT_TYPE, raw: str) -> None:
    context.user_data.pop("await_vip_genkey", None)
    try:
        parts = raw.split(maxsplit=2)
        days  = int(parts[0])
        uses  = int(parts[1]) if len(parts) > 1 else 1
        note  = parts[2] if len(parts) > 2 else ""
        key = _vip_gen_key(days, note=note, uses=uses)
        await update.message.reply_text(
            f"🔑 <b>مفتاح VIP جديد</b>\n<code>{key}</code>\n"
            f"المدة: {days} يوم · الاستخدامات: {uses}\nملاحظة: {escape_html(note) or '—'}",
            parse_mode=ParseMode.HTML)
    except Exception as e:
        await update.message.reply_text(f"❌ صيغة: days [uses] [note]\n{e}")

async def _admin_vip_price_do(update: Update, context: ContextTypes.DEFAULT_TYPE, raw: str) -> None:
    pid = context.user_data.pop("await_vip_price", None)
    if not pid: return
    try:
        stars = int(raw.strip())
        _vip_store()["plans"][pid]["stars"] = stars
        db.save(force=True)
        await update.message.reply_text(f"✅ السعر الجديد لخطة {pid}: {stars}⭐")
    except Exception as e:
        await update.message.reply_text(f"❌ {e}")


# ═════════════════════════════════════════════════════════════════════════════
# 🗂 أقسام لوحة الإدارة المنظمة (admin_sec:*)
# ═════════════════════════════════════════════════════════════════════════════

async def _handle_admin_section(update: Update, context: ContextTypes.DEFAULT_TYPE, data: str) -> None:
    if not is_admin(update.effective_user.id):
        await _edit_or_send(update, "❌ مخصص للإدارة.", kb_back()); return
    sec = data.split(":", 1)[1] if ":" in data else ""

    if sec == "users":
        kb = InlineKeyboardMarkup([
            [btn_primary("👥 كل المستخدمين", "admin:users"),
             btn_success("🔍 بحث",            "admin:search")],
            [btn_primary("🚫 محظورون",        "admin:banned"),
             btn_primary("💎 أعضاء VIP",      "admin_vip:list")],
            [btn_secondary("⬅️ رجوع",         "admin:panel")],
        ])
        await _edit_or_send(update, "👥 <b>قسم المستخدمين</b>\n━━━━━━━━━━━━", kb); return

    if sec == "files":
        kb = InlineKeyboardMarkup([
            [btn_primary("📂 كل الملفات",      "admin:files"),
             btn_primary("⏳ قيد المراجعة",    "admin:pending")],
            [btn_primary("⚙️ العمليات الجارية","admin:procs"),
             btn_danger ("🛑 إيقاف الكل",      "admin:stopall")],
            [btn_secondary("⬅️ رجوع",         "admin:panel")],
        ])
        await _edit_or_send(update, "📂 <b>قسم الملفات</b>\n━━━━━━━━━━━━", kb); return

    if sec == "settings":
        kb = InlineKeyboardMarkup([
            [btn_primary("⚙️ إعدادات عامة",   "admin:settings"),
             btn_primary("📺 إدارة القنوات",   "admin:channels")],
            [btn_primary("💾 نسخة احتياطية",   "admin:backup"),
             btn_primary("♻️ استرجاع",         "admin:restore")],
            [btn_primary("🔧 وضع الصيانة",     "admin:maint")],
            [btn_secondary("⬅️ رجوع",         "admin:panel")],
        ])
        await _edit_or_send(update, "⚙️ <b>قسم الإعدادات</b>\n━━━━━━━━━━━━", kb); return

    if sec == "broadcast":
        kb = InlineKeyboardMarkup([
            [btn_primary("📢 بث للكل",         "broadcast:target:all")],
            [btn_primary("💎 بث للـ VIP",      "admin_vip:broadcast"),
             btn_primary("🆕 بث للجدد",        "broadcast:target:new")],
            [btn_secondary("⬅️ رجوع",         "admin:panel")],
        ])
        await _edit_or_send(update, "📢 <b>قسم البث</b>\n━━━━━━━━━━━━", kb); return

    if sec == "toggle_vip":
        cur = db.settings.get("vip_mode_enabled", True)
        db.settings["vip_mode_enabled"] = not cur
        db.save(force=True)
        await _edit_or_send(update,
            f"✅ تم {'تفعيل' if not cur else 'إيقاف'} وضع VIP.",
            kb_back("admin:panel")); return


# ═════════════════════════════════════════════════════════════════════════════
# 🚫 زر حظر المرسل من شاشة المراجعة (pban:user_id)
# ═════════════════════════════════════════════════════════════════════════════

def kb_pending_admin_plus(pending_id: str, owner_id: int) -> InlineKeyboardMarkup:
    """نسخة موسّعة من kb_pending_admin مع زر حظر المرسل"""
    return InlineKeyboardMarkup([
        [btn_success("✅  قبول",     f"approve:{pending_id}"),
         btn_danger ("❌  رفض",      f"reject:{pending_id}")],
        [btn_primary("🔎  التقرير الكامل", f"pending:report:{pending_id}")],
        [btn_danger ("🚫  حظر المرسل نهائياً", f"pban:{owner_id}:{pending_id}")],
        [btn_secondary("⬅️  لوحة الإدارة", "admin:panel")],
    ])

async def _handle_pending_ban(update: Update, context: ContextTypes.DEFAULT_TYPE, data: str) -> None:
    if not is_admin(update.effective_user.id):
        await _edit_or_send(update, "❌ مخصص للإدارة.", kb_back()); return
    try:
        _, owner_id, pending_id = data.split(":", 2)
        owner_id = int(owner_id)
    except Exception:
        return
    if owner_id in ADMIN_IDS:
        await _edit_or_send(update, "👑 لا يمكن حظر مشرف.", kb_back()); return
    u = db.get_user(owner_id)
    u.is_banned = True
    u.ban_reason = f"رفع ملف مشبوه (pending {pending_id})"
    db.update_user(u, save=True)
    # رفض الملف أيضاً
    pu = db.pending_uploads.get(pending_id)
    if pu:
        pu.status = "rejected"
        pu.reviewed_by = update.effective_user.id
        pu.reviewed_at = now_iso()
        pu.reject_reason = "حظر المرسل"
        db.save(force=True)
    await _edit_or_send(update,
        f"🚫 تم حظر <code>{owner_id}</code> ورفض ملفه.",
        kb_back("admin:panel"))
    try:
        await context.bot.send_message(owner_id,
            "🚫 تم حظر حسابك بسبب محاولة رفع محتوى مخالف للشروط.")
    except: pass


# ═════════════════════════════════════════════════════════════════════════════
# 🔌 تسجيل ADDONS داخل main()
# ═════════════════════════════════════════════════════════════════════════════

def _register_v9_addons(app) -> None:
    """يسجّل أوامر/معالجات v9 — يُستدعى من main()"""
    app.add_handler(CommandHandler("vip",       lambda u,c: _handle_vip_callback_cmd(u,c)))
    app.add_handler(CommandHandler("tos",       cmd_tos))
    app.add_handler(CommandHandler("og4z",      cmd_contact_og4z))
    # معالج خاص بدفعات VIP (يُسجّل قبل الأصلي ليلتقط vip_plan أولاً)
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, vip_successful_payment), group=-1)
    # ─── لوحة التحكم المتقدمة (فتح/إيقاف جماعي + VIP جماعي) ───
    app.add_handler(CommandHandler("control", cmd_control_panel))
    app.add_handler(CommandHandler("panel",   cmd_control_panel))
    app.add_handler(CallbackQueryHandler(_bulk_control_router, pattern=r"^vctl:"), group=-1)
    # فرض وضع Python فقط عند الإقلاع
    _enforce_python_only()

async def _handle_vip_callback_cmd(update, context):
    await _handle_vip_callback(update, context, "vip:menu")

async def cmd_tos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    u = db.get_user(update.effective_user.id)
    await _send_tos_gate(update, context, u)

async def cmd_contact_og4z(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await _handle_vip_callback(update, context, "vip:contact")


# ─── Monkey-patch لـ main() لتسجيل ADDONS تلقائياً ───
_orig_main_v9 = main
def main():
    """نسخة v9: تستدعي main الأصلية مع تسجيل addons قبل run_polling"""
    # نُعيد بناء التطبيق من الصفر بدلاً من تشغيل الأصلي مرتين
    logger.info("=" * 60)
    logger.info(f"  {BOT_NAME} v{BOT_VERSION}")
    logger.info("  Starting v9.0 PLUS...")
    logger.info("=" * 60)

    if BOT_TOKEN in ("ضع_توكن_البوت_هنا", ""):
        logger.critical("BOT_TOKEN غير محدد!")
        sys.exit(1)

    # ✅ إزالة الاشتراك الإجباري وكل القنوات نهائياً من جذورها
    try:
        db.settings["require_subscription"] = False
        db.channels.clear()
        db.save(force=True)
        logger.info("🧹 تم حذف كل القنوات وتعطيل الاشتراك الإجباري نهائياً.")
    except Exception as _e:
        logger.warning("تعذّر تنظيف القنوات: %s", _e)

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .connect_timeout(30.0)
        .read_timeout(30.0)
        .write_timeout(30.0)
        .pool_timeout(30.0)
        .get_updates_connect_timeout(30.0)
        .get_updates_read_timeout(60.0)
        .get_updates_write_timeout(30.0)
        .get_updates_pool_timeout(30.0)
        .build()
    )

    app.add_handler(CommandHandler("start",   cmd_start))
    app.add_handler(CommandHandler("help",    cmd_help))
    app.add_handler(CommandHandler("myfiles", cmd_myfiles))
    app.add_handler(CommandHandler("upload",  cmd_upload))
    app.add_handler(CommandHandler("pending", cmd_pending))
    app.add_handler(CommandHandler("points",  cmd_points))
    app.add_handler(CommandHandler("stats",   cmd_stats))
    app.add_handler(CommandHandler("invite",  cmd_invite))
    app.add_handler(CommandHandler("top",     cmd_top))
    app.add_handler(CommandHandler("support", cmd_support))
    app.add_handler(CommandHandler("about",   cmd_about))
    app.add_handler(CommandHandler("redeem",  cmd_redeem))
    app.add_handler(CommandHandler("admin",   admin_panel))

    # ADDONS v9
    _register_v9_addons(app)

    app.add_handler(CallbackQueryHandler(callback_router))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_router))
    app.add_handler(MessageHandler(filters.Document.ALL, document_router))
    app.add_handler(PreCheckoutQueryHandler(precheckout_handler))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_handler))
    app.add_error_handler(error_handler)

    jq = app.job_queue
    if jq:
        jq.run_repeating(job_save_db,         interval=30,    first=10)
        jq.run_repeating(job_check_premium,   interval=3600,  first=60)
        jq.run_repeating(job_check_scheduled, interval=60,    first=30)
        jq.run_repeating(job_cleanup_pending, interval=86400, first=3600)
        jq.run_repeating(_job_vip_expiry,     interval=3600,  first=120)

    async def post_init(app2):
        # 🛡 منع تضارب البوتات: حذف أي Webhook قديم وتجاهل التحديثات المعلقة لجعل هذا البوت هو الرئيسي
        try:
            await app2.bot.delete_webhook(drop_pending_updates=True)
            logger.info("🧹 تم حذف Webhook القديم وتجاهل التحديثات المعلقة (هذا البوت هو الرئيسي).")
        except Exception as _e:
            logger.warning("تعذّر حذف Webhook: %s", _e)
        await setup_commands(app2)
        logger.info("✅ البوت يعمل (v9.0 PLUS)!")
        logger.info("   المشرفون: %s", ADMIN_IDS)
        logger.info("   دعم VIP: @%s", VIP_SUPPORT_USERNAME)

    app.post_init = post_init

    # 🔒 قفل النسخة الواحدة: يضمن أن هذا البوت فقط هو الذي يعمل (منع تضارب البوتات)
    if not _acquire_singleton_lock():
        logger.critical("🚫 يوجد نسخة أخرى من البوت تعمل بالفعل على هذا الجهاز — تم الإيقاف لمنع التضارب.")
        sys.exit(1)

    # 🛡️ هذا هو الرئيسي: أوقف أي عملية محلية أخرى تحمل نفس التوكن وابدأ حارساً دورياً
    _kill_local_token_conflicts("إقلاع البوت الرئيسي")
    _start_primary_token_guard()

    # 🐍 Python 3.14 fix: ensure an event loop exists
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    # حلقة إعادة تشغيل تلقائية + معالجة التضارب لتفادي توقف البوت
    while True:
        try:
            app.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True,
                timeout=60,
                poll_interval=1.0,
            )
            break
        except Conflict as _conf_err:
            # نسخة أخرى تسحب التحديثات بنفس التوكن — نحاول إيقاف المحلي منها ثم نعيد المحاولة بدون Traceback مزعج
            killed = _kill_local_token_conflicts("run_polling Conflict")
            logger.warning("⚠️ تضارب getUpdates (%s). تم إيقاف %s عملية محلية. إعادة المحاولة بعد 8 ثوانٍ.", _conf_err, killed)
            import time as _t; _t.sleep(8)
            continue
        except (TimedOut, NetworkError) as _net_err:
            logger.warning("انقطاع شبكة في run_polling: %s — إعادة المحاولة بعد 5 ثوانٍ", _net_err)
            import time as _t; _t.sleep(5)
            continue
        except KeyboardInterrupt:
            logger.info("إيقاف يدوي."); break


async def _job_vip_expiry(context: ContextTypes.DEFAULT_TYPE) -> None:
    """يفحص انتهاء اشتراكات VIP ويُبلغ المستخدمين"""
    st = _vip_store()
    now = datetime.utcnow()
    expired = []
    for uid_s, rec in list(st["members"].items()):
        try:
            until = datetime.fromisoformat(rec["until"])
            if until <= now:
                expired.append(int(uid_s))
        except Exception:
            continue
    for uid in expired:
        _vip_revoke(uid)
        try:
            await context.bot.send_message(uid,
                "⌛ انتهى اشتراك VIP الخاص بك.\nيمكنك التجديد من /vip أو التواصل مع @og4_z")
        except: pass


# ═════════════════════════════════════════════════════════════════════════════
# 🔒 قفل النسخة الواحدة + 🐍 وضع Python فقط + 👑 لوحة التحكم الجماعية (v9.1 ULTRA+)
# ═════════════════════════════════════════════════════════════════════════════

_SINGLETON_SOCK = None  # يبقى محجوزاً طوال عمل البوت

def _acquire_singleton_lock() -> bool:
    """يحجز منفذاً محلياً لضمان عمل نسخة واحدة فقط من البوت (منع تضارب البوتات)."""
    global _SINGLETON_SOCK
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # لا نستخدم SO_REUSEADDR حتى يفشل الحجز إن كانت نسخة أخرى تعمل
        s.bind(("127.0.0.1", 47921))
        s.listen(1)
        _SINGLETON_SOCK = s
        logger.info("🔒 تم تأمين قفل النسخة الواحدة — هذا البوت هو الرئيسي.")
        return True
    except OSError:
        return False


def _enforce_python_only() -> None:
    """يجعل البوت يدعم Python فقط (إيقاف PHP) كما طلب المالك."""
    try:
        db.settings["php_support_enabled"] = False
        exts = db.settings.get("allowed_extensions", [".py", ".zip"])
        db.settings["allowed_extensions"] = [e for e in exts if e.lower() != ".php"] or [".py", ".zip"]
        db.save(force=True)
        logger.info("🐍 تم تفعيل وضع Python فقط (PHP معطّل).")
    except Exception as _e:
        logger.warning("تعذّر فرض وضع Python فقط: %s", _e)


# ─── لوحة التحكم المتقدمة ───
async def cmd_control_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_admin(update.effective_user.id):
        return
    await _show_control_panel(update, context)


async def _show_control_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        running = len(pm.all_running())
    except Exception:
        running = 0
    total_files = len(db.files)
    total_users = len(db.users)
    try:
        vip_count = len(_vip_store().get("members", {}))
    except Exception:
        vip_count = 0

    text = (
        "𓆩👑𓆪 <b>لوحة التحكم المتقدمة — ULTRA PLUS</b>\n"
        f"{SEP_MAIN}\n"
        f"🟢 العمليات الشغّالة: <b>{running}</b>\n"
        f"📂 إجمالي الملفات: <b>{total_files}</b>\n"
        f"👥 المستخدمون: <b>{total_users}</b>\n"
        f"💎 أعضاء VIP: <b>{vip_count}</b>\n"
        f"🐍 الوضع: <b>Python فقط</b>\n"
        f"{SEP_THIN}\n"
        "تحكم جماعي سريع بكل الاستضافات والأعضاء 👇"
    )
    kb = InlineKeyboardMarkup([
        [btn_success("▶️ فتح جماعي (تشغيل الكل)", "vctl:startall"),
         btn_danger ("⏹ إيقاف جماعي (إيقاف الكل)", "vctl:stopall")],
        [btn_primary("🔄 إعادة تشغيل الكل", "vctl:restartall")],
        [btn_success("💎 منح VIP للجميع (30 يوم)", "vctl:vipall"),
         btn_danger ("🚫 سحب VIP من الجميع", "vctl:vipnone")],
        [btn_primary("📊 إحصائيات حيّة", "vctl:stats"),
         btn_primary("🔁 تحديث", "vctl:refresh")],
        [btn_secondary("⬅️ لوحة الإدارة", "admin:panel")],
    ])
    await _edit_or_send(update, text, kb)


async def _bulk_control_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    q = update.callback_query
    if q:
        try: await q.answer()
        except: pass
    uid = update.effective_user.id
    if not is_admin(uid):
        await _edit_or_send(update, "❌ مخصص للإدارة فقط.", kb_back()); return
    data = (q.data if q else "") or ""
    action = data.split(":", 1)[1] if ":" in data else ""

    if action in ("refresh", "stats"):
        await _show_control_panel(update, context); return

    if action == "startall":
        started, failed, skipped = 0, 0, 0
        loop = asyncio.get_event_loop()
        for fid, hf in list(db.files.items()):
            try:
                if pm.is_running(fid):
                    skipped += 1; continue
                ok, _msg = await loop.run_in_executor(None, pm._run_hosted_file, hf)
                if ok: started += 1
                else: failed += 1
            except Exception:
                failed += 1
        await _edit_or_send(update,
            f"▶️ <b>فتح جماعي مكتمل</b>\n{SEP_THIN}\n"
            f"✅ تم التشغيل: <b>{started}</b>\n"
            f"⏭ تعمل مسبقاً: <b>{skipped}</b>\n"
            f"❌ فشلت: <b>{failed}</b>",
            kb_back("vctl:refresh")); return

    if action == "stopall":
        try: cnt = pm.stop_all()
        except Exception: cnt = 0
        await _edit_or_send(update,
            f"⏹ <b>إيقاف جماعي مكتمل</b>\n{SEP_THIN}\nتم إيقاف <b>{cnt}</b> عملية.",
            kb_back("vctl:refresh")); return

    if action == "restartall":
        try: pm.stop_all()
        except Exception: pass
        await asyncio.sleep(1)
        started = 0
        loop = asyncio.get_event_loop()
        for fid, hf in list(db.files.items()):
            try:
                ok, _msg = await loop.run_in_executor(None, pm._run_hosted_file, hf)
                if ok: started += 1
            except Exception:
                pass
        await _edit_or_send(update,
            f"🔄 <b>إعادة تشغيل جماعية مكتملة</b>\n{SEP_THIN}\nتم تشغيل <b>{started}</b> ملف.",
            kb_back("vctl:refresh")); return

    if action == "vipall":
        granted = 0
        for u in list(db.users.values()):
            try:
                _vip_grant(u.user_id, 30, source="bulk", granted_by=uid)
                granted += 1
            except Exception:
                pass
        try: db.settings["vip_mode_enabled"] = True; db.save(force=True)
        except Exception: pass
        await _edit_or_send(update,
            f"💎 <b>منح VIP جماعي</b>\n{SEP_THIN}\nتم منح VIP (30 يوم) لـ <b>{granted}</b> عضو.",
            kb_back("vctl:refresh")); return

    if action == "vipnone":
        revoked = 0
        try:
            members = list(_vip_store().get("members", {}).keys())
        except Exception:
            members = []
        for uid_s in members:
            try:
                if _vip_revoke(int(uid_s)): revoked += 1
            except Exception:
                pass
        await _edit_or_send(update,
            f"🚫 <b>سحب VIP جماعي</b>\n{SEP_THIN}\nتم سحب VIP من <b>{revoked}</b> عضو.",
            kb_back("vctl:refresh")); return

    await _show_control_panel(update, context)


if __name__ == "__main__":
    main()

async def cmd_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not is_admin(user.id):
        return
    
    vip_status = "✅ مفعل" if db.settings.get("vip_mode_enabled", False) else "❌ معطل"
    
    text = f"𓆩👑𓆪 <b>لوحة تحكم المشرف (V.I.P SECURITY SHIELD)</b>\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\nاختر القسم الذي تريد إدارته:"
    
    kb = InlineKeyboardMarkup([
        [btn_primary("👥 قسم المستخدمين", "admin_sec:users"), btn_primary("📂 قسم الملفات", "admin_sec:files")],
        [btn_primary("⚙️ إعدادات البوت", "admin_sec:settings"), btn_primary("📢 قسم الإذاعة (البث)", "admin_sec:broadcast")],
        [btn_primary("🎁 نظام الأكواد", "admin:codes")],
        [btn_danger(f"💎 وضع الـ VIP: {vip_status}", "admin_sec:toggle_vip")]
    ])
    
    if update.callback_query:
        await _edit_or_send(update, text, kb)
    else:
        await update.message.reply_text(text, reply_markup=kb, parse_mode=ParseMode.HTML)


async def admin_broadcast_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = f"𓆩📢𓆪 <b>إرسال بث جماعي</b>\n{SEP_MAIN}\nاختر الجمهور:"
    kb   = InlineKeyboardMarkup([
        [btn_success("👥  كل المستخدمين",    "broadcast:target:all"),
         btn_primary("🎯  للجميع",   "broadcast:target:all")],
        [btn_primary("🆕  الجدد (7 أيام)", "broadcast:target:new")],
        [btn_danger ("❌  إلغاء",            "admin:panel")],
    ])
    await _edit_or_send(update, text, kb)


