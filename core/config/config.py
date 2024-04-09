import os
import aiogram
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

admins = [
  os.getenv("ADMIN_ID"),
]

ip = os.getenv("ip")

PGUSER = str(os.getenv("PGUSER"))
PGPASSWORD = str(os.getenv("PGPASSWORD"))
DATABASE = str(os.getenv("DATABASE"))

POSTGRESURI = f"postgresql://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}"

aiogram.redis = {
  'host': ip,
}
