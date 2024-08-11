import os
from dotenv import load_dotenv
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import boyfriendbot

#python 3.12

load_dotenv()

TOKEN: Final = os.getenv('TOKEN')
BOT_USERNAME: Final =  os.getenv('BOT_USERNAME')

# commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thank you for chatting with me!!!')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am a bot! Please ask something so I can help.')


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command.') 


# responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return "Hey there"
    
    if 'how are you' in processed:
        return 'I am good!'
    
    if 'i love python' in processed:
        return 'Remember to subscribe!'
    
    return 'I do not understand what you wrote..'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: {text}')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
        
    else:
        best_response: str = boyfriendbot.get_message(text)
        if best_response:
            response: str = boyfriendbot.send_message(best_response)
        else:
            response: str = 'Bot: I don\'t know the answer. Can you teach me?'

        print('Bot:', response)
        await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Starting bot... ')
    app = Application.builder().token(TOKEN).build()

    #commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    #message
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errors
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3)