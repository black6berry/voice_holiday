from gradio_client import Client
import asyncio

async def send_request_gradio(
        tts_text: str,
        model_name: str = 'Anya',
        speed=0,
        tts_voice: str = 'ru-RU-SvetlanaNeural-Female',
        f0_up_key=0,
        f0_method="rmvpe",
        index_rate=1,
        protect=0.33,
        api_name="/tts"
        ) -> dict:
    """
    Ф-я отправки запроса для генерации аудиодорожки
    Parameters:
        - [Dropdown] model_name: str (required)  (Option from: ['Anya', 'Marat', 'Oxxxymiron', 'Polina', 'Putin', 'Putin2', 'Roma', 'Sergey', 'Tom'])
        - [Slider] speed: float (required)  (numeric value between -100 and 100)
        - [Textbox] tts_text: str (required)
        - [Dropdown] tts_voice: str (required)  (Option from: ['ru-RU-DmitryNeural-Male', 'ru-RU-SvetlanaNeural-Female'])
        - [Number] f0_up_key: float (required)
        - [Radio] f0_method: str (required) "rmpve" or "pm"
        - [Slider] index_rate: float (required)  (numeric value between 0 and 1)
        - [Slider] protect: float (required)  (numeric value between 0 and 0.5)
        api_name="/tts"
    Returns:
        - [Textbox] output_info: str
        - [Audio] edge_voice: str (filepath on your computer (or URL) of file)
        - [Audio] result: str (filepath on your computer (or URL) of file)
    """
    try:
        if model_name in ["Anya", "Polina"]:
            tts_voice = 'ru-RU-SvetlanaNeural-Female'
        else:
            tts_voice = 'ru-RU-DmitryNeural-Male'

        if len(tts_text) > 280:
            raise ValueError("Слишком много текста, напиши покорче")
        client =  Client("http://172.16.0.2:7893/")
        result = client.predict(
            model_name=model_name,
            speed=speed,
            tts_text=tts_text,
            tts_voice=tts_voice,
            f0_up_key=f0_up_key,
            f0_method=f0_method,
            index_rate=index_rate,
            protect=protect,
            api_name=api_name)
        
        output_info = result[0]
        mp3_path = result[1]
        wav_path = result[2]
        
        result = {}
        result['output_info'] = output_info 
        result['mp3_path'] = mp3_path 
        result['wav_path'] = wav_path
        print(result)
        
        return result
    except Exception as e:
        print(f"Не удалось отправить запрос на сервер\n{e}")

# # Запуск асинхронной функции
# async def main():
#     result = await send_request_gradio(model_name='Anya', tts_text="Привет")
#     # print(result)
# # Вызов основного асинхронного метода
# asyncio.run(main())