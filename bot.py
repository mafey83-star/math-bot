import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8708433516:AAGJLRhNS105RasczF8x8Mxnyk03d87klNY"

# --- USERS ---
parents = {"Mafey_Alexx", "MatienkoLulu"}
kids = {
    "veronichka_anime": 5,   # 5 клас
    "zuzu_cat45": 4          # 4 клас
}

scores = {}

daily_tasks = {}

# --- TASK GENERATOR ---
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


# --- START ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.username

    if user in kids:
        level = kids[user]
        tasks = []

        for _ in range(4):
            q, ans = generate_task(level)
            tasks.append((q, ans))

        daily_tasks[user] = tasks
        scores.setdefault(user, 0)

        msg = "📚 Твої задачі на сьогодні:\n\n"
        for i, (q, _) in enumerate(tasks, 1):
            msg += f"{i}) {q} = ?\n"

        msg += "\n✍️ Надсилай відповіді по черзі."

        await update.message.reply_text(msg)

    elif user in parents:
        await update.message.reply_text("👨‍👩‍👧 Батьківський доступ активний. Напиши /stats")

    else:
        await update.message.reply_text("⛔ Тебе немає в системі.")


# --- ANSWERS ---
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

    task_list = daily_tasks[user]

    # знайти перший нерозв’язаний
    for i, (q, correct) in enumerate(task_list):
        if correct is not None:
            if correct == answer:
                scores[user] += 1
                task_list[i] = (q, None)
                await update.message.reply_text("✅ Правильно!")
                return
            else:
                task_list[i] = (q, None)
                await update.message.reply_text(f"❌ Неправильно. Відповідь: {correct}")
                return


# --- STATS ---
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.username

    if user not in parents:
        await update.message.reply_text("⛔ Нема доступу")
        return

    msg = "📊 Статистика:\n\n"
    for k in kids:
        msg += f"{k}: {scores.get(k, 0)} балів\n"

    await update.message.reply_text(msg)


# --- MAIN ---
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()