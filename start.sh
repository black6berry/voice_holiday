#!/bin/bash
# Путь к виртуальной среде
VENV_PATH="./.env"
# Проверка, существует ли виртуальная среда
if [ ! -d "$VENV_PATH" ]; then
  echo "Виртуальная среда .env не найдена!"
  exit 1
fi
# Активация виртуальной среды
source /opt/voice_holiday/$VENV_PATH/bin/activate
# Запуск приложения
python3 /opt/voice_holiday/main.py
