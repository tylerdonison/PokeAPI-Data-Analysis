import json
import requests
import threading
import pandas as pd

class Pokemon(threading.Thread):
    """description"""

    def __init__(self, json_list, url, id):
        super().__init__()
        self.url = url
        self.json_list = json_list
        self.id = id

    def run(self):
        r = requests.get(self.url)
        json = r.json()
        self.json_list.append(json)
        print(f"doing {self.id:6}", end=" ", flush=True)