import requests
from dotmap import DotMap
from os import environ as env



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

