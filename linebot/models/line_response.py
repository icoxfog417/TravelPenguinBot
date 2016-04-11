from linebot.models.line_types import ContentType


class LineResponse():

    def __init__(self, to_mids, content=None):
        self.to_mids = to_mids if isinstance(to_mids, (list, tuple)) else [to_mids]
        self.to_channel = 1383378250  # Fixed value
        self.event_type = "138311608800106203"  # Fixed value
        self.content = {} if content is None else content

    def set_text(self, text):
        self.content = {
            "contentType": ContentType.text.value,
            "toType": 1,
            "text": text
        }

    def set_image(self, image_url, thumbnail_url=""):
        self.content = {
            "contentType": ContentType.image.value,
            "toType": 1,
            "originalContentUrl": image_url,
            "previewImageUrl": thumbnail_url if thumbnail_url else image_url
        }

    def set_video(self, video_url, preview_url):
        self.content = {
            "contentType": ContentType.video.value,
            "toType": 1,
            "originalContentUrl": video_url,
            "previewImageUrl": preview_url
        }

    def set_audio(self, audio_url, audio_length):
        # audio length is millisec
        self.content = {
            "contentType": ContentType.audio.value,
            "toType": 1,
            "originalContentUrl": audio_url,
            "contentMetada": {
                "AUDLEN": audio_length
            }
        }

    def set_location(self, text, title, lat, lng):
        self.content = {
            "contentType": ContentType.location.value,
            "toType": 1,
            "text": text,
            "location": {
                "title": title,
                "latitude": lat,
                "longitude": lng
            }
        }

    def set_sticker(self, sticker_id, package_id, version=""):
        sticker = {
            "STKID": sticker_id,
            "STKPKGID": package_id
        }

        if version:
            sticker["STKVER"] = version

        self.content = {
            "contentType": ContentType.sticker.value,
            "toType": 1,
            "contentMetadata": sticker
        }

    def to_dict(self):
        _dict = {
            "to": self.to_mids,
            "toChannel": self.to_channel,
            "eventType": self.event_type,
            "content": self.content
        }

        return _dict
