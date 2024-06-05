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
        ) -> None:
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
        if model_name == "Anya" or model_name == "Olya" and model_name is not None:
            tts_voice = 'ru-RU-SvetlanaNeural-Female'
        else:
            tts_voice = 'ru-RU-DmitryNeural-Male'
            model_name = "Tom"

        if len(tts_text) > 280:
            raise ValueError("Слишком много текста, напиши покорче")
        client =  Client("http://172.16.0.2:7860/")
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
        print(result)
    except Exception as e:
        print(f"Не удалось отправить запрос на сервер\n{e}")