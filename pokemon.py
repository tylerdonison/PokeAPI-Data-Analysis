import requests

class non_thread_pokemon():
    """description"""

    def __init__(self, url):
        self.r = requests.get(url)
        self.json = self.r.json()
        self.name = self.json["name"].capitalize()
        self.id = self.json["id"]
        self.type_1 = self.json["types"][0]["type"]["name"].capitalize()
        self.type_2 = self.get_type_2().capitalize()
        self.hp =               self.json["stats"][0]["base_stat"]
        self.attack =           self.json["stats"][1]["base_stat"]
        self.defense =          self.json["stats"][2]["base_stat"]
        self.special_attack =   self.json["stats"][3]["base_stat"]
        self.special_defense =  self.json["stats"][4]["base_stat"]
        self.speed =            self.json["stats"][5]["base_stat"]
        self.data = [self.name, self.id, self.type_1, self.type_2, self.hp, self.attack, 
                    self.defense, self.special_attack, self.special_defense, self.speed]

    def get_type_2(self):
        try: #some pokemon don't have a second type, skip if they don't have one.
            type_2 = self.json["types"][1]["type"]["name"]
        except:
            type_2 = "---"
        return type_2
