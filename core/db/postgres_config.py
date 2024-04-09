import psycopg2
from core.config.config import ip, PGUSER, PGPASSWORD, DATABASE 

conn = psycopg2.connect(
  host=ip,
  port=5432,
  user=PGUSER,
  password=PGPASSWORD,
  database=DATABASE
)