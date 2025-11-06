import logging
from datetime import datetime, date
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ЛОГИРОВАНИЕ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ОБРАБОТЧИК /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветствие при запуске бота"""
    await update.message.reply_text(
        "Привет! 👋 Я бот для расчёта разницы дат.\n"
        "Отправь мне любую дату в формате ДД.ММ.ГГГГ, а я скажу — "
        "сколько дней до неё осталось или сколько уже прошло."
    )

# ОБРАБОТЧИК СООБЩЕНИЙ
async def handle_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Принимает сообщение с датой и считает разницу"""
    text = update.message.text.strip()
    try:
        # Пробуем парсить дату
        target_date = datetime.strptime(text, "%d.%m.%Y").date()
        today = date.today()
        delta = (target_date - today).days

        # Формируем ответ
        if delta > 0:
            response = f"До {target_date.strftime('%d.%m.%Y')} осталось {delta} дн."
        elif delta < 0:
            response = f"С даты {target_date.strftime('%d.%m.%Y')} прошло {abs(delta)} дн."
        else:
            response = "Это сегодня!"

        await update.message.reply_text(response)

    except ValueError:
        # Если не смогли распарсить дату
        await update.message.reply_text(
            "Пожалуйста, введи дату в формате ДД.ММ.ГГГГ (например: 07.11.2025)"
        )

#  Основной блок
def main():
    # Токен бота
    TOKEN = "ЗАМЕНИ_НА_СВОЙ_ТОКЕН"

    # Создаём приложение для ТГ
    app = ApplicationBuilder().token(TOKEN).build()

    # Регистрируем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_date))

    # Запускаем бота
    print("✅ Бот запущен. Нажми Ctrl+C для остановки.")
    app.run_polling()

if __name__ == "__main__":
    main()
