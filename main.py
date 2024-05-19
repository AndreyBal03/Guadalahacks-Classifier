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

async def image_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Upload an image of a piece of cloth so I can start identifying it.')
    
#Bot responses
def handle_response(text: str) -> str:
    processed: str = text.lower()
    
    if 'hello' in processed:
        return 'Hello! Glad to see you here. Upload the image of the piece of cloth you want me to identify.'
    
    return """I did not quite catch that. If you are having trouble, 
           you can use my /help command to see my functionalities."""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
        
    print('Bot: ', response)
    await update.message.reply_text(response)
    
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')
    
if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()
    
    #Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', start_command))
    app.add_handler(CommandHandler('upload_image', start_command))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    #Errors
    app.add_error_handler(error)
    
    #Polls the bot
    print('Polling...')
    app.run_polling(poll_interval= 3)