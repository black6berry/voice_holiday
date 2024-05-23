from gradio_client import Client

model_name = ['Anya', 'Daria1', 'Dora', 'Katya', 'Kris', 'Maks', 'Marat', 'Natasha', 'Olya', 'Oxxxymiron', 'Polina', 'Putin', 'Putin2', 'Roma', 'Sasha', 'Semen', 'Sergey', 'Stepan', 'Tom', 'Yulia']
tts_voice = ['ru-RU-DmitryNeural-Male', 'ru-RU-SvetlanaNeural-Female',] 


client = Client("http://127.0.0.1:7860/")
result = client.predict(
	model_name="Roma",
	speed=0,
	tts_text="Привет",
	tts_voice="ru-RU-DmitryNeural-Male",
	f0_up_key=0,
	f0_method="rmvpe",
	index_rate=1,
	protect=0.33,
	api_name="/tts"
)
print(result)