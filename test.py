from telegram.ext import Updater, MessageHandler, Filters

# Define a function to handle incoming messages
def echo(update, context):
    # Get the message text
    message = update.message.text
    # Echo the message back
    update.message.reply_text(message)

# Create an Updater object and attach it to your bot token
updater = Updater("6221913443:AAHu_ru_PQgqXtNbDB5DgEQuqn0NUBxtFMw")

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Register the echo function as a message handler
dispatcher.add_handler(MessageHandler(Filters.text, echo))

# Start the bot
updater.start_polling()

# Run the bot until you press Ctrl-C to stop it
updater.idle()

