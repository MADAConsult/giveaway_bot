import pytz
from dotenv import load_dotenv
import os

load_dotenv()

OWNERS = [437882799, 534941597, 514668084]

bot_token = os.getenv('BOT_TOKEN')
database_url = os.getenv('DB_URL')
timezone_info = pytz.timezone('Asia/Aqtobe')

start_text = 'Главное меню: '
text_for_participation_in_comments_giveaways = 'Участвую'

