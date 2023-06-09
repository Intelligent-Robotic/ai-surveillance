import logging
import os
import random
import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup
from telegram.ext import CallbackContext, Updater, PicklePersistence, CommandHandler, CallbackQueryHandler, \
    MessageHandler, ConversationHandler
from dotenv import load_dotenv
import uuid
import io
from PIL import Image
import shutil
import threading
import requests
from config import HISticker, songList
from queue import Queue
import datetime



message_queue = Queue()


PORT = int(os.environ.get('PORT', 8080))
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)
load_dotenv()
TOKEN=os.getenv("TOKEN")
chat_id=os.getenv("CHAT_ID")
bot = telegram.Bot(token=TOKEN)
def start(update: Update, context: CallbackContext) -> None:
    sticker = random.choice(HISticker)[0]
    bot.send_sticker(chat_id=update.effective_chat.id, sticker=sticker)
    update.message.reply_text('Reporting to duty sir.All system in check and fully operational')

def alert(image):
    filename=save_image(image)
    image_path="./detected_list/"+filename
    keyboard = [
    [
        InlineKeyboardButton("Trigger Alarm", callback_data="1"),
        InlineKeyboardButton("Notified Police", callback_data="2"),
        InlineKeyboardButton("Add to Guest",callback_data=f"3 #{filename}"),

    ],
    [InlineKeyboardButton("Destroy Target", callback_data="4")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_photo(chat_id=chat_id, photo=open(image_path, 'rb'),caption="<b>Alert :</b> \nUnidentified person detected", reply_markup=reply_markup,parse_mode="HTML")


def save_image(image):
    # Set the folder path
    folder_path = './detected_list'

    # Generate a unique random ID
    unique_id = str(uuid.uuid4())

    # Check if a file with the same name already exists in the folder
    filename = unique_id + '.jpg'
    file_path = os.path.join(folder_path, filename)
    while os.path.exists(file_path):
        unique_id = str(uuid.uuid4())
        filename = unique_id + '.jpg'
        file_path = os.path.join(folder_path, filename)

    # Create the image from the BytesIO object
    image2 = Image.open(image)

    # Save the image to the file path
    image2.save(file_path)
    print(filename)
    return filename

def trigger_alarm(update,context):
    respond = requests.get(os.getenv("ACTION_URL") + "/sound_alarm")
    print('alarm triggered')

def send_recording(text):
    bot.send_message(chat_id=chat_id, text=f"<b>Recording Transcribe</b>\n\n{text}", parse_mode="HTML")
    print(text)

def notify_police(update,context):
    bot.send_message(chat_id=chat_id, text=f"<b>Police has been notified</b>\nTime : {str(datetime.datetime.now())}", parse_mode="HTML")
    print('police notified')


def speak(update,context):
    print("hello")
    text_args = ' '.join(context.args)
    params = {
    'text': text_args,
    }
    respond = requests.get(os.getenv("ACTION_URL") + "/speak",params=params)
    print(text_args)



def add_to_guest(update,context):
    update.callback_query.answer()
    filename = ((str(update.callback_query.data).split("#"))[1])
    # Set the source and destination folder paths
    src_folder = './detected_list'
    dst_folder = './guest_list'

    
    # Set the source and destination file paths
    src_path = os.path.join(src_folder, filename)
    dst_path = os.path.join(dst_folder, filename)

    # Move the photo from the source folder to the destination folder
    shutil.move(src_path, dst_path)
    message_queue.put('guest_list_update')

   

  


def main():
    """Start the bot."""
    updater = Updater(TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(trigger_alarm, pattern='1'))
    updater.dispatcher.add_handler(CallbackQueryHandler(add_to_guest, pattern='3'))
    updater.dispatcher.add_handler(CommandHandler('speak', speak, pass_args=True))




    # updater.start_webhook(listen="0.0.0.0",
    #                       port=int(PORT),
    #                       url_path=TOKEN,
    #                       webhook_url='http://192.168.0.133' + TOKEN)
    updater.start_polling()
    updater.idle()
    



# if __name__ == '__main__':
thread = threading.Thread(target=main)
thread.start()


