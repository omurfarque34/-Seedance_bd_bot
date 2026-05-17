from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    ConversationHandler,
)

BOT_TOKEN = "YOUR_BOT_TOKEN"
ADMIN_ID = 6706601403

SERVICE, ACCOUNT, GMAIL, SCREENSHOT = range(4)

services = [
    ["SEEDANCE 2.0"],
]

accounts = [
    ["Shared Account 500 Tk"],
    ["Personal Account 1000 Tk"]
]


def start(update: Update, context: CallbackContext):
    reply = ReplyKeyboardMarkup(services, resize_keyboard=True)

    update.message.reply_text(
        "🔥 সার্ভিস নির্বাচন করুন:",
        reply_markup=reply
    )

    return SERVICE


def service(update: Update, context: CallbackContext):
    context.user_data["service"] = update.message.text

    reply = ReplyKeyboardMarkup(accounts, resize_keyboard=True)

    update.message.reply_text(
        "🔐 Account Type নির্বাচন করুন:",
        reply_markup=reply
    )

    return ACCOUNT


def account(update: Update, context: CallbackContext):
    context.user_data["account"] = update.message.text

    update.message.reply_text(
        "📧 আপনার Gmail দিন:"
    )

    return GMAIL


def gmail(update: Update, context: CallbackContext):
    context.user_data["gmail"] = update.message.text

    update.message.reply_text(
        "💳 Payment করুন:\n\n"
        "Bkash: 01868635778 এজেন্ট শুধু মাত্র ক্যাশ আউট করবেন\n"
        "Nagad: 01343496446 এজেন্ট শুধু মাত্র ক্যাশ আউট করবেন\n\n"
        "টাকা পাঠিয়ে Screenshot দিন।"
    )

    return SCREENSHOT


def screenshot(update: Update, context: CallbackContext):
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

    context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo,
        caption=caption
    )

    update.message.reply_text(
        "✅ Screenshot Received\n\n"
        "⏳ ১০-১৫ মিনিটের মধ্যে অ্যাকাউন্ট পেয়ে যাবেন।"
    )

    return ConversationHandler.END


updater = Updater(BOT_TOKEN, use_context=True)
dp = updater.dispatcher

conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        SERVICE: [MessageHandler(Filters.text & ~Filters.command, service)],
        ACCOUNT: [MessageHandler(Filters.text & ~Filters.command, account)],
        GMAIL: [MessageHandler(Filters.text & ~Filters.command, gmail)],
        SCREENSHOT: [MessageHandler(Filters.photo, screenshot)],
    },
    fallbacks=[]
)

dp.add_handler(conv)

print("Bot Running...")
updater.start_polling()
updater.idle()
