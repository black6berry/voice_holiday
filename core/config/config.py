import os
import aiogram
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

# ADMIN_ID_LIST = os.environ.get("ADMIN_ID_LIST").split(',')
# ADMIN_ID_LIST = [int(admin_id) for admin_id in ADMIN_ID_LIST]

admins = [
  os.getenv("ADMIN_ID"),
]

ip = os.getenv("ip")


aiogram.redis = {
  'host': ip,
}
