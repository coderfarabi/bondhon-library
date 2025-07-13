# library_bot.py
import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


# ✅ DATABASE SETUP
def create_table():
    conn = sqlite3.connect("./sqlite3/library.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS allbooks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            is_borrowed INTEGER DEFAULT 0,
            borrowed_by TEXT
        )
    """
    )
    conn.commit()
    conn.close()


# 🔰 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 হ্যালো! আমি তোমার লাইব্রেরি ম্যানেজমেন্ট বট! \n/start - শুরু করতে, \n /addbook <title> <author> - বই যোগ করতে, \n/listbooks - সমস্ত বইয়ের তালিকা দেখতে। \n📚 বই যোগ করতে /addbook কমান্ড ব্যবহার করো।")


# ➕ /addbook command
async def addbook(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("📚 ব্যবহার: /addbook <title> <author>")
        return
    title = args[0]
    author = " ".join(args[1:])

    conn = sqlite3.connect("./sqlite3/library.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO allbooks (title, author) VALUES (?, ?)", (title, author))
    conn.commit()
    conn.close()

    await update.message.reply_text(f"✅ বই যোগ হয়েছে: {title} - {author}")


# 📖 /listbooks command
async def listbooks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect("./sqlite3/library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, is_borrowed FROM allbooks")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        await update.message.reply_text("😕 কোনো বই পাওয়া যায়নি।")
        return

    message = "📚 সমস্ত বইয়ের তালিকা:\n\n"
    for row in rows:
        status = "✅ Available" if row[3] == 0 else "❌ Borrowed"
        message += f"🔹 ID: {row[0]} | {row[1]} - {row[2]} [{status}]\n"

    await update.message.reply_text(message)


# ✅ BOT STARTUP
def main():
    create_table()
    app = ApplicationBuilder().token("7979706249:AAEjNtitBa3g9Vw_hv-COeDyQrWisFODtns").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addbook", addbook))
    app.add_handler(CommandHandler("listbooks", listbooks))

    print("🤖 Library Bot চলছে...")
    app.run_polling()


if __name__ == "__main__":
    main()
