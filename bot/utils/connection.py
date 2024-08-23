import requests
from dotmap import DotMap
from os import environ as env
from utils.logger import logger


class Connection:

    def __init__(self, api_key, api_url) -> None:
        self.api_key = api_key
        self.api_url = api_url
        self.headers = {'Authorization': f'Token {self.api_key}', 'Content-Type': 'application/json'}

    def link(self, pattern):
        return f'{self.api_url}/{pattern}/'

    @property
    def setting(self):
        pattern = 'setting'
        res = requests.get(self.link(pattern), headers=self.headers)
        if res.status_code == 200:
            setting_data = res.json()
            return DotMap(setting_data)
        else:
            res.raise_for_status()

    def file(self, unique_id_hash=None, channel_chat_id=None, user_chat_id=None, name=None, quality=None, 
             media_type=None, size=None, message_id=None ,duration=None,unique_url_path=None, subtitle_status=None, ):
 
        pattern = 'file'
        url = self.link(pattern)

        data_to_send = {}

        if unique_id_hash:
            data_to_send['unique_id_hash'] = unique_id_hash
        if channel_chat_id is not None:
            data_to_send['channel_chat_id'] = channel_chat_id
        if user_chat_id is not None:
            data_to_send['user_chat_id'] = user_chat_id
        if name is not None:
            data_to_send['name'] = name
        if quality is not None:
            data_to_send['quality'] = quality
        if media_type is not None:
            data_to_send['media_type'] = media_type
        if size is not None:
            data_to_send['size'] = size
        if message_id is not None:
            data_to_send['message_id'] = message_id
        if unique_url_path is not None:
            data_to_send['unique_url_path'] = unique_url_path
        if subtitle_status is not None:
            data_to_send['subtitle_status'] = subtitle_status
        if duration is not None :
            data_to_send['duration'] = duration
        
        
        logger.info(f"Sending data: {data_to_send}")

        if unique_id_hash and not any([channel_chat_id, user_chat_id, name, quality, media_type, size, message_id, unique_url_path, subtitle_status]):
            try:
                res = requests.delete(url, headers=self.headers, json={'unique_id_hash': unique_id_hash})
                if res.status_code == 204:
                    return True
                elif res.status_code == 404:
                    return False
                else:
                    res.raise_for_status()
            except requests.exceptions.HTTPError as http_err:
                logger.error(f"HTTP error occurred: {http_err}")
                return False
            except Exception as err:
                logger.error(f"Other error occurred: {err}")
                return False
        else:
            try:
                res = requests.post(url, headers=self.headers, json=data_to_send)
                logger.info(f"Reciving data: {data_to_send}")
                res.raise_for_status()
                
                return DotMap(res.json())
            except requests.exceptions.HTTPError as http_err:
                logger.error(f"HTTP error occurred: {http_err}")
                return False
            except Exception as err:
                logger.error(f"Other error occurred: {err}")
                return False
