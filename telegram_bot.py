from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import requests
import pytz
from pytz import timezone
from telegram.ext import Application


TELEGRAM_TOKEN = '8096399192:AAG4WdkAn29KHUl4QFT0hwUAjiaRM5zHqBY'  # 🔁 Replace this with your bot token
BASE_URL = 'http://127.0.0.1:8000/api/'  # 🔁 Replace with your Django backend base API URL

# Stages of registration
FULL_NAME, CATEGORY, CITY, DISTRICT, STATE, EMAIL_OPTIONAL = range(6)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to SkillπEarn Bot!\nUse /register to register as a worker.\nUse /search to find workers.\nUse /myprofile to view your info.")
    
# ===== REGISTRATION FLOW =====
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['telegram_user_id'] = update.effective_user.id
    await update.message.reply_text("📛 Please enter your full name:")
    return FULL_NAME

async def get_full_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['full_name'] = update.message.text
    await update.message.reply_text("💼 Enter your work category (e.g., driver, plumber):")
    return CATEGORY

async def get_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['category'] = update.message.text
    await update.message.reply_text("🏙️ Enter your city:")
    return CITY

async def get_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['city'] = update.message.text
    await update.message.reply_text("🏞️ Enter your district:")
    return DISTRICT

async def get_district(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['district'] = update.message.text
    await update.message.reply_text("🗺️ Enter your state:")
    return STATE

async def get_state(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['state'] = update.message.text
    await update.message.reply_text("📧 (Optional) Enter your email or type skip:")
    return EMAIL_OPTIONAL

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text
    if email.lower() != 'skip':
        context.user_data['email'] = email
    else:
        context.user_data['email'] = None

    # Send data to Django API
    payload = {
        "telegram_user_id": context.user_data['telegram_user_id'],
        "full_name": context.user_data['full_name'],
        "category": context.user_data['category'],
        "city": context.user_data['city'],
        "district": context.user_data['district'],
        "state": context.user_data['state'],
        "email": context.user_data['email']
    }

    try:
        res = requests.post(BASE_URL + 'telegram-register/', json=payload)
        if res.status_code == 200:
            await update.message.reply_text("✅ Registered successfully!")
        else:
            await update.message.reply_text(f"⚠️ Error: {res.json().get('non_field_errors', res.text)}")
    except Exception as e:
        await update.message.reply_text("❌ Server error. Please try again later.")

    return ConversationHandler.END

# ===== MY PROFILE =====
async def my_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_user_id = update.effective_user.id
    try:
        res = requests.get(BASE_URL + f'my-profile/{telegram_user_id}/')
        if res.status_code == 200:
            data = res.json()
            msg = (
                f"👤 *{data['full_name']}*\n"
                f"📞 {data.get('phone_number')}\n"
                f"📍 {data['city']}, {data['district']}, {data['state']}\n"
                f"💼 {data['category']}\n"
                f"📝 {data.get('description', '')}"
            )
            await update.message.reply_text(msg, parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ Profile not found. Please register using /register")
    except Exception:
        await update.message.reply_text("⚠️ Could not fetch profile. Try again later.")

# ===== SEARCH COMMAND =====
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 3:
        await update.message.reply_text("Usage: /search <category> <city> <district>")
        return

    category, city, district = args
    try:
        res = requests.get(BASE_URL + 'search-profiles/', params={
            'category': category,
            'city': city,
            'district': district
        })
        data = res.json()
        if data:
            reply = ""
            for p in data:
                reply += (
                    f"👤 *{p['full_name']}*\n"
                    f"📞 {p['phone_number']}\n"
                    f"📍 {p['city']}, {p['district']}, {p['state']}\n"
                    f"💼 {p['category']}\n"
                    f"📝 {p['description']}\n\n"
                )
            await update.message.reply_text(reply, parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ No matching profiles found.")
    except Exception as e:
        await update.message.reply_text("⚠️ Search error. Try again.")

# ===== CANCEL =====
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Registration cancelled.")
    return ConversationHandler.END

# ====== MAIN ======
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

scheduler = AsyncIOScheduler(timezone=timezone('Asia/Kolkata'))

async def start_scheduler(app):
    scheduler.start()

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).post_init(start_scheduler).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('register', register)],
        states={
            FULL_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_full_name)],
            CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_category)],
            CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_city)],
            DISTRICT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_district)],
            STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_state)],
            EMAIL_OPTIONAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    app.add_handler(CommandHandler('start', start))
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler('myprofile', my_profile))
    app.add_handler(CommandHandler('search', search))

    print("🤖 Bot started...")
    app.run_polling()


if __name__ == '__main__':
    main()
