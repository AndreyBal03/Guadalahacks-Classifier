from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = '7066923535:AAETrI2qZQCAoEH6g2kg35UOdWlTPRRbtNw'
BOT_USERNAME: Final = '@closet_ai_bot'

#commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am Closet AI. Use my commands to start.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """I am an artificial intelligence that has the purpose of identifying
        clothes through user-input images. Use my 'Send image' command to try it out""")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command.')
    
#Bot responses
def handle_response(text: str) -> str:
    if 'hello' in text:
        return 'Hello!'