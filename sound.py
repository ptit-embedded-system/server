from datetime import datetime

from gtts import gTTS

from client import cloudinary_client
from client import redis_client


def convert_text_to_speech(text) -> str:
    if len(text) == 0:
        return ""
    tts = gTTS(text=text, lang='vi')
    sound_name = f'./alert_sound/{get_time()}.mp3'
    tts.save(sound_name)
    cld = cloudinary_client.CloudinaryClient()
    resp = dict(cld.upload_file(file_path=sound_name))
    redis = redis_client.RedisClient()
    redis.set(sound_name, resp.get("secure_url"))
    return sound_name


def get_sound_path(sound_name) -> str:
    redis = redis_client.RedisClient()
    return redis.get(sound_name)


def get_time() -> str:
    now = datetime.now()
    timestamp_str = now.strftime("%d%m%Y%H%M%S%f")
    return timestamp_str


if __name__ == "__main__":
    convert_text_to_speech("dô lề, xe hốt bây giờ")
