from decouple import config
import requests
from telegram.ext import Updater, MessageHandler, Filters

token = config('TOKEN')
updater = Updater(token=token)
dispatcher = updater.dispatcher
repos_api = requests.get("https://api.github.com/orgs/JBossOutreach/repos")
repos_data = {repo["name"]: repo for repo in repos_api.json()}


def stalk(bot, update):
    repo = update.message.text

    if repo.strip() in repos_data.keys():
        repo_data = repos_data[repo]
        url = repo_data["html_url"]
        description = repo_data["description"]
        stars = repo_data["stargazers_count"]
        forks = repo_data["forks"]
        watches = repo_data["watchers"]
        issues = repo_data["open_issues"]
        license_name = repo_data["license"]["name"]

        stats = ("%s\nℹ️ %s\n"
                 "⭐ %i | 🔱 %i | 👁 %i | ❗️ %i\n"
                 "⚖️ %s\n") % (
                    url, description,
                    stars, forks, watches, issues,
                    license_name
                )
        update.message.reply_text(stats)


dispatcher.add_handler(MessageHandler(Filters.text, stalk))

updater.start_polling()
updater.idle()
