from datetime import datetime

from gtts import gTTS


def convert_text_to_speech(text):
    if len(text) == 0:
        return
    tts = gTTS(text=text, lang='vi')
    tts.save(f'alert_sound/{get_time()}.mp3')


def get_time() -> str:
    now = datetime.now()
    timestamp_str = now.strftime("%d%m%Y%H%M%S%f")
    return timestamp_str


if __name__ == "__main__":
    convert_text_to_speech("cút dô lề, xe hốt bây giờ")
