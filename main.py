import requests
from telegram import Update
from telegram.ext import Application, Updater, CommandHandler, ContextTypes
# from apscheduler.schedulers.background import BackgroundScheduler

# Telegram Bot Token
TOKEN = '7169420603:AAFXWUqtOO5GHgiTUyV2Cc7zuyyPxdbpu88'
 # Giphy API Key
GIPHY_API_KEY = '9E3X2WLpbZ1WXPvVBKq4PAGlnawiEEoi'
# Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to Giphy Views Tracker Bot!")

async def set_project(update: Update,context: ContextTypes.DEFAULT_TYPE):
    project_name = " ".join(context.args)
    # TODO: Store the project name associated with the user in the database
    await update.message.reply_text(f"Project '{project_name}' set successfully!")

async def get_views(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: Fetch total views for the specified project from Giphy API
    project_name = " ".join(context.args)
    total_views = 1000  # Placeholder for total views
    url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={project_name}&limit=1"
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        total_views = data['pagination']['total_count']
        # return total_views
        await update.message.reply_text(f"Total views: {total_views}, {project_name}")
    else:
        print(f"Failed to fetch data from Giphy API. Status code: {response.status_code}")
        # return None
        await update.message.reply_text(f"Total views: 0, {project_name}")
    # await update.message.reply_text(f"Total views: {total_views}, {project_name}")


# Function to send daily updates to users
def send_daily_updates():
    # Fetch total views for the specified project from Giphy
    project_name = "YOUR_PROJECT_NAME"
    total_views = get_views(project_name)

    if total_views is not None:
        # Send daily update to users
        subscribers = ["@Swissmote2bot"]  # Replace with actual user IDs
        for user_id in subscribers:
            Updater.bot.send_message(chat_id=user_id,
                                     text=f"Daily Update for {project_name}: Total Views - {total_views}")
# Main function
def main() -> None:
    # updater = Updater(TOKEN)
    # dispatcher = updater.dispatcher
    # Start the scheduler
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(send_daily_updates, "cron", hour=0)  # Send daily updates at 00:00 UTC
    # scheduler.start()
    print('Starting bot ...')
    app = Application.builder().token(TOKEN).build()

    # Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setproject", set_project))
    app.add_handler(CommandHandler("views", get_views))

    print('Polling ...')
    app.run_polling(poll_interval=5)

if __name__ == "__main__":
    main()
