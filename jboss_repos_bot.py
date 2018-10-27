import requests
from decouple import config
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters

token = config('TOKEN')
updater = Updater(token=token)
dispatcher = updater.dispatcher
STARGAZERS_URL = "https://api.github.com/repos/%s/stargazers"


def get_stats(bot, update):
    repo = update.message.text
    repo_stargazers = requests.get(STARGAZERS_URL % repo).json()
    if type(repo_stargazers) != list:
        return
    msg = ""

    if len(repo_stargazers) > 0:
        msg = ("Users who starred this repo:\n" +
               "\n".join(user["html_url"] for user in repo_stargazers))
    elif len(repo_stargazers) == 0:
        msg = "No one starred the repo 🙁"

    update.message.reply_text(msg)


def get_help(bot, update):
    update.message.reply_text("To get info about repository watchers "
                              "send the name of github repository like this - "
                              "*owner name*/*repo name*.\n"
                              "Try to send: \"JBossOutreach/jboss-logo\"")


dispatcher.add_handler(MessageHandler(Filters.text, get_stats))
dispatcher.add_handler(CommandHandler("help", get_help))

updater.start_polling()
updater.idle()
