from telegram.ext import CommandHandler, MessageHandler, Filters
from django_telegrambot.apps import DjangoTelegramBot
from larp_egov.apps.accounts.services.deeplink import bind_user, delete_user, verify_user
from larp_egov.apps.accounts.bot_tasks import notify_admins

import logging
logger = logging.getLogger(__name__)


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def register(bot, update):
    success, result = bind_user(update)
    if not success:
        bot.sendMessage(update.message.chat_id, text=result)
        return
    notify_admins(bot, result)
    bot.sendMessage(update.message.chat_id, text="You've been successfully linked; await for verification")


def verify(bot, update):
    success, result = verify_user(update)
    if not success:
        bot.sendMessage(update.message.chat_id, text=result)
        return
    bot.sendMessage(result.telegram_id, text="Your character was successfully verified")


def delete(bot, update):
    success, result = delete_user(update)
    if not success:
        bot.sendMessage(update.message.chat_id, text=result)
        return
    bot.sendMessage(result, text="Your character was deleted by administration")


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    logger.info("Loading handlers for telegram bot")

    # Default dispatcher (this is related to the first bot in settings.DJANGO_TELEGRAMBOT['BOTS'])
    dp = DjangoTelegramBot.dispatcher
    # To get Dispatcher related to a specific bot
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_token')     #get by bot token
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_username')  #get by bot username

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("register", register))
    dp.add_handler(CommandHandler("verify", verify))
    dp.add_handler(CommandHandler("delete", delete))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)