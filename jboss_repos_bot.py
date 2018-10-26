import requests
from decouple import config
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters

token = config('TOKEN')
updater = Updater(token=token)
dispatcher = updater.dispatcher
repos_api = requests.get("https://api.github.com/orgs/JBossOutreach/repos")
repos_data = {repo["name"]: repo for repo in repos_api.json()}


def get_stats(bot, update):
    repo = update.message.text

    if repo.strip() in repos_data.keys():
        repo_data = repos_data[repo]
        url = repo_data["html_url"]
        description = repo_data["description"]
        stars = repo_data["stargazers_count"]
        forks = repo_data["forks"]
        watches = repo_data["watchers"]
        issues = repo_data["open_issues"]
        license_name = repo_data["license"]
        if license_name:
            license_name = license_name["name"]
        else:
            license_name = "Other"
        created_at = repo_data["created_at"].replace('T', ' ').replace('Z', '')

        stats = ("%s\nℹ️ %s\n"
                 "⭐ %i | 🔱 %i | 👁 %i | ❗️ %i\n"
                 "⚖️ %s\n📆 %s") % (
                    url, description,
                    stars, forks, watches, issues,
                    license_name, created_at
                )
        update.message.reply_text(stats)


def get_repos(bot, update):
    update.message.reply_text("Available repos:\n" +
                              "\n".join(repos_data.keys()))


dispatcher.add_handler(MessageHandler(Filters.text, get_stats))
dispatcher.add_handler(CommandHandler('list', get_repos))

updater.start_polling()
updater.idle()
