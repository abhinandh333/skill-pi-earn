from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import requests
import pytz
from pytz import timezone
from telegram.ext import Application


TELEGRAM_TOKEN = '8096399192:AAG4WdkAn29KHUl4QFT0hwUAjiaRM5zHqBY'  # 🔁 Replace this with your bot token
BASE_URL = 'http://127.0.0.1:8000/api/'  # 🔁 Replace with your Django backend base API URL

# Stages of registration
FULL_NAME, CATEGORY, CITY, DISTRICT, STATE, PHONE_NUMBER, EMAIL_OPTIONAL = range(7)


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
    await update.message.reply_text("📞 Enter your phone number:")
    return PHONE_NUMBER

async def get_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone_number'] = update.message.text
    await update.message.reply_text("📧Enter your email or set as phonenumber@gmail.com for future:")
    return EMAIL_OPTIONAL


async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = update.message.text
    if email.lower() != 'skip':
        context.user_data['email'] = email
    else:
        context.user_data['email'] = f"{context.user_data['telegram_user_id']}@noemail.skillpi"

    # Prepare payload
    payload = {
        "telegram_user_id": context.user_data['telegram_user_id'],
        "full_name": context.user_data['full_name'],
        "category": context.user_data['category'],
        "city": context.user_data['city'],
        "district": context.user_data['district'],
        "state": context.user_data['state'],
        "email": context.user_data['email'],
        "phone_number": context.user_data['phone_number'],
    }

    try:
        res = requests.post(BASE_URL + 'telegram-register/', json=payload)
        if res.status_code == 200:
            dashboard_link = f"http://127.0.0.1:8000/dashboard/"
            await update.message.reply_text(
              "✅ Registered successfully!\n\n"
             f"🔗 [Go to your dashboard]({dashboard_link})",
             parse_mode='Markdown'
    )

        elif res.status_code == 400:
            errors = res.json()
            # Check for "already registered" case
            if "User already registered with this Telegram ID." in str(errors):
                await update.message.reply_text("⚠️ You're already registered. Showing your profile...")
                return await my_profile(update, context)  # 🔁 Call my_profile instead
            else:
                # General validation errors
                if isinstance(errors, dict):
                    error_messages = "\n".join([f"{field}: {', '.join(msgs)}" for field, msgs in errors.items()])
                elif isinstance(errors, list):
                    error_messages = "\n".join(errors)
                else:
                    error_messages = str(errors)

                await update.message.reply_text(f"❌ Invalid Data Received:\n{error_messages}")
        else:
            await update.message.reply_text(f"⚠️ Unexpected error: {res.status_code}\n{res.text}")
    except Exception as e:
        await update.message.reply_text(f"❌ Server error: {str(e)}")

    return ConversationHandler.END


# ===== MY PROFILE =====
async def my_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_user_id = update.effective_user.id
    try:
        res = requests.get(BASE_URL + f'my-profile/{telegram_user_id}/')
        if res.status_code == 200:
            data = res.json()
            phone = data.get('phone_number', 'N/A')
            if phone != 'N/A' and len(phone) >= 4:
                masked_phone = 'X' * (len(phone) - 4) + phone[-4:]
            else:
                masked_phone = phone

            msg = (
                f"👤 *{data['full_name']}*\n"
                f"📞 {masked_phone}\n"
                f"📍 {data['city']}, {data['district']}, {data['state']}\n"
                f"💼 {data['category']}\n"
                f"📝 {data.get('description', '')}"
            )
            MAX_LENGTH = 4000  # Telegram safe limit under 4096
            for i in range(0, len(msg), MAX_LENGTH):
                await update.message.reply_text(msg[i:i+MAX_LENGTH], parse_mode='Markdown')
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
                phone = p.get('phone_number', 'N/A')
                if phone != 'N/A' and len(phone) >= 4:
                    masked_phone = 'X' * (len(phone) - 4) + phone[-4:]
            else:
                masked_phone = phone

                reply += (
                    f"👤 *{p['full_name']}*\n"
                    f"📞 {masked_phone}\n"
                    f"📍 {p['city']}, {p['district']}, {p['state']}\n"
                    f"💼 {p['category']}\n"
                    f"📝 {p.get('description', '')}\n\n"
                )
            MAX_LENGTH = 4000
            for i in range(0, len(reply), MAX_LENGTH):
                await update.message.reply_text(reply[i:i + MAX_LENGTH], parse_mode='Markdown')
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
            PHONE_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone_number)],
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
