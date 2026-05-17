from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

BOT_TOKEN = "8812978702:AAEl9Hnug3vUiIIQTdxVDUcaDaEky04zzUM"
ADMIN_ID = 6706601403

SERVICE, ACCOUNT, GMAIL, SCREENSHOT = range(4)

services = [
    ["SEEDANCE 2.0"],
    
]

accounts = [
    ["Shared Account 500 Tk"],
    ["Personal Account 1000 Tk"]
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply = ReplyKeyboardMarkup(services, resize_keyboard=True)

    await update.message.reply_text(
        "🔥 সার্ভিস নির্বাচন করুন:",
        reply_markup=reply
    )

    return SERVICE

async def service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["service"] = update.message.text

    reply = ReplyKeyboardMarkup(accounts, resize_keyboard=True)

    await update.message.reply_text(
        "🔐 Account Type নির্বাচন করুন:",
        reply_markup=reply
    )

    return ACCOUNT

async def account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["account"] = update.message.text

    await update.message.reply_text(
        "📧 আপনার Gmail দিন:"
    )

    return GMAIL

async def gmail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["gmail"] = update.message.text

    await update.message.reply_text(
        "💳 Payment করুন:\n\n"
        "Bkash: 01868635778 এজেন্ট শুধু মাত্র ক্যাশ আউট করবেন\n"
        "Nagad: 01343496446 এজেন্ট শুধু মাত্র ক্যাশ আউট করবেন\n\n"
        "টাকা পাঠিয়ে Screenshot দিন।"
    )

    return SCREENSHOT

async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1].file_id

    service = context.user_data["service"]
    account = context.user_data["account"]
    gmail = context.user_data["gmail"]

    caption = (
        f"🛒 New Order\n\n"
        f"Service: {service}\n"
        f"Account: {account}\n"
        f"Gmail: {gmail}\n\n"
        f"User: @{update.message.from_user.username}\n"
        f"User ID: {update.message.from_user.id}"
    )

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo,
        caption=caption
    )

    await update.message.reply_text(
        "✅ Screenshot Received\n\n"
        "⏳ ১০-১৫ মিনিটের মধ্যে অ্যাকাউন্ট পেয়ে যাবেন।"
    )

    return ConversationHandler.END

app = ApplicationBuilder().token(BOT_TOKEN).build()

conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        SERVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, service)],
        ACCOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, account)],
        GMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, gmail)],
        SCREENSHOT: [MessageHandler(filters.PHOTO, screenshot)],
    },
    fallbacks=[]
)

app.add_handler(conv)

print("Bot Running...")
app.run_polling()
