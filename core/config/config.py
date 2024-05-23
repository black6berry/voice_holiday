import os
import aiogram
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

admins = [
  os.getenv("ADMIN_ID"),
]

ip = os.getenv("ip")


aiogram.redis = {
  'host': ip,
}
