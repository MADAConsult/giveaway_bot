import pytz
from dotenv import load_dotenv
import os

load_dotenv()

OWNERS = os.getenv('OWNERS').split(',')

bot_token = os.getenv('BOT_TOKEN')
database_url = os.getenv('DB_DRIVER') + '://' + os.getenv('DB_USER') + ':' + os.getenv('DB_PASSWORD') + '@' + os.getenv(
    'DB_HOST') + ":" + os.getenv('DB_PORT') + '/' + os.getenv('DB_NAME')
timezone_info = pytz.timezone('Asia/Aqtobe')

start_text = 'Главное меню: '
text_for_participation_in_comments_giveaways = 'Участвую'

