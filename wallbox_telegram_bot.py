#!/usr/bin/env python3
# pylint: disable=C0116,W0613

import logging
from turtle import up

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from wallbox_control import get_status_str, exec_enable_auto, exec_activate, exec_deactivate

HELP_MSG = '''Available commands:
/status - show latest status
/week - show SOC over last 7 days
/auto - enable auto mode
/on - turn permanently on
/off - turn permanently off
either send them as command or message without /'''

authorized_users = ["korbi98", "roswitha70"]

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def get_username(update: Update) -> str:
    return update.message.from_user['username']

def is_user_authorized(update: Update) -> bool:
    return get_username(update) in authorized_users


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    if is_user_authorized(update):
        user = update.effective_user
        update.message.reply_text("Welcome {}".format(user.first_name))
        update.message.reply_text(HELP_MSG)
    else:
        update.message.reply_text("You are not in the list of authorized users!")
    

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    if is_user_authorized(update):
        update.message.reply_text(HELP_MSG)
    else:
        update.message.reply_text("You are not in the list of authorized users!")


def status_command(update: Update, context: CallbackContext) -> None:
    if is_user_authorized(update):
        status = get_status_str()
        msg = "Wallbox and battery status: \n{}".format(status)
        update.message.reply_text(msg)
        img_path = '/home/pi/wallbox_controller/www/soc_over_time.png'
        update.message.reply_photo(open(img_path, 'rb'))
    else:
        update.message.reply_text("You are not in the list of authorized users!")


def week_command(update: Update, context: CallbackContext) -> None:
    if is_user_authorized(update):
        img_path = '/home/pi/wallbox_controller/www/soc_over_time_week.png'
        update.message.reply_photo(open(img_path, 'rb'))
    else:
        update.message.reply_text("You are not in the list of authorized users!")


def auto_command(update: Update, context: CallbackContext) -> None:
    if is_user_authorized(update):
        exec_enable_auto()
        status = get_status_str()
        update.message.reply_text("Auto mode enabled")
        msg = "Wallbox and battery status: \n{}".format(status)
        update.message.reply_text(msg)
    else:
        update.message.reply_text("You are not in the list of authorized users!")
        

def on_command(update: Update, context: CallbackContext) -> None:
    if is_user_authorized(update):
        res = exec_activate()
        if res == "1":
            update.message.reply_text("wallbox successfully activated")
        else:
            update.message.reply_text("I am sorry there was an error")
    else:
        update.message.reply_text("You are not in the list of authorized users!")


def off_command(update: Update, context: CallbackContext) -> None:
    if is_user_authorized(update):
        res = exec_deactivate()
        if res == "0":
            update.message.reply_text("wallbox successfully deactivated")
        else:
            update.message.reply_text("I am sorry there was an error")
    else:
        update.message.reply_text("You are not in the list of authorized users!")


def handle_message(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    message = update.message.text
    
    if is_user_authorized(update):
        if message == "status":
            status = get_status_str()
            msg = "Wallbox and battery status: \n{}".format(status)
            update.message.reply_text(msg)
            img_path = '/home/pi/wallbox_controller/www/soc_over_time.png'
            update.message.reply_photo(open(img_path, 'rb'))
        elif message == "week":
            img_path = '/home/pi/wallbox_controller/www/soc_over_time_week.png'
            update.message.reply_photo(open(img_path, 'rb'))
        elif message == "auto":
            exec_enable_auto()
            status = get_status_str()
            update.message.reply_text("Auto mode enabled")
            msg = "Wallbox and battery status: \n{}".format(status)
            update.message.reply_text(msg)
        elif message == "on":
            res = exec_activate()
            if res == "1":
                update.message.reply_text("wallbox successfully activated")
            else:
                update.message.reply_text("I am sorry there was an error")
        elif message == "off":
            res = exec_deactivate()
            if res == "0":
                update.message.reply_text("wallbox successfully deactivated")
            else:
                update.message.reply_text("I am sorry there was an error")
        else:
            update.message.reply_text("Command does not exist!")
            update.message.reply_text(HELP_MSG)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("YourAPItoken")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("status", status_command))
    dispatcher.add_handler(CommandHandler("week", week_command))
    dispatcher.add_handler(CommandHandler("auto", auto_command))
    dispatcher.add_handler(CommandHandler("on", on_command))
    dispatcher.add_handler(CommandHandler("off", off_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
