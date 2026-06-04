import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")

parents = {"Mafey_Alexx", "MatienkoLulu"}

kids = {
    "veronichka_anime": 5,
    "zuzu_cat45": 4
}

scores = {}
daily_tasks = {}
progress = {}

def generate_task(level):
    if level == 4:
        a, b = random.randint(10, 99), random.randint(2, 12)
    else:
        a, b = random.randint(100, 999), random.randint(10, 20)

    op = random.choice(["+", "-", "*", "/"])

    if op == "+":
        return f"{a} + {b}", a + b
    if op == "-":
        return f"{a} - {b}", a - b
    if op == "*":
        return f"{a} * {b}", a * b
    if op == "/":
        a = a * b
        return f"{a} / {b}", a // b


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.username

    if user in kids:
        level = kids[user]

        tasks = []
        for _ in range(4):
            q, ans = generate_task(level)
            tasks.append((q, ans))

        daily_tasks[user] = tasks
        progress[user] = 0
        scores.setdefault(user, 0)

        msg = "📚 Твої задачі:\n\n"
        for i, (q, _) in enumerate(tasks, 1):
            msg += f"{i}) {q} = ?\n"

        await update.message.reply_text(msg)

    elif user in parents:
        await update.message.reply_text("👨‍👩‍👧 Батьківський доступ: /stats")

    else:
        await update.message.reply_text("⛔ Немає доступу")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.username
    text = update.message.text

    if user not in kids:
        return

    if user not in daily_tasks:
        await update.message.reply_text("Спочатку /start")
        return

    try:
        answer = int(text)
    except:
        await update.message.reply_text("Введи число")
        return

    idx = progress.get(user, 0)

    if idx >= len(daily_tasks[user]):
        await update.message.reply_text("Всі задачі виконані 👍")
        return

    q, correct = daily_tasks[user][idx]

    if answer == correct:
        scores[user] = scores.get(user, 0) + 1
        await update.message.reply_text("✅ Правильно!")
    else:
        await update.message.reply_text(f"❌ Неправильно. Відповідь: {correct}")

    progress[user] = idx + 1


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.username

    if user not in parents:
        await update.message.reply_text("⛔ Нема доступу")
        return

    msg = "📊 Статистика:\n\n"
    for k in kids:
        msg += f"{k}: {scores.get(k, 0)} балів\n"

    await update.message.reply_text(msg)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()
