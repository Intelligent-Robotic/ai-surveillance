import logging
import os
import random
import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup
from telegram.ext import CallbackContext, Updater, PicklePersistence, CommandHandler, CallbackQueryHandler, \
    MessageHandler, ConversationHandler
from dotenv import load_dotenv
import os



from config import HISticker, songList

PORT = int(os.environ.get('PORT', 5000))
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)
load_dotenv()
TOKEN=os.getenv("TOKEN")
chat_id=os.getenv("CHAT_ID")
bot = telegram.Bot(token=TOKEN)
def start(update: Update, context: CallbackContext) -> None:
    sticker = random.choice(HISticker)[0]
    bot.send_sticker(chat_id=update.effective_chat.id, sticker=sticker)
    update.message.reply_text('Reporting to duty sir.All system in check and fully operational')

def alert(image):
    keyboard = [['Trigger Alarm'],['Destroy Target'],['Notified Police'],['Add Target to Guest List']]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    bot.send_photo(chat_id=chat_id, photo=image,caption="<b>Alert :</b> \nUnidentified person detected", reply_markup=reply_markup,parse_mode="HTML")



def main():
    """Start the bot."""
    updater = Updater(TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    # updater.dispatcher.add_handler(MessageHandler(Filters.text,reply))

    # updater.start_webhook(listen="0.0.0.0",
    #                       port=int(PORT),
    #                       url_path=TOKEN,
    #                       webhook_url='https://fathomless-taiga-61724.herokuapp.com/' + TOKEN)
    updater.start_polling()
    updater.idle()
    



if __name__ == '__main__':
    main()


