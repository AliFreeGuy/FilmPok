import requests
from dotmap import DotMap
from utils.logger import logger


class Connection:

    def __init__(self, api_key, api_url) -> None:
        self.api_key = api_key
        self.api_url = api_url
        self.headers = {'Authorization': f'Token {self.api_key}', 'Content-Type': 'application/json'}

    def link(self, pattern):
        return f'{self.api_url}/{pattern}/'

    def file_channel(self, chat_id, message_id):
        pattern = 'save-file-channel'  # استفاده از 'save-file-channel' به عنوان pattern
        data = {'chat_id': chat_id, 'message_id': message_id}
        res = requests.post(self.link(pattern), json=data, headers=self.headers)
        
        if res.status_code == 200:
            return DotMap(res.json())
        else:
            logger.error(f"HTTP error occurred: {res.status_code} - {res.text}")
            return None

    def file(self, unique_id_hash=None, channel=None, user_chat_id=None, name=None, quality=None, 
             media_type=None, size=None, duration=None, unique_url_path=None, subtitle_status=None):

        pattern = 'files'  # استفاده از 'files' به عنوان pattern
        url = self.link(pattern)

        data_to_send = {}

        if unique_id_hash:
            data_to_send['unique_id_hash'] = unique_id_hash
        if channel is not None:
            data_to_send['channel'] = channel
        if user_chat_id is not None:
            data_to_send['user'] = user_chat_id
        if name is not None:
            data_to_send['name'] = name
        if quality is not None:
            data_to_send['quality'] = quality
        if media_type is not None:
            data_to_send['media_type'] = media_type
        if size is not None:
            data_to_send['size'] = size
        if duration is not None:
            data_to_send['duration'] = duration
        if unique_url_path is not None:
            data_to_send['unique_url_path'] = unique_url_path
        if subtitle_status is not None:
            data_to_send['subtitle_status'] = subtitle_status

        logger.info(f"Sending data: {data_to_send}")

        try:
            res = requests.post(url, headers=self.headers, json=data_to_send)
            print(res.text)
            res.raise_for_status()
            response_data = res.json()
            logger.info(f"Received data: {response_data}")
            return DotMap(response_data)
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            return None
        except Exception as err:
            logger.error(f"Other error occurred: {err}")
            return None

    @property
    def setting(self):
        pattern = 'setting'  # استفاده از 'setting' به عنوان pattern
        res = requests.get(self.link(pattern), headers=self.headers)
        if res.status_code == 200:
            setting_data = res.json()
            return DotMap(setting_data)
        else:
            res.raise_for_status()
